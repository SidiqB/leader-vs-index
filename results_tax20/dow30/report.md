# Dow Jones Industrial Average — always own the #1 company vs the index

Period: 2006-10-26 to 2026-10-23. Start capital 10,000 USD. Benchmark: SPDR Dow Jones Industrial Average ETF (DIA). Capital gains tax: 20%.

## Summary

|                                      |   Final value | Total return   | CAGR   | Volatility   |   Sharpe (rf=0) |   Sortino | Max drawdown   |   Calmar | Best year   | Worst year   |   Trades | Distinct companies held   |   Tax paid on switches |   After-tax value if sold today | After-tax CAGR   | CAGR vs index   | After-tax CAGR vs index   |
|:-------------------------------------|--------------:|:---------------|:-------|:-------------|----------------:|----------:|:---------------|---------:|:------------|:-------------|---------:|:--------------------------|-----------------------:|--------------------------------:|:-----------------|:----------------|:--------------------------|
| Naive: always #1                     |        30,018 | 200.2%         | 5.7%   | 28.2%        |            0.34 |      0.45 | -51.6%         |     0.11 | 56.5%       | -26.4%       |       95 | 5                         |                  7,350 |                          30,018 | 5.7%             | -4.3%           | -3.3%                     |
| Patient: 1-week confirm              |        58,806 | 488.4%         | 9.3%   | 28.1%        |            0.46 |      0.63 | -43.8%         |     0.21 | 59.0%       | -26.4%       |       19 | 5                         |                 10,104 |                          57,075 | 9.1%             | -0.7%           | +0.2%                     |
| Patient: 1-month confirm             |        61,259 | 512.9%         | 9.5%   | 28.1%        |            0.46 |      0.63 | -40.7%         |     0.23 | 55.2%       | -26.4%       |       11 | 5                         |                 10,102 |                          59,059 | 9.3%             | -0.5%           | +0.4%                     |
| Dow Jones Industrial Average (index) |        66,639 | 566.4%         | 10.0%  | 18.5%        |            0.61 |      0.75 | -51.9%         |     0.19 | 29.6%       | -32.2%       |        1 | -                         |                      0 |                          55,311 | 8.9%             | +0.0%           | +0.0%                     |

## Before vs after capital gains tax

|                                      |   Before tax: final value | Before tax: CAGR   |   Tax paid on switches |   After tax: value if sold today | After tax: CAGR   | Lost to tax   | After tax: CAGR vs index   |
|:-------------------------------------|--------------------------:|:-------------------|-----------------------:|---------------------------------:|:------------------|:--------------|:---------------------------|
| Naive: always #1                     |                    40,644 | 7.3%               |                  7,350 |                           30,018 | 5.7%              | 26.1%         | -3.3%                      |
| Patient: 1-week confirm              |                    83,317 | 11.2%              |                 10,104 |                           57,075 | 9.1%              | 31.5%         | +0.2%                      |
| Patient: 1-month confirm             |                    85,618 | 11.3%              |                 10,102 |                           59,059 | 9.3%              | 31.0%         | +0.4%                      |
| Dow Jones Industrial Average (index) |                    66,639 | 10.0%              |                      0 |                           55,311 | 8.9%              | 17.0%         | +0.0%                      |

## Calendar-year returns (%)

