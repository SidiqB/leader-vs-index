# S&P 500 — always own the #1 company vs the index

Period: 2008-01-02 to 2026-10-23. Start capital 10,000 USD. Benchmark: SPDR S&P 500 ETF (SPY).

## Summary

|                          |   Final value | Total return   | CAGR   | Volatility   |   Sharpe (rf=0) |   Sortino | Max drawdown   |   Calmar | Best year   | Worst year   |   Trades | Distinct companies held   | CAGR vs index   |
|:-------------------------|--------------:|:---------------|:-------|:-------------|----------------:|----------:|:---------------|---------:|:------------|:-------------|---------:|:--------------------------|:----------------|
| Naive: always #1         |        64,332 | 543.3%         | 10.4%  | 29.9%        |            0.48 |      0.64 | -50.1%         |     0.21 | 56.9%       | -26.4%       |       98 | 6                         | -0.8%           |
| Patient: 1-week confirm  |        97,410 | 874.6%         | 12.9%  | 29.7%        |            0.56 |      0.77 | -50.6%         |     0.25 | 68.1%       | -26.4%       |       26 | 5                         | +1.7%           |
| Patient: 1-month confirm |       129,383 | 1194.5%        | 14.6%  | 29.6%        |            0.61 |      0.84 | -43.8%         |     0.33 | 65.9%       | -26.4%       |       10 | 4                         | +3.4%           |
| S&P 500 (index)          |        73,854 | 638.5%         | 11.2%  | 19.7%        |            0.64 |      0.78 | -51.9%         |     0.22 | 32.3%       | -36.2%       |        1 | -                         | +0.0%           |

## Calendar-year returns (%)

|   Year |   Naive: always #1 |   Patient: 1-week confirm |   Patient: 1-month confirm |   S&P 500 (index) |
|-------:|-------------------:|--------------------------:|---------------------------:|------------------:|
|   2008 |              -13   |                     -13   |                      -13   |             -36.2 |
|   2009 |              -12.6 |                     -12.6 |                      -12.6 |              26.4 |
|   2010 |               10.1 |                      10.1 |                       10.1 |              15.1 |
|   2011 |                3.7 |                      10.3 |                       18.7 |               1.9 |
|   2012 |               21.6 |                      16.9 |                        5.6 |              16   |
|   2013 |               -1.4 |                      -7.6 |                        8.1 |              32.3 |
|   2014 |               40.6 |                      40.6 |                       40.6 |              13.5 |
|   2015 |               -3   |                      -3   |                       -3   |               1.3 |
|   2016 |                5.8 |                      12.5 |                       12.5 |              12   |
|   2017 |               48.5 |                      48.5 |                       48.5 |              21.7 |
|   2018 |               -4.8 |                      -2.6 |                       -2.6 |              -4.6 |
|   2019 |               54.4 |                      50.5 |                       65.9 |              31.2 |
|   2020 |               56.9 |                      68.1 |                       62.2 |              18.4 |
|   2021 |               31.5 |                      27.4 |                       34.6 |              28.7 |
|   2022 |              -26.4 |                     -26.4 |                      -26.4 |             -18.2 |
|   2023 |               49   |                      49   |                       49   |              26.2 |
|   2024 |                7.3 |                       4.3 |                       10.2 |              24.9 |
|   2025 |              -20.7 |                       5.4 |                        3.6 |              17.7 |
|   2026 |                1.8 |                      13.4 |                       13.4 |              12.3 |

## Share of time in each company

|             |   Naive: always #1 |   Patient: 1-week confirm |   Patient: 1-month confirm |
|:------------|-------------------:|--------------------------:|---------------------------:|
| Apple       |               61.9 |                      62.1 |                       61.5 |
| Exxon Mobil |               21.7 |                      21.7 |                       22.1 |
| Microsoft   |                8.6 |                       8.7 |                        9.8 |
| Nvidia      |                7.5 |                       7.3 |                        6.7 |
| Amazon      |                0.3 |                       0.2 |                        0   |
| Alphabet    |                0   |                       0   |                        0   |

