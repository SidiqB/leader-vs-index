# FTSE 100 — always own the #1 company vs the index

Period: 2009-01-02 to 2026-10-26. Start capital 10,000 GBP. Benchmark: iShares Core FTSE 100 ETF (ISF.L).

## Summary

|                          |   Final value | Total return   | CAGR   | Volatility   |   Sharpe (rf=0) |   Sortino | Max drawdown   |   Calmar | Best year   | Worst year   |   Trades | Distinct companies held   | CAGR vs index   |
|:-------------------------|--------------:|:---------------|:-------|:-------------|----------------:|----------:|:---------------|---------:|:------------|:-------------|---------:|:--------------------------|:----------------|
| Naive: always #1         |        15,882 | 58.8%          | 2.6%   | 25.6%        |            0.23 |      0.3  | -60.9%         |     0.04 | 58.6%       | -44.5%       |       81 | 4                         | -5.2%           |
| Patient: 1-week confirm  |        16,080 | 60.9%          | 2.7%   | 25.8%        |            0.23 |      0.31 | -60.9%         |     0.04 | 58.6%       | -51.0%       |       19 | 4                         | -5.1%           |
| Patient: 1-month confirm |        17,604 | 76.1%          | 3.2%   | 25.8%        |            0.25 |      0.34 | -63.6%         |     0.05 | 58.6%       | -58.8%       |        9 | 4                         | -4.6%           |
| FTSE 100 (index)         |        38,423 | 284.2%         | 7.8%   | 15.9%        |            0.56 |      0.72 | -34.0%         |     0.23 | 25.9%       | -11.5%       |        1 | -                         | +0.0%           |

## Calendar-year returns (%)

|   Year |   Naive: always #1 |   Patient: 1-week confirm |   Patient: 1-month confirm |   FTSE 100 (index) |
|-------:|-------------------:|--------------------------:|---------------------------:|-------------------:|
|   2009 |                6.1 |                       6.1 |                        6.1 |               17.8 |
|   2010 |               20.1 |                      20.1 |                       20.1 |                9.5 |
|   2011 |               16.1 |                      16.1 |                       16.1 |               -8.9 |
|   2012 |               -5.9 |                      -5.9 |                       -5.9 |                9   |
|   2013 |                7.5 |                       7.5 |                        7.5 |               17.4 |
|   2014 |                4.7 |                       4.7 |                        4.7 |                1   |
|   2015 |              -24.3 |                     -24.3 |                      -24.3 |               -1.7 |
|   2016 |               58.6 |                      58.6 |                       58.6 |               18.7 |
|   2017 |               18.3 |                      18.3 |                       18.3 |               13.1 |
|   2018 |               -1.4 |                      -1.4 |                       -1.4 |               -9   |
|   2019 |                3   |                       3   |                        3   |               17.1 |
|   2020 |              -44.5 |                     -51   |                      -58.8 |              -11.5 |
|   2021 |               22   |                      18.1 |                       30.1 |               17.7 |
|   2022 |               22.4 |                      38   |                       18.7 |                4.9 |
|   2023 |              -13.5 |                     -14.4 |                       -9.2 |                7.8 |
|   2024 |              -20.3 |                      -9.1 |                       -3.5 |                9.3 |
|   2025 |               20.1 |                      19.6 |                       34.6 |               25.9 |
|   2026 |                2.6 |                      -4.3 |                        3.9 |               11   |

## Share of time in each company

|             |   Naive: always #1 |   Patient: 1-week confirm |   Patient: 1-month confirm |
|:------------|-------------------:|--------------------------:|---------------------------:|
| Shell       |               79.2 |                      79.2 |                       79.1 |
| AstraZeneca |               16.2 |                      16.5 |                       17.1 |
| HSBC        |                3.6 |                       3.3 |                        2.5 |
| Unilever    |                1   |                       1   |                        1.3 |

## Holding periods — Patient: 1-week confirm