|   Year |   Naive: always #1 |   Patient: 1-week confirm |   Patient: 1-month confirm |   Dow Jones Industrial Average (index) |
|-------:|-------------------:|--------------------------:|---------------------------:|---------------------------------------:|
|   2006 |               -1.1 |                       5.3 |                        5.3 |                                    3   |
|   2007 |                3.2 |                      15.4 |                       13.8 |                                    8.8 |
|   2008 |              -13.1 |                     -13.1 |                      -13.1 |                                  -32.2 |
|   2009 |              -12.6 |                     -12.6 |                      -12.6 |                                   22.7 |
|   2010 |               10.1 |                      10.1 |                       10.1 |                                   14   |
|   2011 |               18.7 |                      18.7 |                       18.7 |                                    8.1 |
|   2012 |                4.7 |                       4.7 |                        4.7 |                                    9.9 |
|   2013 |               20.1 |                      20.1 |                       20.1 |                                   29.6 |
|   2014 |              -18.1 |                     -15.7 |                       -6.1 |                                    9.7 |
|   2015 |              -24.1 |                     -19.6 |                      -24   |                                    0.1 |
|   2016 |               12.5 |                      12.5 |                       12.5 |                                   16.4 |
|   2017 |               48.5 |                      48.5 |                       48.5 |                                   28.1 |
|   2018 |               -8.2 |                      -9.9 |                       -5.4 |                                   -3.7 |
|   2019 |               56.5 |                      54.3 |                       39   |                                   25   |
|   2020 |               49.7 |                      59   |                       55.2 |                                    9.6 |
|   2021 |               20.7 |                      16.7 |                       34.6 |                                   20.8 |
|   2022 |              -26.4 |                     -26.4 |                      -26.4 |                                   -7   |
|   2023 |               49   |                      49   |                       49   |                                   16   |
|   2024 |               -1.3 |                       1.4 |                       -0.8 |                                   14.8 |
|   2025 |              -20.7 |                       5.4 |                        1.2 |                                   14.7 |
|   2026 |                1.8 |                      13.4 |                       13.4 |                                    9.7 |

## Share of time in each company

|                  |   Naive: always #1 |   Patient: 1-week confirm |   Patient: 1-month confirm |
|:-----------------|-------------------:|--------------------------:|---------------------------:|
| Apple            |               42.7 |                      43   |                       42.5 |
| Exxon Mobil      |               39.1 |                      39.6 |                       39.3 |
| Microsoft        |                8.8 |                       8.5 |                        8.8 |
| Nvidia           |                7   |                       6.8 |                        6.3 |
| General Electric |                2.4 |                       2.2 |                        3.1 |

## Holding periods — Patient: 1-week confirm

| Company          | Ticker   | From       | To         |   Days |   Return |   Index return |   Excess |
|:-----------------|:---------|:-----------|:-----------|-------:|---------:|---------------:|---------:|
| General Electric | GE       | 2006-10-26 | 2007-04-10 |    166 |     -0.6 |            4.5 |     -5   |
| Exxon Mobil      | XOM      | 2007-04-10 | 2014-12-11 |   2802 |     30.7 |           69.9 |    -39.2 |
| Microsoft        | MSFT     | 2014-12-11 | 2015-01-05 |     25 |     -1.9 |           -0.5 |     -1.4 |
| Exxon Mobil      | XOM      | 2015-01-05 | 2015-03-26 |     80 |     -6   |            1.5 |     -7.5 |
| Apple            | AAPL     | 2015-03-26 | 2018-12-13 |   1358 |     39.1 |           51.7 |    -12.6 |
| Microsoft        | MSFT     | 2018-12-13 | 2019-04-09 |    117 |      7.5 |            7.1 |      0.4 |
| Apple            | AAPL     | 2019-04-09 | 2019-05-09 |     30 |      0.4 |           -1.1 |      1.5 |
| Microsoft        | MSFT     | 2019-05-09 | 2019-10-24 |    168 |      9.7 |            4.9 |      4.9 |
| Apple            | AAPL     | 2019-10-24 | 2020-03-26 |    154 |      5.2 |          -15.1 |     20.3 |
| Microsoft        | MSFT     | 2020-03-26 | 2020-06-10 |     76 |     21   |           20.5 |      0.6 |
| Apple            | AAPL     | 2020-06-10 | 2021-11-05 |    513 |     58.4 |           37.8 |     20.5 |
| Microsoft        | MSFT     | 2021-11-05 | 2021-11-26 |     21 |     -1.8 |           -3.7 |      1.9 |
| Apple            | AAPL     | 2021-11-26 | 2024-02-01 |    797 |     16.7 |           15   |      1.6 |
| Microsoft        | MSFT     | 2024-02-01 | 2024-07-15 |    165 |     10.2 |            5.3 |      4.8 |
| Apple            | AAPL     | 2024-07-15 | 2024-11-15 |    123 |     -3.9 |            8.6 |    -12.4 |
| Nvidia           | NVDA     | 2024-11-15 | 2024-12-02 |     17 |     -2.5 |            3.3 |     -5.7 |
| Apple            | AAPL     | 2024-12-02 | 2025-05-09 |    158 |    -17.1 |           -7.4 |     -9.7 |
| Microsoft        | MSFT     | 2025-05-09 | 2025-07-02 |     54 |     12   |            8.2 |      3.8 |
| Nvidia           | NVDA     | 2025-07-02 | 2026-10-23 |    478 |     34.5 |           19.5 |     15   |