## Holding periods — Patient: 1-week confirm

| Company     | Ticker   | From       | To         |   Days |   Return |   Index return |   Excess |
|:------------|:---------|:-----------|:-----------|-------:|---------:|---------------:|---------:|
| Exxon Mobil | XOM      | 2008-01-02 | 2011-09-15 |   1352 |    -13.8 |           -9.7 |     -4.1 |
| Apple       | AAPL     | 2011-09-15 | 2011-10-26 |     41 |      1.8 |            2.9 |     -1   |
| Exxon Mobil | XOM      | 2011-10-26 | 2012-02-03 |    100 |      5.3 |            8.9 |     -3.7 |
| Apple       | AAPL     | 2012-02-03 | 2013-03-08 |    399 |     -4.8 |           18.1 |    -22.9 |
| Exxon Mobil | XOM      | 2013-03-08 | 2013-03-22 |     14 |      0.3 |            0.5 |     -0.3 |
| Apple       | AAPL     | 2013-03-22 | 2013-04-24 |     33 |    -12.3 |            1.5 |    -13.8 |
| Exxon Mobil | XOM      | 2013-04-24 | 2013-05-03 |      9 |      0.6 |            2.2 |     -1.7 |
| Apple       | AAPL     | 2013-05-03 | 2013-06-24 |     52 |    -10   |           -2.2 |     -7.9 |
| Exxon Mobil | XOM      | 2013-06-24 | 2013-07-08 |     14 |      4.2 |            4.4 |     -0.2 |
| Apple       | AAPL     | 2013-07-08 | 2018-12-06 |   1977 |    226.3 |           82.6 |    143.7 |
| Microsoft   | MSFT     | 2018-12-06 | 2019-01-14 |     39 |     -6.6 |           -4   |     -2.6 |
| Amazon      | AMZN     | 2019-01-14 | 2019-01-29 |     15 |     -1.5 |            2.3 |     -3.9 |
| Microsoft   | MSFT     | 2019-01-29 | 2019-04-09 |     70 |     16.3 |            9.6 |      6.7 |
| Apple       | AAPL     | 2019-04-09 | 2019-04-30 |     21 |      0.5 |            2.3 |     -1.8 |
| Microsoft   | MSFT     | 2019-04-30 | 2019-10-24 |    177 |      7.8 |            3.1 |      4.7 |
| Apple       | AAPL     | 2019-10-24 | 2020-03-26 |    154 |      6.6 |          -12.1 |     18.6 |
| Microsoft   | MSFT     | 2020-03-26 | 2020-06-10 |     76 |     26.3 |           22.1 |      4.2 |
| Apple       | AAPL     | 2020-06-10 | 2021-11-05 |    513 |     73   |           50.2 |     22.8 |
| Microsoft   | MSFT     | 2021-11-05 | 2021-11-26 |     21 |     -1.8 |           -2   |      0.2 |
| Apple       | AAPL     | 2021-11-26 | 2024-02-01 |    797 |     20.4 |           10.4 |     10   |
| Microsoft   | MSFT     | 2024-02-01 | 2024-07-15 |    165 |     12.7 |           15.5 |     -2.8 |
| Apple       | AAPL     | 2024-07-15 | 2024-11-11 |    119 |     -4.2 |            7   |    -11.2 |
| Nvidia      | NVDA     | 2024-11-11 | 2024-12-02 |     21 |     -4.7 |            0.8 |     -5.5 |
| Apple       | AAPL     | 2024-12-02 | 2025-05-09 |    158 |    -17.1 |           -5.9 |    -11.2 |
| Microsoft   | MSFT     | 2025-05-09 | 2025-07-02 |     54 |     12   |           10.3 |      1.8 |
| Nvidia      | NVDA     | 2025-07-02 | 2026-10-23 |    478 |     34.5 |           24.1 |     10.3 |

## Holding periods — Patient: 1-month confirm

