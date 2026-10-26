# Dow Jones Industrial Average — always own the #1 company vs the index

Period: 2008-01-02 to 2026-10-23. Start capital 10,000 USD. Benchmark: SPDR Dow Jones Industrial Average ETF (DIA).

## Summary

|                                      |   Final value | Total return   | CAGR   | Volatility   |   Sharpe (rf=0) |   Sortino | Max drawdown   |   Calmar | Best year   | Worst year   |   Trades | Distinct companies held   | CAGR vs index   |
|:-------------------------------------|--------------:|:---------------|:-------|:-------------|----------------:|----------:|:---------------|---------:|:------------|:-------------|---------:|:--------------------------|:----------------|
| Naive: always #1                     |        39,898 | 299.0%         | 7.6%   | 28.5%        |            0.4  |      0.53 | -51.6%         |     0.15 | 62.2%       | -26.4%       |       72 | 4                         | -2.4%           |
| Patient: 1-week confirm              |        68,653 | 586.9%         | 10.8%  | 28.3%        |            0.5  |      0.69 | -40.5%         |     0.27 | 68.1%       | -26.4%       |       18 | 4                         | +0.8%           |
| Patient: 1-month confirm             |        70,650 | 606.9%         | 11.0%  | 28.3%        |            0.51 |      0.69 | -38.5%         |     0.28 | 62.2%       | -26.4%       |       10 | 4                         | +0.9%           |
| Dow Jones Industrial Average (index) |        60,350 | 503.5%         | 10.0%  | 18.8%        |            0.6  |      0.75 | -48.6%         |     0.21 | 29.6%       | -31.2%       |        1 | -                         | +0.0%           |

## Calendar-year returns (%)

|   Year |   Naive: always #1 |   Patient: 1-week confirm |   Patient: 1-month confirm |   Dow Jones Industrial Average (index) |
|-------:|-------------------:|--------------------------:|---------------------------:|---------------------------------------:|
|   2008 |              -13   |                     -13   |                      -13   |                                  -31.2 |
|   2009 |              -12.6 |                     -12.6 |                      -12.6 |                                   22.7 |
|   2010 |               10.1 |                      10.1 |                       10.1 |                                   14   |
|   2011 |               18.7 |                      18.7 |                       18.7 |                                    8.1 |
|   2012 |                4.7 |                       4.7 |                        4.7 |                                    9.9 |
|   2013 |               20.1 |                      20.1 |                       20.1 |                                   29.6 |
|   2014 |              -14.9 |                     -10.8 |                       -6.1 |                                    9.7 |
|   2015 |              -24.1 |                     -19.6 |                      -20.6 |                                    0.1 |
|   2016 |               12.5 |                      12.5 |                       12.5 |                                   16.4 |
|   2017 |               48.5 |                      48.5 |                       48.5 |                                   28.1 |
|   2018 |               -4.8 |                      -4.9 |                       -5.4 |                                   -3.7 |
|   2019 |               62.2 |                      60.6 |                       54.7 |                                   25   |
|   2020 |               56.9 |                      68.1 |                       62.2 |                                    9.6 |
|   2021 |               31.5 |                      27.4 |                       34.6 |                                   20.8 |
|   2022 |              -26.4 |                     -26.4 |                      -26.4 |                                   -7   |
|   2023 |               49   |                      49   |                       49   |                                   16   |
|   2024 |                4.8 |                       7.1 |                       10.2 |                                   14.8 |
|   2025 |              -20.7 |                       5.4 |                        3.6 |                                   14.7 |
|   2026 |                1.8 |                      13.4 |                       13.4 |                                    9.7 |

## Share of time in each company

|             |   Naive: always #1 |   Patient: 1-week confirm |   Patient: 1-month confirm |
|:------------|-------------------:|--------------------------:|---------------------------:|
| Apple       |               45.3 |                      45.7 |                       45.2 |
| Exxon Mobil |               37.9 |                      38.1 |                       38.8 |
| Microsoft   |                9.4 |                       9   |                        9.4 |
| Nvidia      |                7.4 |                       7.2 |                        6.7 |

## Holding periods — Patient: 1-week confirm

