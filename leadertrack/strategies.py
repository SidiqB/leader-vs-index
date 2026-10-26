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

Both models can also pay capital gains tax on every switch (see ``TaxConfig``). The
index is buy-and-hold, so it only owes tax once, when you finally sell.
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
    equity: pd.Series  # money in the account through time (includes money paid in)
    holding: pd.Series  # ticker held at the end of each day
    trades: pd.DataFrame  # one row per switch
    ranks_of_holding: pd.Series = field(default_factory=pd.Series)
    tax_paid: float = 0.0  # capital gains tax paid on switches along the way
    exit_tax: float = 0.0  # tax that would be due if you sold everything on the last day
    nav: pd.Series = field(default_factory=pd.Series)  # value of one unit: performance without the cash flows
    flows: pd.Series = field(default_factory=pd.Series)  # money paid in on each day (first day = starting money)
    gains_by_tax_year: dict = field(default_factory=dict)  # net realised gain per tax year


@dataclass(frozen=True)
class TaxConfig:
    """Capital gains tax on realised gains.

    Every switch is a sale, so any gain since you bought that company is taxed;
    the tax leaves the portfolio and stops compounding.

    * ``allowance``: tax-free gains per tax year (UK annual exempt amount: 3,000).
      Unused allowance is lost at the end of the year.
    * Net losses in a tax year are carried forward and only used to bring later
      years' gains down to the allowance (UK rules).
    * ``year_start`` ("MM-DD"): when the tax year begins (UK: "04-06").
    * Positions held less than ``short_term_days`` can be taxed at a different
      (US-style short-term) rate.
    """
    rate: float = 0.0
    short_term_rate: float | None = None
    short_term_days: int = 365
    allowance: float = 0.0
    year_start: str = "01-01"

    def rate_for(self, held_days: int) -> float:
        if self.short_term_rate is not None and held_days < self.short_term_days:
            return self.short_term_rate
        return self.rate

    @property
    def active(self) -> bool:
        return self.rate > 0 or bool(self.short_term_rate)


class TaxLedger:
    """Keeps track of one tax year's realised gains, the allowance and carried losses."""

    def __init__(self, tax: TaxConfig):
        self.tax = tax
        m, d = (int(x) for x in tax.year_start.split("-"))
        self._start = (m, d)
        self.year: int | None = None
        self.realised = 0.0  # net gains realised so far this tax year
        self.charged = 0.0  # tax charged so far this tax year
        self.carry = 0.0  # losses carried forward from earlier years
        self.by_year: dict[int, float] = {}  # net realised gain per tax year (for reports)

    def _tax_year(self, d: pd.Timestamp) -> int:
        return d.year if (d.month, d.day) >= self._start else d.year - 1

    def _roll(self, d: pd.Timestamp) -> None:
        y = self._tax_year(d)
        if self.year is None:
            self.year = y
        if y == self.year:
            return
        if self.realised < 0:
            self.carry -= self.realised
        elif self.realised > self.tax.allowance:
            self.carry -= min(self.carry, self.realised - self.tax.allowance)
        self.year, self.realised, self.charged = y, 0.0, 0.0

    def _taxable(self, net: float) -> float:
        over = net - self.tax.allowance
        return max(0.0, over - self.carry) if over > 0 else 0.0

    def realise(self, d: pd.Timestamp, gain: float, held_days: int) -> float:
        """Tax due because of this sale (negative = a later loss in the same year gives tax back)."""
        self._roll(d)
        before = self._taxable(self.realised)
        self.realised += gain
        self.by_year[self.year] = self.realised
        due = (self._taxable(self.realised) - before) * self.tax.rate_for(held_days)
        due = max(due, -self.charged)
        self.charged += due
        return due

    def preview(self, d: pd.Timestamp, gain: float, held_days: int) -> float:
        """Tax that a sale would cost, without recording it."""
        import copy
        return copy.deepcopy(self).realise(d, gain, held_days)


def contribution_days(dates: pd.DatetimeIndex) -> np.ndarray:
    """First trading day of each month, except the very first day of the backtest."""
    month = dates.to_period("M")
    first = np.r_[False, month[1:] != month[:-1]]
    return first


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
                 capital: float = 10_000.0, tax: TaxConfig = TaxConfig(), monthly: float = 0.0) -> StrategyResult:
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
    basis = 0.0  # cost basis of the current position
    bought_on: pd.Timestamp | None = None
    ledger = TaxLedger(tax)
    tax_paid = 0.0
    units = capital  # unit value starts at 1.0
    nav = np.empty(len(dates))
    flows = np.zeros(len(dates))
    flows[0] = capital
    pay_in = contribution_days(dates) if monthly else np.zeros(len(dates), dtype=bool)

    rank_vals = ranks.to_numpy()
    col = {t: i for i, t in enumerate(tickers)}
    ret_vals = rets.to_numpy()

    for i, d in enumerate(dates):
        # 1) earn today's return on what we held overnight
        if held is not None:
            value *= 1.0 + ret_vals[i, col[held]]
        if pay_in[i]:  # monthly contribution, buys more of whatever we hold
            units += monthly / (value / units)
            value += monthly
            flows[i] = monthly
            if held is not None:
                basis += monthly

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
            tax_due = 0.0
            if held is not None:
                value *= 1.0 - cost / 2  # selling cost
                tax_due = ledger.realise(d, value - basis, (d - bought_on).days)
                value -= tax_due
                tax_paid += tax_due
            value *= 1.0 - cost / 2  # buying cost
            trades.append({"date": d, "sold": held, "bought": target, "reason": reason, "tax_paid": tax_due,
                           "value_after": value})
            held, basis, bought_on = target, value, d

        equity[i] = value
        nav[i] = value / units
        holding.append(held)
        if held is not None:
            held_rank[i] = rank_vals[i, col[held]]

    return StrategyResult(
        config=cfg,
        equity=pd.Series(equity, index=dates, name=cfg.name),
        holding=pd.Series(holding, index=dates, name=cfg.name),
        trades=pd.DataFrame(trades, columns=["date", "sold", "bought", "reason", "tax_paid", "value_after"]),
        ranks_of_holding=pd.Series(held_rank, index=dates),
        tax_paid=tax_paid,
        exit_tax=ledger.preview(dates[-1], value - basis, (dates[-1] - bought_on).days) if held is not None else 0.0,
        nav=pd.Series(nav, index=dates, name=cfg.name),
        flows=pd.Series(flows, index=dates),
        gains_by_tax_year=dict(ledger.by_year),
    )


def benchmark_equity(md: MarketData, start: str, end: str | None = None, capital: float = 10_000.0,
                     monthly: float = 0.0) -> tuple[pd.Series, pd.Series]:
    """Buy-and-hold the index, adding ``monthly`` on the first trading day of each month.

    Returns (money in the account, money paid in per day)."""
    b = md.benchmark.loc[start:end].ffill().dropna()
    flows = pd.Series(0.0, index=b.index)
    flows.iloc[0] = capital
    if monthly:
        flows[contribution_days(b.index)] = monthly
    units = (flows / b).cumsum()
    return units * b, flows
