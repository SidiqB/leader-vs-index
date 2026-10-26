"""Interactive dashboard:  streamlit run app.py

Pick an index in the sidebar and everything re-runs automatically: the animated race
chart plays, then the comparison charts and tables appear underneath.
"""

from __future__ import annotations

import time

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from leadertrack.analysis import (holding_periods, leader_history, rolling_excess, run_backtest, summary_table,
                                  time_held, yearly_returns)
from leadertrack.data import load_market_data
from leadertrack.indices import INDICES
from leadertrack.plots import INDEX_INK, OTHER, SERIES
from leadertrack.strategies import StrategyConfig, TaxConfig

st.set_page_config(page_title="Leader vs Index", page_icon="📈", layout="wide")

SYM = {"USD": "$", "GBP": "£", "EUR": "€"}


@st.cache_data(show_spinner=False, ttl=6 * 3600)
def market_data(key: str):
    return load_market_data(INDICES[key])


def colors_for(bt):
    c = {r.config.name: SERIES[i % len(SERIES)] for i, r in enumerate(bt.results)}
    c[bt.benchmark_label] = INDEX_INK
    return c


def base_layout(fig, title, height=420, log=False, pct=False, money=None):
    fig.update_layout(
        title=dict(text=title, x=0, xanchor="left", font=dict(size=16)), height=height, hovermode="x unified",
        margin=dict(l=10, r=10, t=50, b=10), legend=dict(orientation="h", y=-0.15),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="rgba(128,128,128,0.2)", type="log" if log else None,
                     tickformat=".0%" if pct else (",.0f" if money else None), tickprefix=money or "")
    if log:
        fig.update_yaxes(dtick="D2")
    return fig


# ---------------------------------------------------------------- sidebar
st.sidebar.title("📈 Leader vs Index")
key = st.sidebar.selectbox("Index", list(INDICES), format_func=lambda k: INDICES[k].name)
years = st.sidebar.slider("Years to backtest", 3, 30, 20)
start = (pd.Timestamp.today().normalize() - pd.DateOffset(years=years)).date()
capital = st.sidebar.number_input("Starting money", 1_000, 10_000_000, 10_000, step=1_000)

st.sidebar.subheader("Model 1 · Naive")
st.sidebar.caption("Switch every single time a new company becomes #1.")
naive_cost = st.sidebar.number_input("Cost per switch (bps)", 0.0, 100.0, 0.0, key="nc")

st.sidebar.subheader("Model 2 · Patient")
st.sidebar.caption("Ignore new IPOs until they mature. Keep holding while your company is #2; "
                   "switch once the new #1 has held the top spot long enough, or straight away if yours drops to #3.")
confirm = st.sidebar.multiselect("Confirmation period(s), days", [7, 14, 30, 60, 90], default=[7, 30])
min_age = st.sidebar.slider("IPO maturity (days trading before eligible)", 0, 1095, 365, step=30)
drop_rank = st.sidebar.slider("Sell immediately if holding falls to rank", 2, 5, 3)
cost = st.sidebar.number_input("Cost per switch (bps)", 0.0, 100.0, 10.0, key="pc")

st.sidebar.subheader("Tax")
st.sidebar.caption("Every switch is a sale, so gains get taxed along the way (losses carry forward). "
                   "The index is buy-and-hold: it only pays once, when you sell at the end. "
                   "Set 0 for a tax-free account (ISA, IRA/401k).")
tax_rate = st.sidebar.slider("Capital gains tax %", 0, 45, 0)
use_short = st.sidebar.toggle("Higher rate if held under a year (US-style)", False)
short_rate = st.sidebar.slider("Short-term rate %", 0, 50, 37, disabled=not use_short)
tax = TaxConfig(rate=tax_rate / 100, short_term_rate=short_rate / 100 if use_short else None)

st.sidebar.subheader("Animation")
animate = st.sidebar.toggle("Play the race chart", True)
speed = st.sidebar.slider("Speed", 1, 10, 6)

strategies = [StrategyConfig("Naive: always #1", kind="naive", cost_bps=naive_cost)]
for d in sorted(confirm):
    label = {7: "1-week", 14: "2-week", 30: "1-month", 60: "2-month", 90: "3-month"}[d]
    strategies.append(StrategyConfig(f"Patient: {label} confirm", kind="patient", min_age_days=min_age,
                                     confirm_days=d, drop_rank=drop_rank, cost_bps=cost))

