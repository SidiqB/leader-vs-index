"""Why does "own the #1 company" work in some markets and not others?

    python research.py            # writes tables and charts to research/

1. Event study: every time a new company becomes #1, how do the new and the old #1 do
   over the next week / month / quarter / year, relative to the index?
2. Whipsaw: how often does #1 change hands and flip straight back, and how close are
   #1 and #2 in size?
3. Leader quality: how did the companies that held #1 perform over their time at the top?
4. Attribution: how much of each strategy's result came from its single best stretch?
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd
from tabulate import tabulate

from leadertrack.analysis import holding_periods, run_backtest, summary_table
from leadertrack.indices import INDICES
from leadertrack.plots import INDEX_INK, SERIES, SURFACE, TEXT2
from leadertrack.strategies import daily_ranks, membership_mask

OUT = Path(__file__).resolve().parent / "research"
HORIZONS = {"1 week": 5, "1 month": 21, "3 months": 63, "1 year": 252}
START = str((pd.Timestamp.today().normalize() - pd.DateOffset(years=20)).date())

SECTOR = {
    "MSFT": "Tech", "AAPL": "Tech", "NVDA": "Tech", "GOOGL": "Tech", "META": "Tech", "AMZN": "Tech",
    "AVGO": "Tech", "CSCO": "Tech", "INTC": "Tech", "ORCL": "Tech", "IBM": "Tech", "QCOM": "Tech",
    "NFLX": "Tech", "TSLA": "Autos", "SAP.DE": "Tech",
    "XOM": "Energy", "CVX": "Energy", "SHEL.L": "Energy", "BP.L": "Energy", "EOAN.DE": "Utilities",
    "GE": "Industrials", "SIE.DE": "Industrials", "AIR.DE": "Industrials", "RHM.DE": "Industrials",
    "WMT": "Consumer", "PG": "Consumer", "KO": "Consumer", "COST": "Consumer", "ULVR.L": "Consumer",
    "BATS.L": "Consumer", "DGE.L": "Consumer",
    "C": "Financials", "JPM": "Financials", "BAC": "Financials", "BRK-B": "Financials", "V": "Financials",
    "HSBA.L": "Financials", "LSEG.L": "Financials", "ALV.DE": "Financials", "MUV2.DE": "Financials",
    "JNJ": "Healthcare", "PFE": "Healthcare", "LLY": "Healthcare", "AZN.L": "Healthcare", "GSK.L": "Healthcare",
    "BAYN.DE": "Healthcare",
    "VOD.L": "Telecom", "DTE.DE": "Telecom", "RIO.L": "Materials", "BAS.DE": "Materials", "LIN.DE": "Materials",
    "MBG.DE": "Autos", "VOW3.DE": "Autos",
}


def leader_series(bt) -> tuple[pd.Series, pd.DataFrame, pd.DataFrame]:
    md = bt.md
    caps = md.market_cap.loc[bt.start:]
    tr = md.total_return.loc[bt.start:]
    elig = membership_mask(bt.index, caps.index, list(caps.columns)) & caps.notna() & tr.notna()
    ranks = daily_ranks(caps, elig)
    ok = ranks.notna().any(axis=1)
    lead = pd.Series(None, index=caps.index, dtype=object)
    lead[ok] = ranks[ok].idxmin(axis=1)
    return lead, caps.where(elig), tr


def event_study(bt) -> pd.DataFrame:
    lead, caps, tr = leader_series(bt)
    bench = bt.md.benchmark.reindex(tr.index).ffill()
    rows = []
    idx = tr.index
    for i in range(1, len(lead)):
        new, old = lead.iloc[i], lead.iloc[i - 1]
        if not isinstance(new, str) or not isinstance(old, str) or new == old:
            continue
        row = {"date": idx[i], "new": new, "old": old}
        # momentum into the crossover: the month before
        j = max(i - 21, 0)
        row["new: prior month vs index"] = tr[new].iloc[i] / tr[new].iloc[j] - bench.iloc[i] / bench.iloc[j]
        row["old: prior month vs index"] = tr[old].iloc[i] / tr[old].iloc[j] - bench.iloc[i] / bench.iloc[j]
        for label, h in HORIZONS.items():
            k = i + h
            if k >= len(idx):
                continue
            b = bench.iloc[k] / bench.iloc[i] - 1
            row[f"new: next {label} vs index"] = tr[new].iloc[k] / tr[new].iloc[i] - 1 - b
            row[f"old: next {label} vs index"] = tr[old].iloc[k] / tr[old].iloc[i] - 1 - b
            row[f"new minus old: next {label}"] = (tr[new].iloc[k] / tr[new].iloc[i]) - (tr[old].iloc[k] / tr[old].iloc[i])
        # did leadership flip straight back?
        back = lead.iloc[i + 1:i + 22]
        row["flipped back within a month"] = bool((back == old).any())
        rows.append(row)
    return pd.DataFrame(rows)


def leadership_closeness(bt) -> dict:
    lead, caps, _ = leader_series(bt)
    vals = np.nan_to_num(caps.to_numpy(dtype=float), nan=-np.inf)
    top2 = np.sort(vals, axis=1)[:, ::-1][:, :2]
    gap = top2[:, 0] / top2[:, 1] - 1
    changes = (lead != lead.shift()).iloc[1:].sum()
    years = (caps.index[-1] - caps.index[0]).days / 365.25
    return {"Median gap #1 vs #2": float(np.nanmedian(gap)),
            "Days with gap under 5%": float(np.nanmean(gap < 0.05)),
            "Leader changes per year": changes / years}


def leader_quality(bt) -> pd.DataFrame:
    """For each company, its return vs the index *while it was #1*, and over the whole period."""
    lead, _, tr = leader_series(bt)
    bench = bt.md.benchmark.reindex(tr.index).ffill()
    daily = tr.pct_change()
    bdaily = bench.pct_change()
    rows = []
    names = bt.names()
    for t in lead.dropna().unique():
        held = (lead.shift() == t)  # returns earned the day after being #1
        ex = (np.log1p(daily[t][held]) - np.log1p(bdaily[held])).sum()
        whole = tr[t].dropna()
        yrs = (whole.index[-1] - whole.index[0]).days / 365.25
        bw = bench.reindex(whole.index)
        rows.append({
            "Company": names.get(t, t), "Sector": SECTOR.get(t, "?"), "Share of days as #1": held.mean(),
            "Excess return vs index while #1 (a year)": np.expm1(ex / max(held.sum() / 252, 1e-9)),
            "Excess return vs index, whole period (a year)":
                (whole.iloc[-1] / whole.iloc[0]) ** (1 / yrs) - (bw.iloc[-1] / bw.iloc[0]) ** (1 / yrs),
        })
    df = pd.DataFrame(rows).sort_values("Share of days as #1", ascending=False)
    return df[df["Share of days as #1"] >= 0.02]  # a few days at #1 can't be annualised meaningfully


