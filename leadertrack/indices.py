"""Index definitions.

Each index has a benchmark (an ETF or total-return index to compare against) and a
pool of candidate companies: every company that has realistically been, or come close
to being, the index's largest member over the period we can backtest.

Membership windows matter: a company can only be "the most valuable company in the
index" while it is actually in the index (Apple only joined the Dow in 2015, Tesla
only joined the S&P 500 in December 2020, and so on). Dates are approximate join /
leave dates; ``None`` means "for the whole backtest window".
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Member:
    ticker: str
    name: str
    joined: str | None = None
    left: str | None = None


@dataclass(frozen=True)
class IndexDef:
    key: str
    name: str
    benchmark: str
    benchmark_name: str
    currency: str
    members: tuple[Member, ...]
    note: str = ""
    # Pools of large non-US companies rarely have SEC filings, so share counts
    # before ~2015 are back-filled. Shown as a warning in reports.
    us_listed: bool = True
    tags: tuple[str, ...] = field(default_factory=tuple)


SP500 = IndexDef(
    key="sp500",
    name="S&P 500",
    benchmark="SPY",
    benchmark_name="SPDR S&P 500 ETF (SPY)",
    currency="USD",
    members=(
        Member("MSFT", "Microsoft"),
        Member("AAPL", "Apple"),
        Member("XOM", "Exxon Mobil"),
        Member("GE", "General Electric"),
        Member("WMT", "Walmart"),
        Member("C", "Citigroup"),
        Member("JNJ", "Johnson & Johnson"),
        Member("PG", "Procter & Gamble"),
        Member("IBM", "IBM"),
        Member("JPM", "JPMorgan Chase"),
        Member("CVX", "Chevron"),
        Member("BAC", "Bank of America"),
        Member("PFE", "Pfizer"),
        Member("INTC", "Intel"),
        Member("CSCO", "Cisco"),
        Member("ORCL", "Oracle"),
        Member("LLY", "Eli Lilly"),
        Member("NVDA", "Nvidia", joined="2001-11-30"),
        Member("AMZN", "Amazon", joined="2005-11-18"),
        Member("GOOGL", "Alphabet", joined="2006-03-31"),
        Member("V", "Visa", joined="2009-12-21"),
        Member("BRK-B", "Berkshire Hathaway", joined="2010-02-16"),
        Member("META", "Meta Platforms", joined="2013-12-23"),
        Member("AVGO", "Broadcom", joined="2014-05-08"),
        Member("TSLA", "Tesla", joined="2020-12-21"),
    ),
    tags=("US", "market-cap weighted"),
)

NASDAQ100 = IndexDef(
    key="nasdaq100",
    name="Nasdaq-100",
    benchmark="QQQ",
    benchmark_name="Invesco QQQ Trust (QQQ)",
    currency="USD",
    members=(
        Member("MSFT", "Microsoft"),
        Member("AAPL", "Apple"),
        Member("CSCO", "Cisco"),
        Member("INTC", "Intel"),
        Member("QCOM", "Qualcomm"),
        Member("ORCL", "Oracle", left="2013-07-15"),
        Member("AMZN", "Amazon"),
        Member("COST", "Costco"),
        Member("NVDA", "Nvidia"),
        Member("GOOGL", "Alphabet", joined="2005-07-18"),
        Member("META", "Meta Platforms", joined="2013-12-23"),
        Member("TSLA", "Tesla", joined="2013-07-15"),
        Member("AVGO", "Broadcom", joined="2009-12-21"),
        Member("NFLX", "Netflix", joined="2010-12-20"),
    ),
    tags=("US", "tech-heavy"),
)

DOW30 = IndexDef(
    key="dow30",
    name="Dow Jones Industrial Average",
    benchmark="DIA",
    benchmark_name="SPDR Dow Jones Industrial Average ETF (DIA)",
    currency="USD",
    note="The Dow itself is price-weighted; here 'most valuable' still means largest market cap among its members.",
    members=(
        Member("MSFT", "Microsoft"),
        Member("XOM", "Exxon Mobil", left="2020-08-31"),
        Member("GE", "General Electric", left="2018-06-26"),
        Member("WMT", "Walmart"),
        Member("JNJ", "Johnson & Johnson"),
        Member("IBM", "IBM"),
        Member("PG", "Procter & Gamble"),
        Member("JPM", "JPMorgan Chase"),
        Member("KO", "Coca-Cola"),
        Member("C", "Citigroup", left="2009-06-08"),
        Member("INTC", "Intel", left="2024-11-08"),
        Member("PFE", "Pfizer", joined="2004-04-08", left="2020-08-31"),
        Member("CVX", "Chevron", joined="2008-02-19"),
        Member("CSCO", "Cisco", joined="2009-06-08"),
        Member("V", "Visa", joined="2013-09-23"),
        Member("AAPL", "Apple", joined="2015-03-19"),
        Member("AMZN", "Amazon", joined="2024-02-26"),
        Member("NVDA", "Nvidia", joined="2024-11-08"),
    ),
    tags=("US", "price weighted"),
)

FTSE100 = IndexDef(
    key="ftse100",
    name="FTSE 100",
    benchmark="ISF.L",
    benchmark_name="iShares Core FTSE 100 ETF (ISF.L)",
    currency="GBP",
    us_listed=False,
    members=(
        Member("SHEL.L", "Shell"),
        Member("BP.L", "BP"),
        Member("HSBA.L", "HSBC"),
        Member("AZN.L", "AstraZeneca"),
        Member("ULVR.L", "Unilever"),
        Member("GSK.L", "GSK"),
        Member("VOD.L", "Vodafone"),
        Member("RIO.L", "Rio Tinto"),
        Member("BATS.L", "British American Tobacco"),
        Member("DGE.L", "Diageo"),
        Member("LSEG.L", "London Stock Exchange Group"),
    ),
    tags=("UK",),
)

DAX40 = IndexDef(
    key="dax",
    name="DAX",
    benchmark="^GDAXI",
    benchmark_name="DAX performance index (^GDAXI, dividends reinvested)",
    currency="EUR",
    us_listed=False,
    members=(
        Member("SAP.DE", "SAP"),
        Member("SIE.DE", "Siemens"),
        Member("ALV.DE", "Allianz"),
        Member("DTE.DE", "Deutsche Telekom"),
        Member("MBG.DE", "Mercedes-Benz"),
        Member("VOW3.DE", "Volkswagen"),
        Member("BAS.DE", "BASF"),
        Member("BAYN.DE", "Bayer"),
        Member("MUV2.DE", "Munich Re"),
        Member("LIN.DE", "Linde", joined="2018-10-31", left="2023-02-27"),
        Member("AIR.DE", "Airbus", joined="2021-09-20"),
        Member("RHM.DE", "Rheinmetall", joined="2023-03-20"),
    ),
    tags=("Germany",),
)

INDICES: dict[str, IndexDef] = {i.key: i for i in (SP500, NASDAQ100, DOW30, FTSE100, DAX40)}


def get_index(key: str) -> IndexDef:
    try:
        return INDICES[key]
    except KeyError:
        raise SystemExit(f"Unknown index '{key}'. Choose from: {', '.join(INDICES)}") from None