# ---------------------------------------------------------------- run
idx = INDICES[key]
with st.spinner(f"Downloading {idx.name} data (first run takes ~30s, then it's cached)…"):
    md = market_data(key)
bt = run_backtest(key, start=str(start), capital=float(capital), strategies=tuple(strategies), md=md, tax=tax)
# Same run without tax, for the before/after comparison
bt_pre = (run_backtest(key, start=str(start), capital=float(capital), strategies=tuple(strategies), md=md)
          if tax.active else bt)
eq = bt.equity
colors = colors_for(bt)
names = bt.names()
money = SYM.get(idx.currency, "")

st.title(f"Always own the #1 company vs the {idx.name}")
st.caption(f"{eq.index[0]:%d %b %Y} → {eq.index[-1]:%d %b %Y} · benchmark: {idx.benchmark_name} · "
           f"dividends reinvested · {len(idx.members)} candidate companies"
           + (f" · {idx.note}" if idx.note else ""))
if not idx.us_listed:
    st.info("Non-US index: historical share counts are only available from ~2015, so market caps before that "
            "are estimated from later share counts. Rankings in early years are approximate.")
if pd.Timestamp(start) < pd.Timestamp("2008-01-01"):
    st.warning("Share-count data mostly starts 2007-2009, so rankings before then use estimated share "
               "counts and can be off when two companies are close.")

# ---------------------------------------------------------------- race chart
race = st.empty()
holdings = {r.config.name: r.holding for r in bt.results}


def race_figure(n: int):
    sl = eq.iloc[:n]
    d = sl.index[-1]
    fig = go.Figure()
    for col in eq.columns:
        fig.add_trace(go.Scatter(x=sl.index, y=sl[col], name=col, mode="lines",
                                 line=dict(color=colors[col], width=3 if col == bt.benchmark_label else 2)))
        held = holdings.get(col)
        tag = f" · {names.get(held.loc[d], held.loc[d])}" if held is not None and isinstance(held.loc[d], str) else ""
        fig.add_trace(go.Scatter(x=[d], y=[sl[col].iloc[-1]], mode="markers+text", showlegend=False,
                                 marker=dict(color=colors[col], size=10, line=dict(width=2, color="white")),
                                 text=[f"  {money}{sl[col].iloc[-1]:,.0f}{tag}"], textposition="middle right",
                                 hoverinfo="skip"))
    fig.add_annotation(text=f"<b>{d:%b %Y}</b>", x=0.01, y=0.97, xref="paper", yref="paper", showarrow=False,
                       font=dict(size=28, color="gray"), xanchor="left")
    base_layout(fig, f"Growth of {money}{capital:,.0f}", height=520, log=True, money=money)
    pad = (eq.index[-1] - eq.index[0]) * 0.3
    fig.update_xaxes(range=[eq.index[0], eq.index[-1] + pad])
    fig.update_yaxes(range=[np.log10(eq.min().min() * 0.85), np.log10(eq.max().max() * 1.2)])
    return fig


if animate:
    steps = np.unique(np.linspace(2, len(eq), 90).astype(int))
    for n in steps:
        race.plotly_chart(race_figure(n), use_container_width=True, key=f"race_{n}")
        time.sleep(0.25 / speed)
race.plotly_chart(race_figure(len(eq)), use_container_width=True, key="race_final")

# ---------------------------------------------------------------- headline numbers
summary = summary_table(bt)
pre_final = summary_table(bt_pre)["Final value"]
cols = st.columns(len(summary))
val_col, cagr_col, vs_col = (("After-tax value if sold today", "After-tax CAGR", "After-tax CAGR vs index")
                             if tax.active else ("Final value", "CAGR", "CAGR vs index"))
if tax.active:
    st.caption(f"Headline numbers are **after {tax_rate}% capital gains tax**, as if you sold everything today.")
for c, (name, row) in zip(cols, summary.iterrows()):
    c.metric(name, f"{money}{row[val_col]:,.0f}",
             f"{row[vs_col]:+.1%} a year vs index" if name != bt.benchmark_label else f"{row[cagr_col]:.1%} a year",
             delta_color="normal" if name != bt.benchmark_label else "off")
    if tax.active:
        m = money.replace("$", "\\$")  # a bare $ would start LaTeX in markdown
        c.caption(f"Before tax {m}{pre_final[name]:,.0f} · tax paid on switches "
                  f"{m}{row['Tax paid on switches']:,.0f}")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Comparison charts", "Tables", "Holdings & trades", "All indices", "Data notes"])

