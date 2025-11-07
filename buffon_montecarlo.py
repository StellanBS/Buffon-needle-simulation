"""
Buffon's Needle — Monte Carlo Simulation (Interactive Visualization)
--------------------------------------------------------------------
This program demonstrates Buffon's classic needle experiment for estimating π
using Monte Carlo sampling and a live visual simulation.

How it works:
- When you run the program, you will be prompted to enter how many needles to drop
- A pop-up window will appear, showing each randomized needle as it is dropped
- The simulation updates in real time with the current estimate of π

Run:
    python buffon_montecarlo.py
"""

import math, random
from dataclasses import dataclass
from typing import Tuple
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

# ---------- Data container ----------
@dataclass
class Needle:
    x: float
    y: float
    theta: float
    crosses: bool

# ---------- Core Monte Carlo logic ----------
def drop_one_needle(L: float, t: float,
                    xlim: Tuple[float, float],
                    ylim: Tuple[float, float],
                    rng: random.Random) -> Needle:
    x = rng.uniform(xlim[0] + L/2, xlim[1] - L/2)
    y = rng.uniform(ylim[0] + t/2, ylim[1] - t/2)
    theta = rng.uniform(0, math.pi)

    # Distance from the needle center to nearest line
    d_to_line = min((y % t), t - (y % t))
    crosses = (L/2) * math.sin(theta) >= d_to_line
    return Needle(x, y, theta, crosses)

def estimate_pi(crosses: int, total: int, L: float, t: float) -> float:
    if crosses == 0:
        return float("inf")
    return (2 * L * total) / (crosses * t)

# ---------- Visualization helpers ----------
def make_base_figure(xlim, ylim, t, title):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.set_title(title)
    for k in range(int(np.floor(ylim[0]/t))-1, int(np.ceil(ylim[1]/t))+2):
        ax.axhline(k * t, lw=1, alpha=0.3)
    return fig, ax

def draw_needle(ax, nd: Needle, L: float):
    dx, dy = (L/2)*np.cos(nd.theta), (L/2)*np.sin(nd.theta)
    x0, x1 = nd.x - dx, nd.x + dx
    y0, y1 = nd.y - dy, nd.y + dy
    color = "red" if nd.crosses else "blue"
    (ln,) = ax.plot([x0, x1], [y0, y1], lw=1.2, alpha=0.9, color=color)
    return ln

# ---------- Animation ----------
def run_simulation(N: int, speed_ms: int = 15, L: float = 1.0, t: float = 1.0):
    if L > t:
        raise ValueError("Requires L ≤ t")

    rng = random.Random()  # fresh random sequence every run
    xlim, ylim = (-3, 3), (-3, 3)
    fig, ax = make_base_figure(xlim, ylim, t, "Buffon's Needle - Monte Carlo Simulation")
    text_pi = ax.text(0.02, 0.97, "", transform=ax.transAxes, va="top", ha="left")
    text_counts = ax.text(0.02, 0.90, "", transform=ax.transAxes, va="top", ha="left")

    state = {"i": 0, "crosses": 0}

    def init():
        text_pi.set_text("")
        text_counts.set_text("")
        return [text_pi, text_counts]

    def update(_):
        state["i"] += 1
        nd = drop_one_needle(L, t, xlim, ylim, rng)
        if nd.crosses:
            state["crosses"] += 1
        ln = draw_needle(ax, nd, L)
        pi_hat = estimate_pi(state["crosses"], state["i"], L, t)
        text_pi.set_text(f"π ≈ {pi_hat:.5f}")
        text_counts.set_text(f"Needles: {state['i']}  Crossings: {state['crosses']}")
        return [ln, text_pi, text_counts]

    ani = animation.FuncAnimation(
        fig,
        update,
        init_func=init,
        frames=N,
        interval=max(1, speed_ms),
        blit=False,
        repeat=False,
    )

    plt.show()

# ---------- Main ----------
if __name__ == "__main__":
    print("Welcome to Buffon's Needle Monte Carlo Simulator!")
    print("Each run will be random and yield a different π estimate.\n")

    try:
        N = int(input("How many needles should be dropped? ").strip())
    except Exception:
        N = 300
        print("Invalid input. Using default N=300.\n")

    run_simulation(N, speed_ms=10)