## Holding periods — Patient: 1-month confirm

| Company          | Ticker   | From       | To         |   Days |   Return |   Index return |   Excess |
|:-----------------|:---------|:-----------|:-----------|-------:|---------:|---------------:|---------:|
| General Electric | GE       | 2006-10-26 | 2007-06-11 |    228 |      5.4 |           12   |     -6.6 |
| Exxon Mobil      | XOM      | 2007-06-11 | 2015-04-20 |   2870 |     21.4 |           63.3 |    -42   |
| Apple            | AAPL     | 2015-04-20 | 2019-01-07 |   1358 |     19   |           42.4 |    -23.4 |
| Microsoft        | MSFT     | 2019-01-07 | 2019-12-02 |    329 |     38.8 |           20.5 |     18.3 |
| Apple            | AAPL     | 2019-12-02 | 2020-04-20 |    140 |      4   |          -14.1 |     18.1 |
| Microsoft        | MSFT     | 2020-04-20 | 2020-07-06 |     77 |     16.4 |           11.7 |      4.8 |
| Apple            | AAPL     | 2020-07-06 | 2024-02-26 |   1330 |     78.4 |           59.1 |     19.3 |
| Microsoft        | MSFT     | 2024-02-26 | 2024-08-07 |    163 |     -2.2 |           -0   |     -2.1 |
| Apple            | AAPL     | 2024-08-07 | 2025-05-14 |    280 |      1.6 |            9.7 |     -8.2 |
| Microsoft        | MSFT     | 2025-05-14 | 2025-07-25 |     72 |     10.9 |            7.2 |      3.7 |
| Nvidia           | NVDA     | 2025-07-25 | 2026-10-23 |    455 |     21.9 |           18.3 |      3.6 |

## Data notes

| ticker   | shares                                                       |   calibration |
|:---------|:-------------------------------------------------------------|--------------:|
| MSFT     | SEC from 2007 + Yahoo from 2015; trend-estimated before 2007 |         1     |
| XOM      | SEC from 2009 + Yahoo from 2015; trend-estimated before 2009 |         1     |
| GE       | SEC from 2009 + Yahoo from 2015; trend-estimated before 2009 |         1     |
| WMT      | SEC from 2008 + Yahoo from 2015; trend-estimated before 2008 |         1     |
| JNJ      | SEC from 2007 + Yahoo from 2015; trend-estimated before 2007 |         1     |
| IBM      | SEC from 2007 + Yahoo from 2015; trend-estimated before 2007 |         1     |
| PG       | SEC from 2008 + Yahoo from 2015; trend-estimated before 2008 |         1     |
| JPM      | SEC from 2007 + Yahoo from 2015; trend-estimated before 2007 |         1     |
| KO       | SEC from 2007 + Yahoo from 2015; trend-estimated before 2007 |         1     |
| C        | SEC from 2007 + Yahoo from 2015; trend-estimated before 2007 |         0.987 |
| INTC     | SEC from 2007 + Yahoo from 2015; trend-estimated before 2007 |         1     |
| PFE      | SEC from 2007 + Yahoo from 2015; trend-estimated before 2007 |         1     |
| CVX      | SEC from 2008 + Yahoo from 2015; trend-estimated before 2008 |         1     |
| CSCO     | SEC from 2008 + Yahoo from 2015; trend-estimated before 2008 |         1     |
| V        | Yahoo from 2015; trend-estimated before 2015                 |         1     |
| AAPL     | SEC from 2007 + Yahoo from 2015; trend-estimated before 2007 |         1     |
| AMZN     | SEC from 2007 + Yahoo from 2015; trend-estimated before 2007 |         1     |
| NVDA     | SEC from 2009 + Yahoo from 2015; trend-estimated before 2009 |         1     |