# ---------------------------------------------------------------- charts
with tab1:
    if tax.active:
        fig = go.Figure([
            go.Bar(x=summary.index, y=pre_final.reindex(summary.index), name="Before tax", marker_color=SERIES[0]),
            go.Bar(x=summary.index, y=summary["After-tax value if sold today"], name=f"After {tax_rate}% tax",
                   marker_color=SERIES[1],
                   text=[f"{money}{v:,.0f}" for v in summary["After-tax value if sold today"]], textposition="outside"),
        ])
        fig.update_layout(barmode="group")
        st.plotly_chart(base_layout(fig, "What you'd actually keep: before vs after capital gains tax", money=money),
                        use_container_width=True)
    a, b = st.columns(2)
    dd = eq / eq.cummax() - 1
    fig = go.Figure([go.Scatter(x=dd.index, y=dd[c], name=c, line=dict(color=colors[c], width=1.6)) for c in dd])
    a.plotly_chart(base_layout(fig, "Drawdown from previous peak", pct=True), use_container_width=True)

    rx = rolling_excess(bt)
    fig = go.Figure([go.Scatter(x=rx.index, y=rx[c], name=c, line=dict(color=colors[c], width=1.6)) for c in rx])
    fig.add_hline(y=0, line_color=INDEX_INK)
    b.plotly_chart(base_layout(fig, "Rolling 1-year return minus the index", pct=True), use_container_width=True)

    yr = yearly_returns(bt)
    fig = go.Figure([go.Bar(x=yr.index.astype(str), y=yr[c], name=c, marker_color=colors[c]) for c in yr])
    fig.update_layout(barmode="group", bargap=0.25, bargroupgap=0.05)
    st.plotly_chart(base_layout(fig, "Calendar-year returns", pct=True), use_container_width=True)

    s = summary.drop(columns=["CAGR vs index"])
    a, b = st.columns(2)
    fig = go.Figure([go.Bar(x=s.index, y=s["CAGR"], marker_color=[colors[c] for c in s.index],
                            text=[f"{v:.1%}" for v in s["CAGR"]], textposition="outside")])
    a.plotly_chart(base_layout(fig, "Annual growth rate (CAGR)", pct=True), use_container_width=True)
    fig = go.Figure([go.Scatter(x=s["Volatility"], y=s["CAGR"], mode="markers+text", text=s.index,
                                textposition="top center",
                                marker=dict(size=14, color=[colors[c] for c in s.index], line=dict(width=2, color="white")))])
    fig.update_xaxes(tickformat=".0%", title="Volatility (risk)")
    b.plotly_chart(base_layout(fig, "Risk vs return", pct=True), use_container_width=True)

# ---------------------------------------------------------------- tables
with tab2:
    st.subheader("Performance summary")
    pct_cols = ["Total return", "CAGR", "CAGR vs index", "Volatility", "Max drawdown", "Best year", "Worst year",
                "After-tax CAGR", "After-tax CAGR vs index"]
    fmt = {c: "{:.1%}" for c in pct_cols} | {"Final value": money + "{:,.0f}", "Sharpe (rf=0)": "{:.2f}",
                                              "Sortino": "{:.2f}", "Calmar": "{:.2f}", "Trades": "{:.0f}",
                                              "Distinct companies held": "{:.0f}",
                                              "Tax paid on switches": money + "{:,.0f}",
                                              "After-tax value if sold today": money + "{:,.0f}"}
    st.dataframe(summary.style.format(fmt, na_rep="-"), use_container_width=True)

    st.subheader("Calendar-year returns")
    st.dataframe(yr.style.format("{:+.1%}").background_gradient(cmap="RdYlGn", vmin=-0.4, vmax=0.4, axis=None),
                 use_container_width=True, height=min(40 + 35 * len(yr), 760))

    st.subheader("Share of time spent in each company")
    st.dataframe(time_held(bt).style.format("{:.0%}"), use_container_width=True)

