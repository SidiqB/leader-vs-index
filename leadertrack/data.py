"""Market data: prices, share counts and historical market caps.

Market cap on day d = (unadjusted price on d) x (shares outstanding on d).

* Prices, dividends and splits come from Yahoo Finance (via ``yfinance``). Total
  return (dividends reinvested) is rebuilt from Close + Dividends.
* Share counts come from Yahoo (roughly 2015 onwards) spliced onto SEC EDGAR XBRL
  filings (roughly 2007 onwards, US filers only). Before the first known share count
  the earliest value is carried backwards, which is an approximation.
* Each company's series is finally calibrated so today's value matches Yahoo's quoted
  market cap. That fixes multi-share-class companies (Alphabet, Berkshire) whose
  share count on one ticker understates the whole company.

Everything is cached under ``data_cache/`` so repeat runs are fast and work offline.
"""

from __future__ import annotations

import json
import logging
import os
import pickle
import time
import warnings
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
import requests

from .indices import IndexDef

warnings.filterwarnings("ignore", module="yfinance")
warnings.filterwarnings("ignore", category=FutureWarning)
logging.getLogger("yfinance").setLevel(logging.CRITICAL)

CACHE_DIR = Path(os.environ.get("LEADERTRACK_CACHE", Path(__file__).resolve().parent.parent / "data_cache"))
CACHE_TTL_SECONDS = 24 * 3600
HISTORY_START = "1995-01-01"
SEC_USER_AGENT = os.environ.get("SEC_USER_AGENT", "leader-vs-index research script admin@example.org")


@dataclass
class MarketData:
    close: pd.DataFrame  # split-adjusted close, used for market caps
    total_return: pd.DataFrame  # dividend + split adjusted close, used for performance
    market_cap: pd.DataFrame  # estimated market cap per company
    benchmark: pd.Series  # benchmark total-return price
    first_trade: dict[str, pd.Timestamp]  # first day each stock traded (for IPO maturity)
    quality: pd.DataFrame  # per-company notes on share-count coverage


# ---------------------------------------------------------------- caching helpers
def _cache_path(name: str) -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    return CACHE_DIR / name.replace("^", "IDX_").replace("/", "_")


def _cached(name: str, fetch, ttl: float | None = CACHE_TTL_SECONDS, offline: bool = False):
    path = _cache_path(name)
    if path.exists() and (offline or ttl is None or time.time() - path.stat().st_mtime < ttl):
        with open(path, "rb") as f:
            return pickle.load(f)
    try:
        value = fetch()
    except Exception as exc:  # network trouble: fall back to a stale cache if we have one
        if path.exists():
            logging.warning("Using stale cache for %s (%s)", name, exc)
            with open(path, "rb") as f:
                return pickle.load(f)
        raise
    with open(path, "wb") as f:
        pickle.dump(value, f)
    return value


# ---------------------------------------------------------------- prices
def _download_prices(ticker: str) -> pd.DataFrame:
    import yfinance as yf

    df = yf.Ticker(ticker).history(start=HISTORY_START, auto_adjust=False, actions=True)
    if df.empty:
        raise RuntimeError(f"No price data for {ticker}")
    df.index = pd.to_datetime(df.index).tz_localize(None).normalize()
    df = df[~df.index.duplicated(keep="last")]
    # Yahoo's own "Adj Close" misses many dividends on non-US listings (e.g. London),
    # so build the dividends-reinvested series ourselves from Close + Dividends.
    df["Total Return"] = ((df["Close"] + df["Dividends"]) / df["Close"].shift()).fillna(1.0).cumprod()
    return df[["Close", "Total Return", "Dividends", "Stock Splits"]]


def load_prices(ticker: str, offline: bool = False) -> pd.DataFrame:
    return _cached(f"{ticker}_prices.pkl", lambda: _download_prices(ticker), offline=offline)


# ---------------------------------------------------------------- share counts
def _sec_cik_map() -> dict[str, int]:
    r = requests.get("https://www.sec.gov/files/company_tickers.json", headers={"User-Agent": SEC_USER_AGENT}, timeout=30)
    r.raise_for_status()
    return {v["ticker"].upper(): int(v["cik_str"]) for v in r.json().values()}


