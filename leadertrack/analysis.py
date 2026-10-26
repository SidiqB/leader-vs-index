"""Backtest orchestration, performance metrics and result tables."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from .data import MarketData, load_market_data
from .indices import IndexDef, get_index
from .strategies import (DEFAULT_STRATEGIES, StrategyConfig, StrategyResult, TaxConfig, TaxLedger,
                         benchmark_equity, run_strategy)

TRADING_DAYS = 252


@dataclass
class Backtest:
    index: IndexDef
    md: MarketData
    start: str
    end: str | None
    capital: float
    benchmark: pd.Series
    results: list[StrategyResult]
    tax: TaxConfig = TaxConfig()
    monthly: float = 0.0
    bench_flows: pd.Series | None = None

    @property
    def equity(self) -> pd.DataFrame:
        """Money in the account (includes monthly contributions)."""
        df = pd.concat([r.equity for r in self.results], axis=1)
        df[self.index.name + " (index)"] = self.benchmark
        return df.dropna()

    @property
    def nav(self) -> pd.DataFrame:
        """Growth of one unit: pure performance, unaffected by contributions."""
        df = pd.concat([r.nav for r in self.results], axis=1)
        b = self.md.benchmark.reindex(self.benchmark.index).ffill()
        df[self.benchmark_label] = b / b.iloc[0]
        return df.dropna()

    def flows(self, col: str) -> pd.Series:
        res = next((r for r in self.results if r.config.name == col), None)
        return res.flows if res is not None else self.bench_flows

    def paid_in(self) -> float:
        return float(self.bench_flows.sum())

    @property
    def benchmark_label(self) -> str:
        return self.index.name + " (index)"

    def names(self) -> dict[str, str]:
        return {m.ticker: m.name for m in self.index.members}


def run_backtest(index_key: str, start: str = "2008-01-01", end: str | None = None, capital: float = 10_000.0,
                 strategies: tuple[StrategyConfig, ...] = DEFAULT_STRATEGIES, offline: bool = False,
                 progress=None, md: MarketData | None = None, tax: TaxConfig = TaxConfig(),
                 monthly: float = 0.0) -> Backtest:
    index = get_index(index_key)
    md = md or load_market_data(index, offline=offline, progress=progress)
    start = str(max(pd.Timestamp(start), md.market_cap.dropna(how="all").index[0]).date())
    results = [run_strategy(cfg, index, md, start, end, capital, tax, monthly) for cfg in strategies]
    bench, bench_flows = benchmark_equity(md, start, end, capital, monthly)
    return Backtest(index, md, start, end, capital, bench, results, tax, monthly, bench_flows)


def xirr(flows: pd.Series, final_value: float) -> float:
    """Money-weighted annual return: the rate that turns the deposits into the final value."""
    cf = flows[flows != 0]
    t = (cf.index - cf.index[0]).days.to_numpy() / 365.25
    T = (flows.index[-1] - cf.index[0]).days / 365.25
    amounts = cf.to_numpy()

    def gap(r):
        return final_value - float(np.sum(amounts * (1 + r) ** (T - t)))

    lo, hi = -0.99, 10.0
    if gap(lo) * gap(hi) > 0:
        return np.nan
    for _ in range(200):
        mid = (lo + hi) / 2
        if gap(lo) * gap(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


# ---------------------------------------------------------------- metrics
def max_drawdown(eq: pd.Series) -> float:
    return float((eq / eq.cummax() - 1).min())


def metrics(eq: pd.Series) -> dict:
    eq = eq.dropna()
    years = (eq.index[-1] - eq.index[0]).days / 365.25
    daily = eq.pct_change().dropna()
    cagr = (eq.iloc[-1] / eq.iloc[0]) ** (1 / years) - 1 if years > 0 else np.nan
    vol = daily.std() * np.sqrt(TRADING_DAYS)
    downside = daily[daily < 0].std() * np.sqrt(TRADING_DAYS)
    yearly = eq.resample("YE").last().pct_change()
    yearly.iloc[0] = eq.resample("YE").last().iloc[0] / eq.iloc[0] - 1
    mdd = max_drawdown(eq)
    return {
        "Total return": eq.iloc[-1] / eq.iloc[0] - 1,
        "CAGR": cagr,
        "Volatility": vol,
        "Sharpe (rf=0)": (daily.mean() * TRADING_DAYS) / vol if vol else np.nan,
        "Sortino": (daily.mean() * TRADING_DAYS) / downside if downside else np.nan,
        "Max drawdown": mdd,
        "Calmar": cagr / abs(mdd) if mdd else np.nan,
        "Best year": yearly.max(),
        "Worst year": yearly.min(),
    }


def summary_table(bt: Backtest) -> pd.DataFrame:
    """One row per strategy plus the index.

    Return/risk statistics (CAGR, volatility, drawdown...) use the unit value, so they
    measure the strategy itself. "Final value", "Paid in" and the money-weighted
    returns describe what happens to *your* money, contributions included.
    """
    eq, nav = bt.equity, bt.nav
    rows = {}
    for col in eq.columns:
        m = metrics(nav[col])
        res = next((r for r in bt.results if r.config.name == col), None)
        flows = bt.flows(col).reindex(eq.index).fillna(0.0)
        final = float(eq[col].iloc[-1])
        m["Final value"] = final
        m["Paid in"] = float(flows.sum())
        m["Trades"] = len(res.trades) if res is not None else 1
        m["Distinct companies held"] = res.holding.dropna().nunique() if res is not None else np.nan
        if res is not None:
            m["Tax paid on switches"], exit_tax = res.tax_paid, res.exit_tax
        else:  # buy and hold: one sale at the very end, held long term
            m["Tax paid on switches"] = 0.0
            exit_tax = TaxLedger(bt.tax).preview(eq.index[-1], final - m["Paid in"], 10 ** 6)
        m["After-tax value if sold today"] = final - exit_tax
        m["Annual return on your money"] = xirr(flows, final)
        m["After-tax annual return"] = xirr(flows, m["After-tax value if sold today"])
        rows[col] = m
    df = pd.DataFrame(rows).T
    df["CAGR vs index"] = df["CAGR"] - df.loc[bt.benchmark_label, "CAGR"]
    df["Annual return vs index"] = (df["Annual return on your money"]
                                    - df.loc[bt.benchmark_label, "Annual return on your money"])
    df["After-tax annual return vs index"] = (df["After-tax annual return"]
                                              - df.loc[bt.benchmark_label, "After-tax annual return"])
    return df


def yearly_returns(bt: Backtest) -> pd.DataFrame:
    eq = bt.nav
    ye = eq.resample("YE").last()
    first = ye.iloc[[0]] / eq.iloc[0] - 1
    out = pd.concat([first, ye.pct_change().iloc[1:]])
    out.index = out.index.year
    out.index.name = "Year"
    return out


def holding_periods(res: StrategyResult, eq_bench: pd.Series, names: dict[str, str]) -> pd.DataFrame:
    """One row per stretch of time a single company was held."""
    h = res.holding.dropna()
    if h.empty:
        return pd.DataFrame()
    block = (h != h.shift()).cumsum()
    rows = []
    for _, seg in h.groupby(block):
        t = seg.iloc[0]
        s, e = seg.index[0], seg.index[-1]
        # value is measured close-to-close: bought at s close, sold at the close after e
        nxt = res.nav.index.get_indexer([e])[0] + 1
        e_eff = res.nav.index[min(nxt, len(res.nav) - 1)]
        strat = res.nav.loc[e_eff] / res.nav.loc[s] - 1
        bench = eq_bench.loc[e_eff] / eq_bench.loc[s] - 1
        rows.append({
            "Company": names.get(t, t), "Ticker": t, "From": s.date(), "To": e_eff.date(),
            "Days": (e_eff - s).days, "Return": strat, "Index return": bench, "Excess": strat - bench,
        })
    return pd.DataFrame(rows)


def leader_history(bt: Backtest) -> pd.DataFrame:
    """Every change of the #1 company (all members, no maturity filter)."""
    res = next((r for r in bt.results if r.config.kind == "naive"), bt.results[0])
    tr = res.trades
    names = bt.names()
    return pd.DataFrame({
        "Date": tr["date"].dt.date,
        "New #1": tr["bought"].map(lambda t: names.get(t, t)),
        "Previous #1": tr["sold"].map(lambda t: names.get(t, t) if isinstance(t, str) else "-"),
    })


