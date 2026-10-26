# Nasdaq-100 — always own the #1 company vs the index

Period: 2008-01-02 to 2026-10-23. Start capital 10,000 USD. Benchmark: Invesco QQQ Trust (QQQ).

## Summary

|                          |   Final value | Total return   | CAGR   | Volatility   |   Sharpe (rf=0) |   Sortino | Max drawdown   |   Calmar | Best year   | Worst year   |   Trades | Distinct companies held   | CAGR vs index   |
|:-------------------------|--------------:|:---------------|:-------|:-------------|----------------:|----------:|:---------------|---------:|:------------|:-------------|---------:|:--------------------------|:----------------|
| Naive: always #1         |       109,623 | 996.2%         | 13.6%  | 30.6%        |            0.57 |      0.77 | -56.1%         |     0.24 | 60.5%       | -43.8%       |       70 | 5                         | -2.4%           |
| Patient: 1-week confirm  |       169,413 | 1595.0%        | 16.2%  | 30.3%        |            0.65 |      0.91 | -56.1%         |     0.29 | 68.1%       | -43.8%       |       18 | 4                         | +0.2%           |
| Patient: 1-month confirm |       181,584 | 1716.7%        | 16.7%  | 30.3%        |            0.66 |      0.92 | -56.1%         |     0.3  | 65.9%       | -43.8%       |       10 | 3                         | +0.7%           |
| Nasdaq-100 (index)       |       162,813 | 1528.1%        | 16.0%  | 22.4%        |            0.78 |      1    | -49.4%         |     0.32 | 54.9%       | -40.8%       |        1 | -                         | +0.0%           |

## Calendar-year returns (%)

|   Year |   Naive: always #1 |   Patient: 1-week confirm |   Patient: 1-month confirm |   Nasdaq-100 (index) |
|-------:|-------------------:|--------------------------:|---------------------------:|---------------------:|
|   2008 |              -43.8 |                     -43.8 |                      -43.8 |                -40.8 |
|   2009 |               60.5 |                      60.5 |                       60.5 |                 54.7 |
|   2010 |                9.4 |                       7   |                       -1.9 |                 20.1 |
|   2011 |               25.6 |                      25.6 |                       25.6 |                  3.5 |
|   2012 |               32.6 |                      32.6 |                       32.6 |                 18.1 |
|   2013 |                8.1 |                       8.1 |                        8.1 |                 36.6 |
|   2014 |               40.6 |                      40.6 |                       40.6 |                 19.2 |
|   2015 |               -3   |                      -3   |                       -3   |                  9.4 |
|   2016 |                5.8 |                      12.5 |                       12.5 |                  7.1 |
|   2017 |               48.5 |                      48.5 |                       48.5 |                 32.7 |
|   2018 |               -4.8 |                      -2.6 |                       -2.6 |                 -0.1 |
|   2019 |               54.4 |                      50.5 |                       65.9 |                 39   |
|   2020 |               56.9 |                      68.1 |                       62.2 |                 48.4 |
|   2021 |               31.5 |                      27.4 |                       34.6 |                 27.4 |
|   2022 |              -26.4 |                     -26.4 |                      -26.4 |                -32.6 |
|   2023 |               49   |                      49   |                       49   |                 54.9 |
|   2024 |                7.3 |                       4.3 |                       10.2 |                 25.6 |
|   2025 |              -20.7 |                       5.4 |                        3.6 |                 20.8 |
|   2026 |                1.8 |                      13.4 |                       13.4 |                 15.1 |

## Share of time in each company

|           |   Naive: always #1 |   Patient: 1-week confirm |   Patient: 1-month confirm |
|:----------|-------------------:|--------------------------:|---------------------------:|
| Apple     |               70.8 |                      70.9 |                       70.4 |
| Microsoft |               21.4 |                      21.6 |                       23   |
| Nvidia    |                7.5 |                       7.3 |                        6.7 |
| Amazon    |                0.3 |                       0.2 |                        0   |
| Alphabet  |                0   |                       0   |                        0   |

## Holding periods — Patient: 1-week confirm