| Company     | Ticker   | From       | To         |   Days |   Return |   Index return |   Excess |
|:------------|:---------|:-----------|:-----------|-------:|---------:|---------------:|---------:|
| Shell       | SHEL.L   | 2009-01-02 | 2020-09-21 |   4280 |      5.5 |           68.4 |    -62.9 |
| Unilever    | ULVR.L   | 2020-09-21 | 2020-11-16 |     56 |      0.4 |           11   |    -10.6 |
| Shell       | SHEL.L   | 2020-11-16 | 2021-02-12 |     88 |      9.3 |            3.1 |      6.3 |
| Unilever    | ULVR.L   | 2021-02-12 | 2021-02-22 |     10 |     -3.4 |            0.5 |     -3.9 |
| Shell       | SHEL.L   | 2021-02-22 | 2022-06-29 |    492 |     60.3 |           16.4 |     43.9 |
| AstraZeneca | AZN.L    | 2022-06-29 | 2022-09-09 |     72 |     -4.4 |            1.7 |     -6.1 |
| Shell       | SHEL.L   | 2022-09-09 | 2022-11-24 |     76 |      2.7 |            1.9 |      0.7 |
| AstraZeneca | AZN.L    | 2022-11-24 | 2023-03-03 |     99 |      0.1 |            7.1 |     -7.1 |
| Shell       | SHEL.L   | 2023-03-03 | 2023-03-29 |     26 |    -11   |           -4.4 |     -6.7 |
| AstraZeneca | AZN.L    | 2023-03-29 | 2023-09-20 |    175 |     -1.4 |            4.2 |     -5.6 |
| Shell       | SHEL.L   | 2023-09-20 | 2024-01-15 |    117 |     -4.3 |           -0.9 |     -3.4 |
| AstraZeneca | AZN.L    | 2024-01-15 | 2024-02-19 |     35 |     -4.1 |            1.9 |     -6   |
| Shell       | SHEL.L   | 2024-02-19 | 2024-05-02 |     73 |     14.4 |            6.9 |      7.6 |
| AstraZeneca | AZN.L    | 2024-05-02 | 2025-09-30 |    516 |     -5.5 |           20.2 |    -25.8 |
| HSBC        | HSBA.L   | 2025-09-30 | 2025-10-08 |      8 |      1.9 |            2.3 |     -0.3 |
| AstraZeneca | AZN.L    | 2025-10-08 | 2026-01-27 |    111 |      8.3 |            7.6 |      0.6 |
| HSBC        | HSBA.L   | 2026-01-27 | 2026-02-18 |     22 |      1.5 |            4.8 |     -3.3 |
| AstraZeneca | AZN.L    | 2026-02-18 | 2026-04-28 |     69 |     -9.7 |           -2.3 |     -7.5 |
| HSBC        | HSBA.L   | 2026-04-28 | 2026-10-26 |    181 |      3.9 |            5.4 |     -1.5 |

## Holding periods — Patient: 1-month confirm

| Company     | Ticker   | From       | To         |   Days |   Return |   Index return |   Excess |
|:------------|:---------|:-----------|:-----------|-------:|---------:|---------------:|---------:|
| Shell       | SHEL.L   | 2009-01-02 | 2020-09-21 |   4280 |      5.5 |           68.4 |    -62.9 |
| Unilever    | ULVR.L   | 2020-09-21 | 2020-12-09 |     79 |     -5.9 |           13.8 |    -19.7 |
| Shell       | SHEL.L   | 2020-12-09 | 2022-07-22 |    590 |     56   |           17.1 |     38.9 |
| AstraZeneca | AZN.L    | 2022-07-22 | 2022-10-03 |     73 |     -8.3 |           -4   |     -4.4 |
| Shell       | SHEL.L   | 2022-10-03 | 2022-12-19 |     77 |      0.2 |            7   |     -6.7 |
| AstraZeneca | AZN.L    | 2022-12-19 | 2023-11-06 |    322 |     -5.6 |            4.2 |     -9.8 |
| Shell       | SHEL.L   | 2023-11-06 | 2024-05-28 |    204 |      7.1 |           13.6 |     -6.5 |
| AstraZeneca | AZN.L    | 2024-05-28 | 2026-05-21 |    723 |     20.8 |           35.6 |    -14.8 |
| HSBC        | HSBA.L   | 2026-05-21 | 2026-10-26 |    158 |      1.4 |            3.9 |     -2.5 |

## Data notes

| ticker   | shares                                   |   calibration |
|:---------|:-----------------------------------------|--------------:|
| SHEL.L   | Yahoo from 2022; back-filled before 2022 |             1 |
| BP.L     | Yahoo from 2015; back-filled before 2015 |             1 |
| HSBA.L   | Yahoo from 2015; back-filled before 2015 |             1 |
| AZN.L    | Yahoo from 2015; back-filled before 2015 |             1 |
| ULVR.L   | Yahoo from 2016; back-filled before 2016 |             1 |
| GSK.L    | Yahoo from 2015; back-filled before 2015 |             1 |
| VOD.L    | Yahoo from 2015; back-filled before 2015 |             1 |
| RIO.L    | Yahoo from 2015; back-filled before 2015 |             1 |
| BATS.L   | Yahoo from 2015; back-filled before 2015 |             1 |
| DGE.L    | Yahoo from 2015; back-filled before 2015 |             1 |
| LSEG.L   | Yahoo from 2021; back-filled before 2021 |             1 |