def time_held(bt: Backtest) -> pd.DataFrame:
    """Share of the backtest each strategy spent in each company."""
    out = {}
    names = bt.names()
    for r in bt.results:
        out[r.config.name] = r.holding.dropna().map(lambda t: names.get(t, t)).value_counts(normalize=True)
    return pd.DataFrame(out).fillna(0).sort_values(bt.results[0].config.name, ascending=False)


def rolling_excess(bt: Backtest, window_days: int = TRADING_DAYS) -> pd.DataFrame:
    eq = bt.nav
    roll = eq.pct_change(window_days)
    return roll.drop(columns=[bt.benchmark_label]).sub(roll[bt.benchmark_label], axis=0).dropna(how="all")


def fmt_summary(df: pd.DataFrame, capital: float) -> pd.DataFrame:
    pct = ["Total return", "CAGR", "Volatility", "Max drawdown", "Best year", "Worst year", "CAGR vs index",
           "Annual return on your money", "Annual return vs index", "After-tax annual return",
           "After-tax annual return vs index"]
    out = df.copy().astype(object)
    for c in out.columns:
        if c in pct:
            out[c] = df[c].map(lambda v: f"{v:+.1%}" if c.endswith("vs index") else f"{v:.1%}")
        elif c in ("Final value", "Paid in", "Tax paid on switches", "After-tax value if sold today"):
            out[c] = df[c].map(lambda v: f"{v:,.0f}")
        elif c in ("Trades", "Distinct companies held"):
            out[c] = df[c].map(lambda v: "-" if pd.isna(v) else f"{int(v)}")
        else:
            out[c] = df[c].map(lambda v: f"{v:.2f}")
    return out


def tax_comparison(bt_taxed: Backtest, bt_untaxed: Backtest) -> pd.DataFrame:
    """Before vs after tax, side by side (same strategies, same data)."""
    pre, post = summary_table(bt_untaxed), summary_table(bt_taxed)
    out = pd.DataFrame({
        "Before tax: final value": pre["Final value"],
        "Before tax: annual return": pre["Annual return on your money"],
        "Tax paid on switches": post["Tax paid on switches"],
        "After tax: value if sold today": post["After-tax value if sold today"],
        "After tax: annual return": post["After-tax annual return"],
    })
    out["Lost to tax"] = 1 - out["After tax: value if sold today"] / out["Before tax: final value"]
    out["After tax: annual return vs index"] = post["After-tax annual return vs index"]
    return out


def realised_gains_by_tax_year(bt: Backtest) -> pd.DataFrame:
    """Net gains each strategy realised (sold at a profit) in each tax year."""
    df = pd.DataFrame({r.config.name: pd.Series(r.gains_by_tax_year, dtype=float) for r in bt.results})
    m, d = bt.tax.year_start.split("-")
    df.index = [f"{y}/{str(y + 1)[2:]}" if bt.tax.year_start != "01-01" else str(y) for y in df.index]
    df.index.name = "Tax year" + (f" (from {d}/{m})" if bt.tax.year_start != "01-01" else "")
    return df.fillna(0.0)