# Tickers whose SEC history lives under other/older registrants (holding-company
# reorganisations, Google Inc -> Alphabet Inc, ...). Oldest first.
SEC_CIK_OVERRIDES: dict[str, list[int]] = {
    "XOM": [34088],
    "GOOGL": [1288776, 1652044],
    "META": [1326801],
    "BRK-B": [],  # SEC reports Class-A equivalents mixed with B shares; Yahoo only
}

_SEC_CONCEPTS = [
    ("us-gaap", "WeightedAverageNumberOfSharesOutstandingBasic"),
    ("dei", "EntityCommonStockSharesOutstanding"),
    ("us-gaap", "CommonStockSharesOutstanding"),
]


def _sec_company_shares(cik: int) -> pd.Series:
    def fetch():
        url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"
        r = requests.get(url, headers={"User-Agent": SEC_USER_AGENT}, timeout=60)
        r.raise_for_status()
        return r.json()

    facts = _cached(f"sec_{cik}.pkl", fetch, ttl=30 * 24 * 3600)
    best = pd.Series(dtype=float)
    for ns, concept in _SEC_CONCEPTS:
        rows = facts.get("facts", {}).get(ns, {}).get(concept, {}).get("units", {}).get("shares", [])
        if len(rows) < 4:
            continue
        df = pd.DataFrame(rows)
        df["end"] = pd.to_datetime(df["end"])
        df = df.sort_values("filed").drop_duplicates("end", keep="last").sort_values("end")
        ser = df.set_index("end")["val"].astype(float)
        ser = ser[ser > 0]
        # Prefer whichever concept reaches furthest back in time.
        if len(ser) >= 4 and (best.empty or ser.index[0] < best.index[0] - pd.Timedelta(days=365)):
            best = ser
    return best


def _sec_shares(ticker: str) -> pd.Series:
    """Shares outstanding from SEC XBRL company facts (raw, as reported at the time)."""
    ciks = SEC_CIK_OVERRIDES.get(ticker.upper())
    if ciks is None:
        cik_map = _cached("sec_cik_map.pkl", _sec_cik_map, ttl=30 * 24 * 3600)
        cik = cik_map.get(ticker.upper())
        ciks = [cik] if cik else []
    parts = [p for p in (_sec_company_shares(c) for c in ciks) if len(p)]
    if not parts:
        return pd.Series(dtype=float)
    out = pd.concat(parts).sort_index()
    return out[~out.index.duplicated(keep="last")]


def _yahoo_shares(ticker: str) -> pd.Series:
    import yfinance as yf

    s = yf.Ticker(ticker).get_shares_full(start="2000-01-01")
    if s is None or len(s) == 0:
        return pd.Series(dtype=float)
    s = s.astype(float)
    s.index = pd.to_datetime(s.index).tz_localize(None).normalize()
    s = s[~s.index.duplicated(keep="last")].sort_index()
    return s[s > 0]


def _yahoo_market_cap(ticker: str) -> float | None:
    import yfinance as yf

    try:
        mc = yf.Ticker(ticker).info.get("marketCap")
        return float(mc) if mc else None
    except Exception:
        return None


def _despike(s: pd.Series, window: int = 7) -> pd.Series:
    """Share-count feeds contain occasional bad prints (e.g. 10x off); drop them."""
    if len(s) < 3:
        return s
    med = s.rolling(window, center=True, min_periods=1).median()
    ok = (s / med).between(0.85, 1.15)
    return s[ok]


def _split_factor_after(splits: pd.Series, dates: pd.DatetimeIndex) -> pd.Series:
    """For each date, the product of all stock splits that happen *after* it."""
    splits = splits[splits > 0]
    out = pd.Series(1.0, index=dates)
    for d, ratio in splits.items():
        out[out.index < d] *= ratio
    return out


