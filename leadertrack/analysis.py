"""Backtest orchestration, performance metrics and result tables."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from .data import MarketData, load_market_data
from .indices import IndexDef, get_index
from .strategies import DEFAULT_STRATEGIES, StrategyConfig, StrategyResult, benchmark_equity, run_strategy

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

    @property
    def equity(self) -> pd.DataFrame:
        df = pd.concat([r.equity for r in self.results], axis=1)
        df[self.index.name + " (index)"] = self.benchmark
        return df.dropna()

    @property
    def benchmark_label(self) -> str:
        return self.index.name + " (index)"

    def names(self) -> dict[str, str]:
        return {m.ticker: m.name for m in self.index.members}


def run_backtest(index_key: str, start: str = "2008-01-01", end: str | None = None, capital: float = 10_000.0,
                 strategies: tuple[StrategyConfig, ...] = DEFAULT_STRATEGIES, offline: bool = False,
                 progress=None, md: MarketData | None = None) -> Backtest:
    index = get_index(index_key)
    md = md or load_market_data(index, offline=offline, progress=progress)
    start = str(max(pd.Timestamp(start), md.market_cap.dropna(how="all").index[0]).date())
    results = [run_strategy(cfg, index, md, start, end, capital) for cfg in strategies]
    bench = benchmark_equity(md, start, end, capital)
    return Backtest(index, md, start, end, capital, bench, results)


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
        "Final value": eq.iloc[-1],
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
    eq = bt.equity
    rows = {}
    for col in eq.columns:
        m = metrics(eq[col])
        res = next((r for r in bt.results if r.config.name == col), None)
        m["Trades"] = len(res.trades) if res is not None else 1
        m["Distinct companies held"] = res.holding.dropna().nunique() if res is not None else np.nan
        rows[col] = m
    df = pd.DataFrame(rows).T
    bench_cagr = df.loc[bt.benchmark_label, "CAGR"]
    df["CAGR vs index"] = df["CAGR"] - bench_cagr
    return df


def yearly_returns(bt: Backtest) -> pd.DataFrame:
    eq = bt.equity
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
        nxt = res.equity.index.get_indexer([e])[0] + 1
        e_eff = res.equity.index[min(nxt, len(res.equity) - 1)]
        strat = res.equity.loc[e_eff] / res.equity.loc[s] - 1
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
    eq = bt.equity
    roll = eq.pct_change(window_days)
    return roll.drop(columns=[bt.benchmark_label]).sub(roll[bt.benchmark_label], axis=0).dropna(how="all")


def fmt_summary(df: pd.DataFrame, capital: float) -> pd.DataFrame:
    pct = ["Total return", "CAGR", "Volatility", "Max drawdown", "Best year", "Worst year", "CAGR vs index"]
    out = df.copy().astype(object)
    for c in out.columns:
        if c in pct:
            out[c] = df[c].map(lambda v: f"{v:+.1%}" if c in ("CAGR vs index",) else f"{v:.1%}")
        elif c == "Final value":
            out[c] = df[c].map(lambda v: f"{v:,.0f}")
        elif c in ("Trades", "Distinct companies held"):
            out[c] = df[c].map(lambda v: "-" if pd.isna(v) else f"{int(v)}")
        else:
            out[c] = df[c].map(lambda v: f"{v:.2f}")
    return out
