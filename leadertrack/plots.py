"""Matplotlib charts: the animated race chart plus static comparison charts."""

from __future__ import annotations

from pathlib import Path

import matplotlib

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd
from matplotlib.animation import FuncAnimation, PillowWriter

from .analysis import Backtest, rolling_excess, yearly_returns

# Validated categorical palette (fixed order). The index is drawn in neutral ink.
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
INDEX_INK = "#3d3d3a"
OTHER = "#b8b7b0"
SURFACE = "#fcfcfb"
TEXT, TEXT2, GRID = "#0b0b0b", "#52514e", "#e6e5e0"

plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "axes.edgecolor": GRID, "axes.labelcolor": TEXT2, "xtick.color": TEXT2, "ytick.color": TEXT2,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8, "axes.spines.top": False,
    "axes.spines.right": False, "font.size": 10, "axes.titlesize": 12, "axes.titleweight": "bold",
    "axes.titlecolor": TEXT, "legend.frameon": False, "lines.linewidth": 2,
})


def series_colors(bt: Backtest) -> dict[str, str]:
    colors = {r.config.name: SERIES[i % len(SERIES)] for i, r in enumerate(bt.results)}
    colors[bt.benchmark_label] = INDEX_INK
    return colors


def company_colors(bt: Backtest) -> dict[str, str]:
    """Colour per company, assigned by first appearance across strategies (max 8, rest grey)."""
    seen: list[str] = []
    for r in bt.results:
        for t in r.holding.dropna():
            if t not in seen:
                seen.append(t)
    return {t: (SERIES[i] if i < len(SERIES) else OTHER) for i, t in enumerate(seen)}


def _money(ax, currency: str):
    sym = {"USD": "$", "GBP": "£", "EUR": "€"}.get(currency, "")
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda v, _: f"{sym}{v:,.0f}"))


# ---------------------------------------------------------------- animation
def animate(bt: Backtest, out_path: Path | None = None, show: bool = True, frames: int = 240, fps: int = 24):
    """The 'moving graph': portfolio values racing through time vs the index."""
    eq = bt.equity
    eq = eq.iloc[np.unique(np.linspace(0, len(eq) - 1, min(frames, len(eq))).astype(int))]
    colors = series_colors(bt)
    names = bt.names()
    holdings = {r.config.name: r.holding.reindex(eq.index, method="ffill") for r in bt.results}

    fig, ax = plt.subplots(figsize=(11, 6.2))
    fig.subplots_adjust(right=0.78, top=0.86)
    ax.set_yscale("log")
    _money(ax, bt.index.currency)
    ax.set_xlim(eq.index[0], eq.index[-1] + (eq.index[-1] - eq.index[0]) * 0.02)
    ax.set_ylim(eq.min().min() * 0.85, eq.max().max() * 1.25)
    fig.suptitle(f"Always own the #1 company vs the {bt.index.name}", x=0.06, ha="left",
                 fontsize=15, fontweight="bold", color=TEXT)
    sub = fig.text(0.06, 0.905, f"Growth of {bt.capital:,.0f} {bt.index.currency}"
                   + (f" + {bt.monthly:,.0f} a month" if bt.monthly else "") + ", dividends reinvested. "
                   "[brackets] = company held right now", fontsize=10, color=TEXT2)
    date_txt = ax.text(0.02, 0.95, "", transform=ax.transAxes, fontsize=20, fontweight="bold", color=TEXT2, alpha=0.6,
                       va="top")

    lines, dots, labels = {}, {}, {}
    for col in eq.columns:
        lw = 2.6 if col == bt.benchmark_label else 2
        (lines[col],) = ax.plot([], [], color=colors[col], lw=lw, label=col)
        (dots[col],) = ax.plot([], [], "o", color=colors[col], ms=8, mec=SURFACE, mew=2)
        labels[col] = ax.text(0, 0, "", color=TEXT, fontsize=9, va="center", clip_on=False)
    ax.legend(loc="lower right", fontsize=9)

    def update(i):
        sl = eq.iloc[: i + 1]
        d = sl.index[-1]
        date_txt.set_text(f"{d:%b %Y}")
        for col in eq.columns:
            lines[col].set_data(sl.index, sl[col])
            dots[col].set_data([d], [sl[col].iloc[-1]])
            tag = ""
            if col in holdings:
                t = holdings[col].iloc[i]
                tag = f"  [{names.get(t, t)}]" if isinstance(t, str) else ""
            labels[col].set_position((d + (eq.index[-1] - eq.index[0]) * 0.01, sl[col].iloc[-1]))
            labels[col].set_text(f"{sl[col].iloc[-1]:,.0f}{tag}")
        return [*lines.values(), *dots.values(), *labels.values(), date_txt, sub]

    anim = FuncAnimation(fig, update, frames=len(eq), interval=1000 / fps, blit=False, repeat=False)
    if out_path:
        anim.save(out_path, writer=PillowWriter(fps=fps))
        update(len(eq) - 1)
        fig.savefig(Path(out_path).with_suffix(".final.png"), dpi=130)
    if show and matplotlib.get_backend().lower() not in ("agg", "pdf", "svg"):
        anim = FuncAnimation(fig, update, frames=len(eq), interval=1000 / fps, blit=False, repeat=False)
        plt.show()
    plt.close(fig)
    return anim