| Company     | Ticker   | From       | To         |   Days |   Return |   Index return |   Excess |
|:------------|:---------|:-----------|:-----------|-------:|---------:|---------------:|---------:|
| Exxon Mobil | XOM      | 2008-01-02 | 2012-02-27 |   1517 |      2.8 |            3.2 |     -0.4 |
| Apple       | AAPL     | 2012-02-27 | 2018-12-06 |   2474 |    163.1 |          125.2 |     37.9 |
| Microsoft   | MSFT     | 2018-12-06 | 2019-12-02 |    361 |     38.9 |           17.8 |     21.1 |
| Apple       | AAPL     | 2019-12-02 | 2020-04-20 |    140 |      5   |           -8.6 |     13.6 |
| Microsoft   | MSFT     | 2020-04-20 | 2020-07-06 |     77 |     20.6 |           13.1 |      7.5 |
| Apple       | AAPL     | 2020-07-06 | 2024-02-26 |   1330 |     98   |           68.3 |     29.7 |
| Microsoft   | MSFT     | 2024-02-26 | 2024-08-07 |    163 |     -2.2 |            3.2 |     -5.3 |
| Apple       | AAPL     | 2024-08-07 | 2025-05-14 |    280 |      1.6 |           14.4 |    -12.8 |
| Microsoft   | MSFT     | 2025-05-14 | 2025-07-25 |     72 |     13.5 |            8.7 |      4.8 |
| Nvidia      | NVDA     | 2025-07-25 | 2026-10-23 |    455 |     21.9 |           20.9 |      1   |

## Data notes

| ticker   | shares                                                   |   calibration |
|:---------|:---------------------------------------------------------|--------------:|
| MSFT     | SEC from 2007 + Yahoo from 2015; back-filled before 2007 |         1     |
| AAPL     | SEC from 2007 + Yahoo from 2015; back-filled before 2007 |         1     |
| XOM      | SEC from 2009 + Yahoo from 2015; back-filled before 2009 |         1     |
| GE       | SEC from 2009 + Yahoo from 2015; back-filled before 2009 |         1     |
| WMT      | SEC from 2008 + Yahoo from 2015; back-filled before 2008 |         1     |
| C        | SEC from 2007 + Yahoo from 2015; back-filled before 2007 |         0.987 |
| JNJ      | SEC from 2007 + Yahoo from 2015; back-filled before 2007 |         1     |
| PG       | SEC from 2008 + Yahoo from 2015; back-filled before 2008 |         1     |
| IBM      | SEC from 2007 + Yahoo from 2015; back-filled before 2007 |         1     |
| JPM      | SEC from 2007 + Yahoo from 2015; back-filled before 2007 |         1     |
| CVX      | SEC from 2008 + Yahoo from 2015; back-filled before 2008 |         1     |
| BAC      | SEC from 2007 + Yahoo from 2015; back-filled before 2007 |         0.99  |
| PFE      | SEC from 2007 + Yahoo from 2015; back-filled before 2007 |         1     |
| INTC     | SEC from 2007 + Yahoo from 2015; back-filled before 2007 |         1     |
| CSCO     | SEC from 2008 + Yahoo from 2015; back-filled before 2008 |         1     |
| ORCL     | SEC from 2008 + Yahoo from 2015; back-filled before 2008 |         1     |
| LLY      | SEC from 2008 + Yahoo from 2015; back-filled before 2008 |         1     |
| NVDA     | SEC from 2009 + Yahoo from 2015; back-filled before 2009 |         1     |
| AMZN     | SEC from 2007 + Yahoo from 2015; back-filled before 2007 |         1     |
| GOOGL    | SEC from 2008 + Yahoo from 2015; back-filled before 2008 |         1     |
| V        | Yahoo from 2015; back-filled before 2015                 |         1     |
| BRK-B    | Yahoo from 2015; back-filled before 2015                 |         1     |
| META     | SEC from 2010 + Yahoo from 2022                          |         1     |
| AVGO     | Yahoo from 2015; back-filled before 2015                 |         1     |
| TSLA     | SEC from 2010 + Yahoo from 2015; back-filled before 2010 |         1     |