def shares_history(ticker: str, prices: pd.DataFrame, offline: bool = False) -> tuple[pd.Series, str]:
    """Daily share count on a *split-adjusted* basis (matches the split-adjusted Close).

    Returns the series plus a short note on where the data came from.
    """
    yahoo = _cached(f"{ticker}_shares_yahoo.pkl", lambda: _yahoo_shares(ticker), offline=offline)
    try:
        sec = _sec_shares(ticker) if "." not in ticker else pd.Series(dtype=float)
    except Exception as exc:
        logging.warning("SEC lookup failed for %s: %s", ticker, exc)
        sec = pd.Series(dtype=float)

    splits = prices["Stock Splits"]
    idx = prices.index

    def to_adjusted(raw: pd.Series) -> pd.Series:
        raw = raw[~raw.index.duplicated(keep="last")].sort_index()
        # De-spike on the split-adjusted basis: share counts reported a few days
        # early/late around a split show up as jumps of exactly the split ratio.
        return _despike(raw * _split_factor_after(splits, pd.DatetimeIndex(raw.index)).values)

    parts = []
    note = []
    if len(yahoo):
        y_adj = to_adjusted(yahoo)
        parts.append(y_adj)
        note.append(f"Yahoo from {y_adj.index[0]:%Y}")
    if len(sec):
        s_adj = to_adjusted(sec)
        if parts:
            y_adj = parts[0]
            overlap = s_adj[s_adj.index >= y_adj.index[0]]
            if len(overlap):
                y_at = y_adj.reindex(y_adj.index.union(overlap.index)).ffill().bfill().reindex(overlap.index)
                ratio = float(np.nanmedian(y_at.values / overlap.values))
                if np.isfinite(ratio) and 0.2 < ratio < 5:
                    s_adj = s_adj * ratio
                else:  # SEC and Yahoo count different things (e.g. Class A equivalents)
                    s_adj = s_adj.iloc[0:0]
            s_adj = s_adj[s_adj.index < y_adj.index[0]]
            # The two sources must join up smoothly, otherwise ignore SEC.
            if len(s_adj) and not 0.8 < y_adj.iloc[0] / s_adj.iloc[-1] < 1.25:
                s_adj = s_adj.iloc[0:0]
        if len(s_adj):
            parts.insert(0, s_adj)
            note.insert(0, f"SEC from {s_adj.index[0]:%Y}")

    if not parts:
        return pd.Series(np.nan, index=idx), "no share data"

    combined = pd.concat(parts).sort_index()
    combined = combined[~combined.index.duplicated(keep="last")]
    daily = combined.reindex(idx.union(combined.index)).ffill().reindex(idx)
    first_known = combined.index[0]
    daily = daily.bfill()  # carry earliest known count backwards (approximation)
    return daily, " + ".join(note) + (f"; back-filled before {first_known:%Y}" if first_known > idx[0] else "")


# ---------------------------------------------------------------- top level
def load_market_data(index: IndexDef, offline: bool = False, progress=None) -> MarketData:
    tickers = [m.ticker for m in index.members]
    close, tr, caps, first_trade, quality = {}, {}, {}, {}, []

    for n, t in enumerate(tickers, 1):
        if progress:
            progress(n / (len(tickers) + 1), f"Loading {t}")
        try:
            px = load_prices(t, offline=offline)
        except Exception as exc:
            logging.warning("Skipping %s: %s", t, exc)
            quality.append({"ticker": t, "shares": "skipped: no price data", "calibration": np.nan})
            continue
        shares, note = shares_history(t, px, offline=offline)
        mc = px["Close"] * shares
        live_cap = _cached(f"{t}_mcap.pkl", lambda: _yahoo_market_cap(t), offline=offline)
        scale = 1.0
        if live_cap and mc.dropna().size:
            scale = live_cap / float(mc.dropna().iloc[-1])
            if not 0.2 < scale < 5:  # something is badly off; don't trust it
                scale = 1.0
        close[t], tr[t], caps[t] = px["Close"], px["Total Return"], mc * scale
        first_trade[t] = px["Close"].first_valid_index()
        quality.append({"ticker": t, "shares": note, "calibration": round(scale, 3)})

    if progress:
        progress(1.0, f"Loading benchmark {index.benchmark}")
    bench = load_prices(index.benchmark, offline=offline)["Total Return"]

    close_df = pd.DataFrame(close).sort_index()
    cal = close_df.index.intersection(bench.index)
    return MarketData(
        close=close_df.reindex(cal),
        total_return=pd.DataFrame(tr).reindex(cal),
        market_cap=pd.DataFrame(caps).reindex(cal),
        benchmark=bench.reindex(cal),
        first_trade=first_trade,
        quality=pd.DataFrame(quality).set_index("ticker"),
    )


def save_json(obj, path: Path) -> None:
    path.write_text(json.dumps(obj, indent=2, default=str))