def incumbent_edge(bt) -> pd.DataFrame:
    """Patient models keep holding while their company is #2. Was that a good idea?

    On every day a patient strategy held the #2 company, compare its return with the
    #1 company it refused to buy (yet)."""
    lead, _, tr = leader_series(bt)
    daily = np.log1p(tr.pct_change())
    out = {}
    for r in bt.results:
        if r.config.kind != "patient":
            continue
        held = r.holding.shift()  # what we held overnight into each day
        rank = r.ranks_of_holding.shift()
        prev_lead = lead.shift()
        mask = (rank == 2) & held.notna() & prev_lead.notna()
        diffs = [daily.at[d, held[d]] - daily.at[d, prev_lead[d]] for d in mask[mask].index]
        days = len(diffs)
        out[r.config.name] = {"Days held at #2": days,
                              "Held #2 minus #1 on those days (total)": float(np.expm1(np.nansum(diffs))) if days else np.nan}
    return pd.DataFrame(out).T


def best_stretch_share(bt) -> pd.DataFrame:
    out = {}
    bench_nav = bt.nav[bt.benchmark_label]
    for r in bt.results:
        hp = holding_periods(r, bench_nav, bt.names())
        log_ex = np.log1p(hp["Return"]) - np.log1p(hp["Index return"])
        best = hp.loc[log_ex.idxmax()]
        out[r.config.name] = {
            "Best stretch": f"{best['Company']} {best['From']} → {best['To']}",
            "Its excess vs index": best["Excess"],
            "Total excess, all stretches (log)": log_ex.sum(),
            "Total excess without best stretch (log)": log_ex.sum() - log_ex.max(),
        }
    return pd.DataFrame(out).T