| Company     | Ticker   | From       | To         |   Days |   Return |   Index return |   Excess |
|:------------|:---------|:-----------|:-----------|-------:|---------:|---------------:|---------:|
| Exxon Mobil | XOM      | 2008-01-02 | 2014-12-11 |   2535 |     13.3 |           60.8 |    -47.5 |
| Microsoft   | MSFT     | 2014-12-11 | 2015-01-05 |     25 |     -1.9 |           -0.5 |     -1.4 |
| Exxon Mobil | XOM      | 2015-01-05 | 2015-03-26 |     80 |     -6   |            1.5 |     -7.5 |
| Apple       | AAPL     | 2015-03-26 | 2018-12-13 |   1358 |     46.8 |           51.7 |     -4.8 |
| Microsoft   | MSFT     | 2018-12-13 | 2019-04-09 |    117 |      9.3 |            7.1 |      2.3 |
| Apple       | AAPL     | 2019-04-09 | 2019-05-09 |     30 |      0.5 |           -1.1 |      1.6 |
| Microsoft   | MSFT     | 2019-05-09 | 2019-10-24 |    168 |     12.2 |            4.9 |      7.3 |
| Apple       | AAPL     | 2019-10-24 | 2020-03-26 |    154 |      6.6 |          -15.1 |     21.6 |
| Microsoft   | MSFT     | 2020-03-26 | 2020-06-10 |     76 |     26.3 |           20.5 |      5.8 |
| Apple       | AAPL     | 2020-06-10 | 2021-11-05 |    513 |     73   |           37.8 |     35.2 |
| Microsoft   | MSFT     | 2021-11-05 | 2021-11-26 |     21 |     -1.8 |           -3.7 |      1.9 |
| Apple       | AAPL     | 2021-11-26 | 2024-02-01 |    797 |     20.4 |           15   |      5.4 |
| Microsoft   | MSFT     | 2024-02-01 | 2024-07-15 |    165 |     12.7 |            5.3 |      7.4 |
| Apple       | AAPL     | 2024-07-15 | 2024-11-15 |    123 |     -3.9 |            8.6 |    -12.4 |
| Nvidia      | NVDA     | 2024-11-15 | 2024-12-02 |     17 |     -2.5 |            3.3 |     -5.7 |
| Apple       | AAPL     | 2024-12-02 | 2025-05-09 |    158 |    -17.1 |           -7.4 |     -9.7 |
| Microsoft   | MSFT     | 2025-05-09 | 2025-07-02 |     54 |     12   |            8.2 |      3.8 |
| Nvidia      | NVDA     | 2025-07-02 | 2026-10-23 |    478 |     34.5 |           19.5 |     15   |

## Holding periods — Patient: 1-month confirm

| Company     | Ticker   | From       | To         |   Days |   Return |   Index return |   Excess |
|:------------|:---------|:-----------|:-----------|-------:|---------:|---------------:|---------:|
| Exxon Mobil | XOM      | 2008-01-02 | 2015-04-20 |   2665 |     11.6 |           65.7 |    -54.1 |
| Apple       | AAPL     | 2015-04-20 | 2019-01-07 |   1358 |     23.7 |           42.4 |    -18.7 |
| Microsoft   | MSFT     | 2019-01-07 | 2019-12-02 |    329 |     48.6 |           20.5 |     28.1 |
| Apple       | AAPL     | 2019-12-02 | 2020-04-20 |    140 |      5   |          -14.1 |     19.1 |
| Microsoft   | MSFT     | 2020-04-20 | 2020-07-06 |     77 |     20.6 |           11.7 |      8.9 |
| Apple       | AAPL     | 2020-07-06 | 2024-02-26 |   1330 |     98   |           59.1 |     39   |
| Microsoft   | MSFT     | 2024-02-26 | 2024-08-07 |    163 |     -2.2 |           -0   |     -2.1 |
| Apple       | AAPL     | 2024-08-07 | 2025-05-14 |    280 |      1.6 |            9.7 |     -8.2 |
| Microsoft   | MSFT     | 2025-05-14 | 2025-07-25 |     72 |     13.5 |            7.2 |      6.3 |
| Nvidia      | NVDA     | 2025-07-25 | 2026-10-23 |    455 |     21.9 |           18.3 |      3.6 |

## Data notes

| ticker   | shares                                                   |   calibration |
|:---------|:---------------------------------------------------------|--------------:|
| MSFT     | SEC from 2007 + Yahoo from 2015; back-filled before 2007 |         1     |
| XOM      | SEC from 2009 + Yahoo from 2015; back-filled before 2009 |         1     |
| GE       | SEC from 2009 + Yahoo from 2015; back-filled before 2009 |         1     |
| WMT      | SEC from 2008 + Yahoo from 2015; back-filled before 2008 |         1     |
| JNJ      | SEC from 2007 + Yahoo from 2015; back-filled before 2007 |         1     |
| IBM      | SEC from 2007 + Yahoo from 2015; back-filled before 2007 |         1     |
| PG       | SEC from 2008 + Yahoo from 2015; back-filled before 2008 |         1     |
| JPM      | SEC from 2007 + Yahoo from 2015; back-filled before 2007 |         1     |
| KO       | SEC from 2007 + Yahoo from 2015; back-filled before 2007 |         1     |
| C        | SEC from 2007 + Yahoo from 2015; back-filled before 2007 |         0.987 |
| INTC     | SEC from 2007 + Yahoo from 2015; back-filled before 2007 |         1     |
| PFE      | SEC from 2007 + Yahoo from 2015; back-filled before 2007 |         1     |
| CVX      | SEC from 2008 + Yahoo from 2015; back-filled before 2008 |         1     |
| CSCO     | SEC from 2008 + Yahoo from 2015; back-filled before 2008 |         1     |
| V        | Yahoo from 2015; back-filled before 2015                 |         1     |
| AAPL     | SEC from 2007 + Yahoo from 2015; back-filled before 2007 |         1     |
| AMZN     | SEC from 2007 + Yahoo from 2015; back-filled before 2007 |         1     |
| NVDA     | SEC from 2009 + Yahoo from 2015; back-filled before 2009 |         1     |