| Company   | Ticker   | From       | To         |   Days |   Return |   Index return |   Excess |
|:----------|:---------|:-----------|:-----------|-------:|---------:|---------------:|---------:|
| Microsoft | MSFT     | 2008-01-02 | 2010-06-02 |    882 |    -21   |           -7.3 |    -13.7 |
| Apple     | AAPL     | 2010-06-02 | 2018-12-06 |   3109 |    424.2 |          295.9 |    128.3 |
| Microsoft | MSFT     | 2018-12-06 | 2019-01-14 |     39 |     -6.6 |           -4.3 |     -2.3 |
| Amazon    | AMZN     | 2019-01-14 | 2019-01-29 |     15 |     -1.5 |            1.4 |     -3   |
| Microsoft | MSFT     | 2019-01-29 | 2019-04-09 |     70 |     16.3 |           14.4 |      1.9 |
| Apple     | AAPL     | 2019-04-09 | 2019-04-30 |     21 |      0.5 |            2.7 |     -2.3 |
| Microsoft | MSFT     | 2019-04-30 | 2019-10-24 |    177 |      7.8 |            2.8 |      5   |
| Apple     | AAPL     | 2019-10-24 | 2020-03-26 |    154 |      6.6 |           -0.7 |      7.3 |
| Microsoft | MSFT     | 2020-03-26 | 2020-06-10 |     76 |     26.3 |           28.3 |     -2   |
| Apple     | AAPL     | 2020-06-10 | 2021-11-05 |    513 |     73   |           63   |     10   |
| Microsoft | MSFT     | 2021-11-05 | 2021-11-26 |     21 |     -1.8 |           -1.9 |      0   |
| Apple     | AAPL     | 2021-11-26 | 2024-02-01 |    797 |     20.4 |            9.5 |     10.9 |
| Microsoft | MSFT     | 2024-02-01 | 2024-07-15 |    165 |     12.7 |           17.9 |     -5.2 |
| Apple     | AAPL     | 2024-07-15 | 2024-11-11 |    119 |     -4.2 |            3.7 |     -7.9 |
| Nvidia    | NVDA     | 2024-11-11 | 2024-12-02 |     21 |     -4.7 |            0.3 |     -4.9 |
| Apple     | AAPL     | 2024-12-02 | 2025-05-09 |    158 |    -17.1 |           -5   |    -12.1 |
| Microsoft | MSFT     | 2025-05-09 | 2025-07-02 |     54 |     12   |           13   |     -1   |
| Nvidia    | NVDA     | 2025-07-02 | 2026-10-23 |    478 |     34.5 |           28.6 |      5.9 |

## Holding periods — Patient: 1-month confirm

| Company   | Ticker   | From       | To         |   Days |   Return |   Index return |   Excess |
|:----------|:---------|:-----------|:-----------|-------:|---------:|---------------:|---------:|
| Microsoft | MSFT     | 2008-01-02 | 2010-06-25 |    905 |    -26.8 |           -8.9 |    -17.9 |
| Apple     | AAPL     | 2010-06-25 | 2018-12-06 |   3086 |    418.8 |          302.9 |    115.9 |
| Microsoft | MSFT     | 2018-12-06 | 2019-12-02 |    361 |     38.9 |           22.7 |     16.1 |
| Apple     | AAPL     | 2019-12-02 | 2020-04-20 |    140 |      5   |            5.2 |     -0.3 |
| Microsoft | MSFT     | 2020-04-20 | 2020-07-06 |     77 |     20.6 |           21.7 |     -1.1 |
| Apple     | AAPL     | 2020-07-06 | 2024-02-26 |   1330 |     98   |           72.5 |     25.5 |
| Microsoft | MSFT     | 2024-02-26 | 2024-08-07 |    163 |     -2.2 |           -0.1 |     -2   |
| Apple     | AAPL     | 2024-08-07 | 2025-05-14 |    280 |      1.6 |           19.8 |    -18.3 |
| Microsoft | MSFT     | 2025-05-14 | 2025-07-25 |     72 |     13.5 |            9.3 |      4.2 |
| Nvidia    | NVDA     | 2025-07-25 | 2026-10-23 |    455 |     21.9 |           25.1 |     -3.2 |

## Data notes

| ticker   | shares                                                   |   calibration |
|:---------|:---------------------------------------------------------|--------------:|
| MSFT     | SEC from 2007 + Yahoo from 2015; back-filled before 2007 |             1 |
| AAPL     | SEC from 2007 + Yahoo from 2015; back-filled before 2007 |             1 |
| CSCO     | SEC from 2008 + Yahoo from 2015; back-filled before 2008 |             1 |
| INTC     | SEC from 2007 + Yahoo from 2015; back-filled before 2007 |             1 |
| QCOM     | SEC from 2007 + Yahoo from 2015; back-filled before 2007 |             1 |
| ORCL     | SEC from 2008 + Yahoo from 2015; back-filled before 2008 |             1 |
| AMZN     | SEC from 2007 + Yahoo from 2015; back-filled before 2007 |             1 |
| COST     | SEC from 2008 + Yahoo from 2015; back-filled before 2008 |             1 |
| NVDA     | SEC from 2009 + Yahoo from 2015; back-filled before 2009 |             1 |
| GOOGL    | SEC from 2008 + Yahoo from 2015; back-filled before 2008 |             1 |
| META     | SEC from 2010 + Yahoo from 2022                          |             1 |
| TSLA     | SEC from 2010 + Yahoo from 2015; back-filled before 2010 |             1 |
| AVGO     | Yahoo from 2015; back-filled before 2015                 |             1 |
| NFLX     | SEC from 2007 + Yahoo from 2015; back-filled before 2007 |             1 |