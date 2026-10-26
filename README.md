# Leader vs Index

**What if, instead of buying the whole index, you only ever owned its single most valuable company, and switched every time a new company took the #1 spot?**

This project backtests that idea against five indices (S&P 500, Nasdaq-100, Dow Jones, FTSE 100, DAX), with an animated "race" chart, comparison charts and tables.

![S&P 500 race](results/sp500/race.gif)

## The two models

| | **Model 1: Naive** | **Model 2: Patient** |
|---|---|---|
| When to switch | The moment a different company becomes #1 | Only when the new #1 has been #1 for a **confirmation period** (default: one model at 7 days and one at 30) |
| If your company slips to #2 | Switch | **Keep holding** |
| If your company falls to #3 or lower | Switch | **Switch straight away** to the current #1 |
| New IPOs | Allowed straight away | Must have traded for **365 days** first |
| Transaction costs | Ignored (0 bps) | 10 bps per switch |

All of these are settings: `--confirm-days`, `--min-age-days`, `--drop-rank`, `--cost-bps`, `--naive-cost-bps` on the command line, or the sliders in the app.

Decisions are made at each day's close using that day's market caps, and the trade happens at that close, so there is no look-ahead. Returns include reinvested dividends for both the strategies and the index.

## Tax: why switching costs more than it looks

Every switch is a **sale**, so in a normal (taxable) account any gain since you bought that company is taxed right then. The tax leaves the portfolio and stops compounding. The index is buy-and-hold: it pays tax **once**, when you finally sell, and its gains compound untaxed until then.

The model handles this with `--tax-rate` (and the tax slider in the app):

* tax is charged on the realised gain at each switch;
* losses are carried forward and offset later gains;
* `--short-term-tax-rate` optionally taxes positions held under a year at a higher rate, as in the US (e.g. `--tax-rate 20 --short-term-tax-rate 37`);
* at the end everything is valued **as if sold today**, so the index pays its tax too and the comparison is fair.

With a tax rate of 0 the results are what you'd get in a tax-free account (ISA, IRA/401k).

## Results: 20 years (2006-10-26 → 2026-10-23), $10,000 start

Yearly growth rate (CAGR). The "after tax" rows use a flat 20% capital gains tax and assume you sell everything on the last day.

| Index | | Naive | Patient (1 week) | Patient (1 month) | **Index** |
|---|---|---|---|---|---|
| **S&P 500** | tax-free | 9.9% (121 trades) | 13.2% (27) | **14.8%** (11) | 10.9% |
| | after 20% tax | 7.9% | 10.9% | **12.3%** | 9.8% |
| **Nasdaq-100** | tax-free | 14.0% (70) | 16.6% (18) | **17.0%** (10) | 15.9% |
| | after 20% tax | 11.5% | 14.1% | 14.4% | **14.7%** |
| **Dow Jones** | tax-free | 7.3% (95) | 11.2% (19) | **11.3%** (11) | 10.0% |
| | after 20% tax | 5.7% | 9.1% | **9.3%** | 8.9% |
| **FTSE 100** *(from 2009)* | tax-free | 3.1% (81) | 4.1% (17) | 5.5% (7) | **7.8%** |
| | after 20% tax | 2.3% | 3.4% | 4.7% | **6.9%** |
| **DAX** | tax-free | 2.5% (114) | 0.4% (50) | −0.7% (39) | **7.2%** |
| | after 20% tax | 2.0% | 0.3% | −0.7% | **6.4%** |

What $10,000 became in the S&P 500:

| | Tax-free | After 20% tax, sold today | Lost to tax |
|---|---|---|---|
| Naive | $65,535 | $45,662 | 30% |
| Patient (1 week) | $118,216 | $78,797 | 33% |
| Patient (1 month) | $156,795 | $100,921 | 36% |
| S&P 500 index | $78,980 | $65,184 | 17% |

What the backtest shows:

* **Constant switching hurts.** The naive model lost to the index in every market, even with no costs or tax. The leaders kept trading places for days at a time (Apple, Microsoft and Nvidia in 2024–25, for example), and every switch came right after the new leader had risen and the old one had fallen, so it often bought just before the move reversed.
* **Patience helps.** Waiting a month before switching, and holding through a drop to #2, beat all three US indices tax-free: by 3.9 percentage points a year in the S&P 500, 1.4 in the Dow and 1.0 in the Nasdaq-100. Over 20 years in the S&P 500 that's $156,795 against $78,980, about twice as much. It spent 58% of the time in Apple and 24% in Exxon.
* **Tax takes a big bite.** At 20%, the patient strategies lost about a third of their final value to tax, against 17% for the index. The S&P 500 lead shrinks from 3.9 to 2.5 points a year, and the Nasdaq-100 lead disappears (14.4% against 14.7%). In a taxable account this strategy is much less attractive.
* **It's much riskier.** Volatility was about 30% a year against about 20% for the index, and Sharpe ratios were about the same or lower. The extra return came with a lot more ups and downs.
* **Outside the US it failed.** The FTSE's leaders (Shell, AstraZeneca) and the DAX's (E.ON, Volkswagen, Bayer, SAP) lagged their indices badly. German leaders were so close in size in 2008–09 that the strategy kept swapping between them through the crash.
* **The start date matters.** Starting in 2008 instead of 2006 gives different numbers (the S&P 500 patient lead was 3.4 points instead of 3.9), because a handful of switches decide most of the result.

Full tables are in `results/<index>/report.md` (tax-free) and `results_tax20/<index>/report.md` (20% tax, with a before/after table). Chart dashboards are in `dashboard.png` in each folder.

![S&P 500 dashboard](results/sp500/dashboard.png)

## Running it

```bash
git clone https://github.com/SidiqB/leader-vs-index.git
cd leader-vs-index
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

**Interactive app.** Pick any index from the dropdown and it re-runs on its own: the race chart plays, then the comparison charts and tables appear.

```bash
streamlit run app.py
```

**Command line.** Shows the animation in a window, prints the tables, and saves everything to `results/<index>/`.

```bash
python run.py                    # choose an index from a menu
python run.py --index nasdaq100  # or name it
python run.py --all --no-show    # every index, files only
python run.py --years 10                          # backtest length (default 20 years)
python run.py --index sp500 --start 2012-01-01 --confirm-days 14 60 --cost-bps 25
python run.py --tax-rate 20                       # 20% capital gains tax on every switch
python run.py --tax-rate 20 --short-term-tax-rate 37 --out results_us_tax
```

The first run downloads data (about 30 seconds per index). After that it is cached in `data_cache/` for a day; add `--offline` to use only the cache.

**Tests:** `pytest`

## Outputs per index

| File | What |
|---|---|
| `race.gif` | The animated chart |
| `dashboard.png` | Growth, drawdowns, rolling excess return, yearly returns, holdings timeline |
| `report.md` | All tables in one readable file |
| `tax_comparison.csv` | Before vs after tax side by side (only when `--tax-rate` is set) |
| `summary.csv` | Final value, CAGR, volatility, Sharpe, Sortino, max drawdown, trades… |
| `yearly_returns.csv` | Calendar-year returns of each strategy and the index |
| `holdings_*.csv` | Every period a company was held, its return and the index's return over the same period |
| `trades_*.csv` | Every switch, why it happened, and tax paid on it |
| `leader_changes.csv` | Every time the #1 company changed |
| `time_in_each_company.csv` | Share of time spent in each company |

## How it works

```
leadertrack/
  indices.py     index definitions: benchmark ETF + candidate companies with join/leave dates
  data.py        prices, dividends, share counts → historical market caps (cached)
  strategies.py  naive + patient models
  analysis.py    metrics and tables
  plots.py       matplotlib animation + static charts
app.py           Streamlit dashboard
run.py           command line
```

**Market cap** = unadjusted price × shares outstanding on that day. Share counts come from Yahoo Finance (about 2015 onwards) joined onto SEC EDGAR filings (about 2007 onwards, US companies only).

## Caveats

* **Share counts before about 2007 (US) or 2015 (UK/Germany) are estimates.** The buyback/issuance trend of the first known years is extended backwards (for up to 5 years), so when two companies were close, early rankings can be wrong. For example, the S&P 500 run may rank GE above Exxon for the first few months of the 20-year window. The app warns you when the start date is that early.
* **Candidate pools are hand-picked** (the 11–25 companies that realistically competed for #1), not the full historical membership. Join/leave dates are approximate. Add companies in `indices.py`.
* **Tax model is simplified:** a flat capital gains rate (optionally a short-term rate), no annual allowance, no tax on dividends (which would hit the index and the strategies roughly equally).
* **Dow note:** the Dow is price-weighted, but "most valuable" here still means largest market cap among its members.
* **FTSE:** Yahoo only has the FTSE 100 ETF (ISF.L) from 2009, so FTSE runs start there, and its dividends only from 2013, so the index return is slightly understated before then.
* **Spin-offs:** Yahoo prices are not adjusted for spin-offs (e.g. Siemens Energy from Siemens in 2020), so a holding that spins off a business shows a one-day drop that isn't a real loss.
* None of this is investment advice.
