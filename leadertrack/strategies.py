"""The "always own the biggest company" strategies.

All decisions are made with information available at the close of day ``t`` and the
trade happens at that close, so the new holding earns day ``t+1``'s return onwards.
No look-ahead.

Two models:

* ``naive``   - whenever a different company becomes #1, sell everything and buy it.
                No maturity filter, transaction costs ignored by default.
* ``patient`` - the realistic version:
    - a company is only eligible once it has traded for ``min_age_days``
      (newly IPO'd companies have to "mature" first);
    - if your company slips to #2 you keep holding it; you only switch to the new #1
      once that company has been #1 continuously for ``confirm_days``
      (e.g. 7 = a week, 30 = a month), so constant swapping does not churn you;
    - if your company falls to #3 or lower (``drop_rank``), you sell straight away
      and buy the current #1;
    - optional transaction cost per switch (``cost_bps``).
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from .data import MarketData
from .indices import IndexDef


@dataclass(frozen=True)
class StrategyConfig:
    name: str
    kind: str = "naive"  # "naive" | "patient"
    min_age_days: int = 0
    confirm_days: int = 0
    drop_rank: int = 3
    cost_bps: float = 0.0  # cost charged on each switch (sell + buy), in basis points


DEFAULT_STRATEGIES = (
    StrategyConfig("Naive: always #1", kind="naive"),
    StrategyConfig("Patient: 1-week confirm", kind="patient", min_age_days=365, confirm_days=7, cost_bps=10),
    StrategyConfig("Patient: 1-month confirm", kind="patient", min_age_days=365, confirm_days=30, cost_bps=10),
)


@dataclass
class StrategyResult:
    config: StrategyConfig
    equity: pd.Series  # portfolio value through time
    holding: pd.Series  # ticker held at the end of each day
    trades: pd.DataFrame  # one row per switch
    ranks_of_holding: pd.Series = field(default_factory=pd.Series)


def membership_mask(index: IndexDef, dates: pd.DatetimeIndex, tickers: list[str]) -> pd.DataFrame:
    mask = pd.DataFrame(False, index=dates, columns=tickers)
    for m in index.members:
        if m.ticker not in mask:
            continue
        lo = pd.Timestamp(m.joined) if m.joined else dates[0]
        hi = pd.Timestamp(m.left) if m.left else dates[-1] + pd.Timedelta(days=1)
        mask.loc[(dates >= lo) & (dates < hi), m.ticker] = True
    return mask


def daily_ranks(caps: pd.DataFrame, eligible: pd.DataFrame) -> pd.DataFrame:
    """Rank 1 = most valuable eligible company that day; NaN if not eligible."""
    return caps.where(eligible).rank(axis=1, ascending=False, method="first")


def run_strategy(cfg: StrategyConfig, index: IndexDef, md: MarketData, start: str, end: str | None = None,
                 capital: float = 10_000.0) -> StrategyResult:
    caps = md.market_cap.loc[start:end]
    tr = md.total_return.loc[start:end]
    dates = caps.index
    tickers = list(caps.columns)

    eligible = membership_mask(index, dates, tickers) & caps.notna() & tr.notna()
    if cfg.min_age_days:
        for t in tickers:
            first = md.first_trade.get(t)
            if first is not None:
                eligible.loc[dates < first + pd.Timedelta(days=cfg.min_age_days), t] = False
    ranks = daily_ranks(caps, eligible)
    has_any = ranks.notna().any(axis=1)
    leader = pd.Series(None, index=dates, dtype=object)  # rank-1 ticker per day
    leader[has_any] = ranks[has_any].idxmin(axis=1)

    rets = tr.pct_change().fillna(0.0)
    cost = cfg.cost_bps / 1e4

    value = capital
    held: str | None = None
    lead_since: pd.Timestamp | None = None
    prev_leader: str | None = None
    equity = np.empty(len(dates))
    holding = []
    held_rank = np.full(len(dates), np.nan)
    trades = []

    rank_vals = ranks.to_numpy()
    col = {t: i for i, t in enumerate(tickers)}
    ret_vals = rets.to_numpy()

    for i, d in enumerate(dates):
        # 1) earn today's return on what we held overnight
        if held is not None:
            value *= 1.0 + ret_vals[i, col[held]]

        # 2) decide at today's close
        today_leader = leader.iloc[i]
        if not isinstance(today_leader, str):  # no eligible company today
            today_leader = None
        if today_leader != prev_leader:
            lead_since = d
            prev_leader = today_leader

        target = held
        reason = ""
        if today_leader is not None:
            if held is None:
                target, reason = today_leader, "initial buy"
            elif held != today_leader:
                r = rank_vals[i, col[held]]
                if cfg.kind == "naive":
                    target, reason = today_leader, "new #1"
                elif np.isnan(r):
                    target, reason = today_leader, "holding left the index"
                elif r >= cfg.drop_rank:
                    target, reason = today_leader, f"holding fell to #{int(r)}"
                elif (d - lead_since).days >= cfg.confirm_days:
                    target, reason = today_leader, f"new #1 for {(d - lead_since).days} days"

        if target != held:
            value *= 1.0 - (cost if held is not None else cost / 2)
            trades.append({"date": d, "sold": held, "bought": target, "reason": reason, "value_after": value})
            held = target

        equity[i] = value
        holding.append(held)
        if held is not None:
            held_rank[i] = rank_vals[i, col[held]]

    return StrategyResult(
        config=cfg,
        equity=pd.Series(equity, index=dates, name=cfg.name),
        holding=pd.Series(holding, index=dates, name=cfg.name),
        trades=pd.DataFrame(trades, columns=["date", "sold", "bought", "reason", "value_after"]),
        ranks_of_holding=pd.Series(held_rank, index=dates),
    )


def benchmark_equity(md: MarketData, start: str, end: str | None = None, capital: float = 10_000.0) -> pd.Series:
    b = md.benchmark.loc[start:end].ffill().dropna()
    return b / b.iloc[0] * capital
