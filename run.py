"""Command-line runner.

    python run.py                      # pick an index from a menu, watch the animation
    python run.py --index sp500        # run straight away
    python run.py --all --no-show      # every index, save results only
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import pandas as pd
from tabulate import tabulate

from leadertrack.analysis import (fmt_summary, holding_periods, leader_history, run_backtest, summary_table,
                                  tax_comparison, time_held, yearly_returns)
from leadertrack.indices import INDICES
from leadertrack.strategies import StrategyConfig, TaxConfig

ROOT = Path(__file__).resolve().parent


def build_strategies(a) -> tuple[StrategyConfig, ...]:
    out = [StrategyConfig("Naive: always #1", kind="naive", cost_bps=a.naive_cost_bps)]
    for days in a.confirm_days:
        label = {7: "1-week", 30: "1-month"}.get(days, f"{days}-day")
        out.append(StrategyConfig(f"Patient: {label} confirm", kind="patient", min_age_days=a.min_age_days,
                                  confirm_days=days, drop_rank=a.drop_rank, cost_bps=a.cost_bps))
    return tuple(out)


def choose_index() -> str:
    keys = list(INDICES)
    print("\nWhich index?")
    for n, k in enumerate(keys, 1):
        print(f"  {n}. {INDICES[k].name}  (benchmark {INDICES[k].benchmark})")
    while True:
        pick = input(f"Enter 1-{len(keys)} [1]: ").strip() or "1"
        if pick.isdigit() and 1 <= int(pick) <= len(keys):
            return keys[int(pick) - 1]
        if pick in INDICES:
            return pick


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


def run_one(key: str, a) -> None:
    from leadertrack import plots

    print(f"\n=== {INDICES[key].name} ===")
    tax = TaxConfig(rate=a.tax_rate / 100,
                    short_term_rate=None if a.short_term_tax_rate is None else a.short_term_tax_rate / 100)
    bt = run_backtest(key, start=a.start, end=a.end, capital=a.capital, strategies=build_strategies(a),
                      offline=a.offline, tax=tax, progress=lambda f, msg: print(f"\r  {msg:<40}", end="", flush=True))
    print("\r" + " " * 50)
    out = ROOT / a.out / key
    out.mkdir(parents=True, exist_ok=True)

    summary = summary_table(bt)
    yearly = yearly_returns(bt)
    shown = fmt_summary(summary, bt.capital)
    cols = ["Final value", "Total return", "CAGR", "CAGR vs index", "Volatility", "Max drawdown", "Sharpe (rf=0)",
            "Trades"]
    if tax.active:
        print("Values below already have the tax paid on each switch taken out (before the final sale).")
    print(tabulate(shown[cols], headers="keys", tablefmt="rounded_outline"))
    taxcmp = None
    if tax.active:
        untaxed = run_backtest(key, start=a.start, end=a.end, capital=a.capital, strategies=build_strategies(a),
                               md=bt.md)
        taxcmp = tax_comparison(bt, untaxed)
        taxcmp.to_csv(out / "tax_comparison.csv")
        taxcmp_fmt = taxcmp.copy().astype(object)
        for c in taxcmp:
            taxcmp_fmt[c] = taxcmp[c].map((lambda v: f"{v:+.1%}") if "vs index" in c else
                                          (lambda v: f"{v:.1%}") if ("CAGR" in c or c == "Lost to tax") else
                                          (lambda v: f"{v:,.0f}"))
        print(f"\nBefore vs after capital gains tax ({a.tax_rate:g}%"
              + (f", {a.short_term_tax_rate:g}% if held < 1 year" if a.short_term_tax_rate is not None else "")
              + "). The strategies pay tax at every switch; the index only pays once, when you sell at the end.")
        print(tabulate(taxcmp_fmt, headers="keys", tablefmt="rounded_outline"))
    print("\nCalendar-year returns")
    print(tabulate((yearly * 100).round(1), headers="keys", tablefmt="simple", floatfmt="+.1f"))

    summary.to_csv(out / "summary.csv")
    yearly.to_csv(out / "yearly_returns.csv")
    time_held(bt).to_csv(out / "time_in_each_company.csv")
    leader_history(bt).to_csv(out / "leader_changes.csv", index=False)
    bt.equity.to_csv(out / "equity_curves.csv")
    md = [f"# {bt.index.name} — always own the #1 company vs the index\n",
          f"Period: {bt.equity.index[0]:%Y-%m-%d} to {bt.equity.index[-1]:%Y-%m-%d}. "
          f"Start capital {bt.capital:,.0f} {bt.index.currency}. Benchmark: {bt.index.benchmark_name}. "
          f"Capital gains tax: {a.tax_rate:g}%"
          + (f" ({a.short_term_tax_rate:g}% if held under a year)" if a.short_term_tax_rate is not None else "")
          + ".\n",
          "## Summary\n", shown.to_markdown(),
          *(["\n## Before vs after capital gains tax\n", taxcmp_fmt.to_markdown()] if taxcmp is not None else []), "\n## Calendar-year returns (%)\n",
          (yearly * 100).round(1).to_markdown(), "\n## Share of time in each company\n",
          (time_held(bt) * 100).round(1).to_markdown()]
    for r in bt.results:
        hp = holding_periods(r, bt.benchmark, bt.names())
        hp.to_csv(out / f"holdings_{slug(r.config.name)}.csv", index=False)
        r.trades.to_csv(out / f"trades_{slug(r.config.name)}.csv", index=False)
        if r.config.kind == "patient":
            md += [f"\n## Holding periods — {r.config.name}\n",
                   hp.assign(**{c: (hp[c] * 100).round(1) for c in ("Return", "Index return", "Excess")}).to_markdown(index=False)]
    md += ["\n## Data notes\n", bt.md.quality.to_markdown()]
    (out / "report.md").write_text("\n".join(md))

    plots.dashboard(bt, out / "dashboard.png")
    plots.save_individual(bt, out)
    print(f"Rendering animation -> {out / 'race.gif'}")
    plots.animate(bt, out_path=out / "race.gif", show=not a.no_show)
    print(f"Saved tables, charts and report to {out}")


def main(argv=None):
    p = argparse.ArgumentParser(description="Backtest 'always own the most valuable company' against an index.")
    p.add_argument("--index", choices=list(INDICES), help="index to test (omit for a menu)")
    p.add_argument("--all", action="store_true", help="run every index")
    p.add_argument("--years", type=float, default=20, help="how many years back to start (ignored if --start)")
    p.add_argument("--start", default=None, help="start date, e.g. 2008-01-01")
    p.add_argument("--end", default=None)
    p.add_argument("--capital", type=float, default=10_000)
    p.add_argument("--confirm-days", type=int, nargs="+", default=[7, 30],
                   help="patient model: days the new #1 must stay #1 before you switch (one model per value)")
    p.add_argument("--min-age-days", type=int, default=365, help="patient model: IPO maturity period")
    p.add_argument("--drop-rank", type=int, default=3, help="patient model: sell immediately if holding falls to this rank")
    p.add_argument("--cost-bps", type=float, default=10, help="patient model: cost per switch in basis points")
    p.add_argument("--naive-cost-bps", type=float, default=0, help="naive model: cost per switch (default ignores costs)")
    p.add_argument("--tax-rate", type=float, default=0,
                   help="capital gains tax %% charged on each switch's realised gain (e.g. 20)")
    p.add_argument("--short-term-tax-rate", type=float, default=None,
                   help="US-style rate %% for gains on positions held under a year (e.g. 37)")
    p.add_argument("--out", default="results", help="output folder")
    p.add_argument("--no-show", action="store_true", help="don't open the animation window (still saves the GIF)")
    p.add_argument("--offline", action="store_true", help="use cached data only")
    a = p.parse_args(argv)
    if a.start is None:
        a.start = str((pd.Timestamp.today().normalize() - pd.DateOffset(days=round(a.years * 365.25))).date())

    if a.no_show:
        import matplotlib
        matplotlib.use("Agg")
    keys = list(INDICES) if a.all else [a.index or choose_index()]
    for k in keys:
        run_one(k, a)


if __name__ == "__main__":
    pd.set_option("display.width", 200)
    sys.exit(main())