# ---------------------------------------------------------------- holdings
with tab3:
    seen = []
    for r in bt.results:
        seen += [t for t in r.holding.dropna().unique() if t not in seen]
    cc = {t: (SERIES[i] if i < len(SERIES) else OTHER) for i, t in enumerate(seen)}
    tl = pd.concat([holding_periods(r, bt.benchmark, names).assign(Strategy=r.config.name) for r in bt.results])
    tl["From"], tl["To"] = pd.to_datetime(tl["From"]), pd.to_datetime(tl["To"])
    fig = px.timeline(tl, x_start="From", x_end="To", y="Strategy", color="Company",
                      color_discrete_map={names.get(t, t): c for t, c in cc.items()},
                      hover_data={"Return": ":+.1%", "Index return": ":+.1%", "Strategy": False})
    fig.update_yaxes(autorange="reversed")
    base_layout(fig, "Which company each strategy held", height=120 + 70 * len(bt.results))
    fig.update_layout(hovermode="closest")
    st.plotly_chart(fig, use_container_width=True)

    pick = st.selectbox("Strategy", [r.config.name for r in bt.results], index=len(bt.results) - 1)
    r = next(r for r in bt.results if r.config.name == pick)
    hp = holding_periods(r, bt.benchmark, names)
    st.markdown(f"**Holding periods — {pick}** ({len(r.trades)} trades)")
    st.dataframe(hp.style.format({"Return": "{:+.1%}", "Index return": "{:+.1%}", "Excess": "{:+.1%}"}),
                 use_container_width=True, hide_index=True)
    st.markdown("**Trade log**")
    st.dataframe(r.trades.assign(sold=r.trades["sold"].map(lambda t: names.get(t, t) if isinstance(t, str) else "-"),
                                 bought=r.trades["bought"].map(lambda t: names.get(t, t)))
                 .style.format({"value_after": money + "{:,.0f}", "tax_paid": money + "{:,.0f}"}), use_container_width=True, hide_index=True)
    st.markdown("**Every change of #1 in the index**")
    st.dataframe(leader_history(bt), use_container_width=True, hide_index=True)

# ---------------------------------------------------------------- all indices
with tab4:
    st.caption("Same settings, run on every index. Takes a while the first time while data downloads.")
    if st.button("Run all indices"):
        rows = []
        prog = st.progress(0.0)
        for n, k in enumerate(INDICES, 1):
            prog.progress(n / len(INDICES), f"{INDICES[k].name}")
            b2 = run_backtest(k, start=str(start), capital=float(capital), strategies=tuple(strategies),
                              md=market_data(k), tax=tax)
            s2 = summary_table(b2)
            for name, row in s2.iterrows():
                rows.append({"Index": INDICES[k].name, "Strategy": "Index" if name == b2.benchmark_label else name,
                             "CAGR": row[cagr_col], "CAGR vs index": row[vs_col],
                             "Max drawdown": row["Max drawdown"], "Trades": row["Trades"]})
        allres = pd.DataFrame(rows)
        piv = allres.pivot(index="Index", columns="Strategy", values="CAGR")
        strat_cols = [c for c in piv.columns if c != "Index"]
        fig = go.Figure([go.Bar(x=piv.index, y=piv[c], name=c,
                                marker_color=colors.get(c, INDEX_INK if c == "Index" else OTHER)) for c in
                         strat_cols + ["Index"]])
        fig.update_layout(barmode="group")
        st.plotly_chart(base_layout(fig, "CAGR by index and strategy", pct=True), use_container_width=True)
        st.dataframe(allres.style.format({"CAGR": "{:.1%}", "CAGR vs index": "{:+.1%}", "Max drawdown": "{:.1%}",
                                          "Trades": "{:.0f}"}), use_container_width=True, hide_index=True)

# ---------------------------------------------------------------- data notes
with tab5:
    st.markdown("""
**How market caps are estimated:** unadjusted price × shares outstanding on each day. Share counts come from
Yahoo Finance (~2015 onwards) spliced onto SEC filings (~2007 onwards, US companies). Before the first known
count, the earliest one is carried backwards.

**Candidate pool:** each index uses a hand-picked list of companies that have been, or come close to being, its
largest member, with approximate join/leave dates. Edit `leadertrack/indices.py` to add more.

**No look-ahead:** decisions use the closing market caps of day *t* and trade at that close.
""")
    st.dataframe(bt.md.quality, use_container_width=True)
