"""Strategy rules on small synthetic markets (no network needed)."""

import numpy as np
import pandas as pd

from leadertrack.data import MarketData
from leadertrack.indices import IndexDef, Member
from leadertrack.strategies import StrategyConfig, run_strategy

IDX = IndexDef("t", "Test", "BENCH", "bench", "USD", (Member("A", "A"), Member("B", "B"), Member("C", "C")))


def make_md(caps: dict[str, list[float]], first_trade: dict | None = None) -> MarketData:
    dates = pd.bdate_range("2020-01-01", periods=len(next(iter(caps.values()))))
    mc = pd.DataFrame(caps, index=dates)
    tr = pd.DataFrame(1.0, index=dates, columns=mc.columns)
    return MarketData(close=tr, total_return=tr, market_cap=mc, benchmark=tr.iloc[:, 0],
                      first_trade=first_trade or {t: dates[0] - pd.Timedelta(days=3650) for t in mc},
                      quality=pd.DataFrame())


def held(cfg, md):
    return run_strategy(cfg, IDX, md, str(md.market_cap.index[0].date())).holding.tolist()


NAIVE = StrategyConfig("n", kind="naive")
PATIENT = StrategyConfig("p", kind="patient", confirm_days=7)


def test_naive_flips_every_time():
    # A and B swap #1 every day
    md = make_md({"A": [10, 9, 10, 9], "B": [9, 10, 9, 10], "C": [1, 1, 1, 1]})
    assert held(NAIVE, md) == ["A", "B", "A", "B"]


def test_patient_ignores_short_swaps_at_rank_2():
    md = make_md({"A": [10, 9, 10, 9], "B": [9, 10, 9, 10], "C": [1, 1, 1, 1]})
    assert held(PATIENT, md) == ["A"] * 4


def test_patient_switches_after_confirmation_period():
    n = 15
    a = [10] * 2 + [9] * (n - 2)
    b = [9] * 2 + [10] * (n - 2)
    md = make_md({"A": a, "B": b, "C": [1] * n})
    h = held(PATIENT, md)
    first_b = h.index("B")
    days = (md.market_cap.index[first_b] - md.market_cap.index[2]).days
    assert days >= 7 and h[first_b - 1] == "A"


def test_patient_sells_immediately_at_rank_3():
    md = make_md({"A": [10, 5, 5], "B": [9, 10, 10], "C": [8, 9, 9]})
    assert held(PATIENT, md) == ["A", "B", "B"]


def test_young_ipo_is_ignored():
    md = make_md({"A": [10] * 3, "B": [9] * 3, "C": [50] * 3})
    md.first_trade["C"] = md.market_cap.index[0]
    cfg = StrategyConfig("p", kind="patient", confirm_days=7, min_age_days=365)
    assert held(cfg, md) == ["A"] * 3
    assert held(NAIVE, md) == ["C"] * 3


def test_costs_reduce_value():
    md = make_md({"A": [10, 9, 10, 9], "B": [9, 10, 9, 10], "C": [1, 1, 1, 1]})
    r = run_strategy(StrategyConfig("n", kind="naive", cost_bps=10), IDX, md, "2020-01-01")
    assert np.isclose(r.equity.iloc[-1], 10_000 * (1 - 0.0005) * (1 - 0.001) ** 3)
