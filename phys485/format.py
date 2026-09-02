"""
PHYS485 lab helpers: imports, SI prefixes, signal processing, and plotting.
Drop this at the top of a notebook with:  from lab_helpers import *
"""

# ── Libraries ────────────────────────────────────────────────
import math
import os
import csv

import numpy as np
import pandas as pd
import scipy
from scipy import stats
from scipy.stats import linregress, chi2
from scipy.optimize import curve_fit
import sympy as sp

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from tabulate import tabulate as tb
from IPython.display import display, Markdown, Image


# ── SI prefixes ──────────────────────────────────────────────
Y, Z, E, P, T, G, M, k, h, da = 1e24, 1e21, 1e18, 1e15, 1e12, 1e9, 1e6, 1e3, 1e2, 1e1
d, c, m, u, n, p, f, a, z, y = 1e-1, 1e-2, 1e-3, 1e-6, 1e-9, 1e-12, 1e-15, 1e-18, 1e-21, 1e-24


# ── Signal processing ────────────────────────────────────────
def rms(signal):
    """Root-mean-square of a signal array."""
    return np.sqrt(np.mean(np.square(signal)))


def vpp(signal):
    """Peak-to-peak voltage/amplitude."""
    return np.max(signal) - np.min(signal)


def dc(signal):
    """DC (mean) offset of a signal."""
    return np.mean(signal)


def do_fft(signal, dt):
    """Single-sided FFT: returns (freqs, amplitudes)."""
    freqs = np.fft.fftfreq(len(signal), dt)
    amps = np.abs(np.fft.fft(signal))
    half = len(signal) // 2
    return freqs[:half], amps[:half]


# ── Plot styling ─────────────────────────────────────────────
def look_nice(axis, xlabel, ylabel, title, caption=None):
    """Apply consistent labels/grid/legend to an axis, with an optional
    centered caption below the plot. Does NOT call plt.show() —
    call that yourself after any additional plotting on `axis`."""
    axis.set_xlabel(xlabel, size=12)
    axis.set_ylabel(ylabel, size=12)
    axis.set_title(title, size=16)
    axis.tick_params(axis="both", labelsize=10)
    axis.legend(loc="best")
    axis.grid(True)

    if caption:
        bbox = axis.get_position()
        caption_x = (bbox.x0 + bbox.x1) / 2
        caption_y = bbox.y0 - 0.16
        axis.figure.text(
            caption_x, caption_y, caption, ha="center", fontsize=10,
            bbox={"facecolor": "white", "alpha": 0.5, "pad": 5},
        )


def image_import(file_path, title, figure_caption=""):
    """Display an image file (e.g. circuit photo) with title + caption."""
    img = mpimg.imread(file_path)
    plt.imshow(img)
    plt.title(title)
    plt.axis("off")
    if figure_caption:
        plt.figtext(0.5, 0.01, figure_caption, ha="center", fontsize=10,
                    bbox={"facecolor": "white", "alpha": 0.5, "pad": 5})
    plt.show()


def show_screenshot(path, caption=""):
    """Display a saved screenshot inline (e.g. scope/DMM screen grab)."""
    display(Image(filename=path))
    if caption:
        print(caption)


def plot_signals(t, sig1, sig2, labels=("Signal 1", "Signal 2"), title="Signals"):
    """Quick two-trace time-domain plot."""
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(t, sig1, label=labels[0])
    ax.plot(t, sig2, label=labels[1])
    look_nice(ax, "Time (s)", "Amplitude", title)
    plt.show()


def plot_fft(signal, dt, title="FFT"):
    """Quick frequency-domain plot via do_fft()."""
    freqs, amps = do_fft(signal, dt)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(freqs, amps, label="Spectrum")
    look_nice(ax, "Frequency (Hz)", "Amplitude", title)
    plt.show()


# ── File I/O ─────────────────────────────────────────────────
def import_scope_csv(filepath, num_signals=2, skip_header=22):
    """Load an oscilloscope CSV export and plot each channel.
    Returns the raw data array (time in col 0, seconds)."""
    columns = tuple(range(1, num_signals + 2))
    data = np.genfromtxt(filepath, delimiter=",", skip_header=skip_header, usecols=columns)

    fig, ax = plt.subplots(figsize=(8, 6))
    colors = ["orange", "green", "blue", "red"]
    for i in range(num_signals):
        ax.plot(data[:, 0] * 1e6, data[:, i + 1], color=colors[i % len(colors)],
                 linestyle="", marker=".", markersize=4, label=f"V{i+1}")

    look_nice(ax, "Time (µs)", "Voltage (V)", "Oscilloscope Trace")
    plt.show()
    return data


def save_to_csv(data_dict, filename="data.csv"):
    """Save a dict of equal-length arrays/lists to CSV."""
    df = pd.DataFrame(data_dict)
    df.to_csv(filename, index=False)
    print(f"Saved to {filename}")