# ---------------------------------------------------------------- static charts
def growth_chart(bt: Backtest, ax):
    eq, colors = bt.equity, series_colors(bt)
    for col in eq.columns:
        ax.plot(eq.index, eq[col], color=colors[col], lw=2.6 if col == bt.benchmark_label else 2, label=col)
        ax.annotate(f"{eq[col].iloc[-1]:,.0f}", (eq.index[-1], eq[col].iloc[-1]), xytext=(4, 0),
                    textcoords="offset points", fontsize=8, color=TEXT, va="center")
    if bt.monthly:
        paid = bt.bench_flows.cumsum().reindex(eq.index).ffill()
        ax.plot(paid.index, paid, color=TEXT2, lw=1.2, ls="--", label="Money paid in")
    ax.set_yscale("log")
    _money(ax, bt.index.currency)
    ax.set_title(f"Growth of {bt.capital:,.0f}" + (f" + {bt.monthly:,.0f} a month" if bt.monthly else "")
                 + " (log scale)", loc="left")
    ax.legend(fontsize=8, loc="upper left")


def drawdown_chart(bt: Backtest, ax):
    eq, colors = bt.nav, series_colors(bt)
    dd = eq / eq.cummax() - 1
    for col in dd.columns:
        ax.plot(dd.index, dd[col], color=colors[col], lw=1.5 if col != bt.benchmark_label else 2.2, label=col)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0, decimals=0))
    ax.set_title("Drawdown from previous peak", loc="left")


def yearly_chart(bt: Backtest, ax):
    yr = yearly_returns(bt)
    colors = series_colors(bt)
    n = len(yr.columns)
    w = 0.8 / n
    x = np.arange(len(yr))
    for i, col in enumerate(yr.columns):
        ax.bar(x + (i - (n - 1) / 2) * w, yr[col], width=w * 0.9, color=colors[col], label=col)
    ax.axhline(0, color=TEXT2, lw=0.8)
    ax.set_xticks(x, [str(y) for y in yr.index], rotation=90, fontsize=8)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0, decimals=0))
    ax.set_title("Calendar-year returns", loc="left")
    ax.grid(axis="x", visible=False)


def rolling_chart(bt: Backtest, ax):
    rx = rolling_excess(bt)
    colors = series_colors(bt)
    for col in rx.columns:
        ax.plot(rx.index, rx[col], color=colors[col], lw=1.5, label=col)
    ax.axhline(0, color=INDEX_INK, lw=1.2)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0, decimals=0))
    ax.set_title("Rolling 1-year return minus the index", loc="left")


def holdings_chart(bt: Backtest, ax):
    names = bt.names()
    cc = company_colors(bt)
    for row, r in enumerate(bt.results):
        h = r.holding.dropna()
        block = (h != h.shift()).cumsum()
        for _, seg in h.groupby(block):
            t = seg.iloc[0]
            start = matplotlib.dates.date2num(seg.index[0])
            width = matplotlib.dates.date2num(seg.index[-1]) - start + 1
            ax.broken_barh([(start, width)], (row - 0.38, 0.76), facecolors=cc[t], edgecolor=SURFACE, linewidth=0.6)
    ax.set_yticks(range(len(bt.results)), [r.config.name for r in bt.results], fontsize=9)
    ax.invert_yaxis()
    ax.xaxis_date()
    ax.grid(axis="y", visible=False)
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in cc.values()]
    ax.legend(handles, [names.get(t, t) for t in cc], ncol=min(len(cc), 8), fontsize=8,
              loc="upper center", bbox_to_anchor=(0.5, -0.12))
    ax.set_title("Which company each strategy held", loc="left")


def dashboard(bt: Backtest, out_path: Path):
    fig = plt.figure(figsize=(15, 15))
    gs = fig.add_gridspec(4, 2, height_ratios=[1.3, 1, 1, 0.75], hspace=0.45, wspace=0.18, top=0.95)
    growth_chart(bt, fig.add_subplot(gs[0, :]))
    drawdown_chart(bt, fig.add_subplot(gs[1, 0]))
    rolling_chart(bt, fig.add_subplot(gs[1, 1]))
    yearly_chart(bt, fig.add_subplot(gs[2, :]))
    holdings_chart(bt, fig.add_subplot(gs[3, :]))
    fig.suptitle(f"{bt.index.name}: always own the most valuable company vs the index "
                 f"({bt.equity.index[0]:%Y-%m-%d} to {bt.equity.index[-1]:%Y-%m-%d})",
                 x=0.06, ha="left", fontsize=15, fontweight="bold", y=0.985)
    fig.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


def save_individual(bt: Backtest, out_dir: Path):
    for name, fn, size in [("growth", growth_chart, (12, 6)), ("drawdown", drawdown_chart, (12, 5)),
                           ("yearly_returns", yearly_chart, (14, 5)), ("rolling_excess", rolling_chart, (12, 5)),
                           ("holdings_timeline", holdings_chart, (14, 3.6))]:
        fig, ax = plt.subplots(figsize=size)
        fn(bt, ax)
        fig.savefig(out_dir / f"{name}.png", dpi=120, bbox_inches="tight")
        plt.close(fig)