def main():
    OUT.mkdir(exist_ok=True)
    plt.rcParams.update({"figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "axes.spines.top": False,
                         "axes.spines.right": False, "axes.grid": True, "grid.color": "#e6e5e0"})
    summary_rows, closeness, events_all, quality_all, stretches, incumbent = [], {}, [], [], [], []
    for key, idx in INDICES.items():
        print(f"{idx.name}…")
        bt = run_backtest(key, start=START)
        s = summary_table(bt)
        ev = event_study(bt).assign(index=idx.name)
        events_all.append(ev)
        closeness[idx.name] = leadership_closeness(bt)
        q = leader_quality(bt).assign(Index=idx.name)
        quality_all.append(q)
        stretches.append(best_stretch_share(bt).assign(Index=idx.name))
        incumbent.append(incumbent_edge(bt).assign(Index=idx.name))
        summary_rows.append({"Index": idx.name, **{n: s.loc[n, "CAGR vs index"] for n in s.index
                                                   if n != bt.benchmark_label}})

    ev = pd.concat(events_all)
    ev.to_csv(OUT / "leader_change_events.csv", index=False)
    pd.concat(quality_all).to_csv(OUT / "leader_quality.csv", index=False)
    pd.concat(stretches).to_csv(OUT / "best_stretch.csv")
    inc = pd.concat(incumbent)
    inc.to_csv(OUT / "incumbent_edge.csv")
    print(tabulate(inc, headers="keys", tablefmt="simple"))
    clos = pd.DataFrame(closeness).T
    clos.to_csv(OUT / "leadership_closeness.csv")
    summ = pd.DataFrame(summary_rows).set_index("Index")
    summ.to_csv(OUT / "cagr_vs_index.csv")

    # average event response by index
    cols = ["new: prior month vs index"] + [f"new: next {h} vs index" for h in HORIZONS] + \
           ["old: prior month vs index"] + [f"old: next {h} vs index" for h in HORIZONS] + \
           [f"new minus old: next {h}" for h in HORIZONS] + ["flipped back within a month"]
    avg = ev.groupby("index")[cols].mean().reindex([i.name for i in INDICES.values()])
    avg.insert(0, "Leader changes", ev.groupby("index").size())
    avg.to_csv(OUT / "event_study_averages.csv")
    hit = ev.groupby("index")[[f"new minus old: next {h}" for h in HORIZONS]].agg(lambda x: (x > 0).mean())
    hit.to_csv(OUT / "event_study_hit_rate.csv")

    print(tabulate((avg * 100).round(2), headers="keys", tablefmt="simple"))
    print(tabulate(clos.round(3), headers="keys", tablefmt="simple"))

    # chart 1: new #1 minus old #1 after a change, by horizon
    fig, ax = plt.subplots(figsize=(10, 5))
    names = list(avg.index)
    x = np.arange(len(HORIZONS))
    w = 0.8 / len(names)
    for n, name in enumerate(names):
        vals = [avg.loc[name, f"new minus old: next {h}"] for h in HORIZONS]
        ax.bar(x + (n - (len(names) - 1) / 2) * w, vals, w * 0.9, color=SERIES[n], label=name)
    ax.axhline(0, color=INDEX_INK, lw=1)
    ax.set_xticks(x, [f"next {h}" for h in HORIZONS])
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0, decimals=0))
    ax.set_title("After a new company takes #1: return of the new #1 minus the old #1 (average)", loc="left",
                 fontweight="bold")
    ax.legend(frameon=False, fontsize=9)
    fig.savefig(OUT / "new_minus_old_after_change.png", dpi=120, bbox_inches="tight")
    plt.close(fig)

    # chart 2: did the market's #1 companies beat the index? vs how the patient strategy did
    fig, ax = plt.subplots(figsize=(7.5, 5))
    leaders_beat = avg[["new: next 1 year vs index", "old: next 1 year vs index"]].mean(axis=1)
    patient = summ["Patient: 1-month confirm"]
    for n, name in enumerate(avg.index):
        ax.scatter(leaders_beat[name], patient[name], s=110, color=SERIES[n], edgecolor=SURFACE, linewidth=2)
        ax.annotate(name, (leaders_beat[name], patient[name]), xytext=(7, 4), textcoords="offset points",
                    fontsize=9, color=TEXT2)
    ax.axhline(0, color=INDEX_INK, lw=1)
    ax.axvline(0, color=INDEX_INK, lw=1)
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.0, decimals=0))
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0, decimals=0))
    ax.set_xlabel("Average return of the top-2 companies vs the index, over the year after a leader change")
    ax.set_ylabel("Patient (1-month) CAGR minus index")
    ax.set_title("It worked where the biggest companies kept beating their index", loc="left", fontweight="bold")
    fig.savefig(OUT / "leaders_vs_strategy.png", dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved to {OUT}")


if __name__ == "__main__":
    main()
