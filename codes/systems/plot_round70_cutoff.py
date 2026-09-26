"""Plot chapter 12's synthetic cutoff model; requires matplotlib >= 3.6.

Run from repository root: python3 codes/systems/plot_round70_cutoff.py
Produces the book SVG and a temporary PNG preview specified via --preview.
The numerical lesson scripts remain dependency-free. No hardware or randomness.
"""
import argparse
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from network_cutoff import closed_form


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    ks = list(range(41))
    pairs = [closed_form(.1, k) for k in ks]
    wait, coherence = zip(*pairs)
    plt.rcParams.update({"font.size": 11, "svg.fonttype": "none", "svg.hashsalt": "round70-cutoff"})
    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.8), layout="constrained")
    fig.suptitle("Two-link memory cutoff: shorter storage costs more retries\n"
                 "Synthetic model: p = 0.1; slot = 1 ms; memory time = 20 ms; ideal herald and swap", fontsize=12)
    fig.supxlabel("Cutoff K (additional 1 ms attempts after the first link succeeds)")
    axes[0].plot(ks, wait, color="#0c6370", marker="o", markevery=5, label="Finite cutoff")
    axes[0].axhline(2/.1 - 1/(1-.9**2), color="#555555", linestyle="--", label="No cutoff: 14.74 ms")
    axes[0].set_ylabel("Mean completion time (ms)")
    axes[0].set_ylim(0, 110)
    axes[1].plot(ks, coherence, color="#945025", marker="s", markevery=5, label="Accepted-pair coherence")
    import math
    no_cutoff = .1/1.9 * (1+.9*math.exp(-.05))/(1-.9*math.exp(-.05))
    axes[1].axhline(no_cutoff, color="#555555", linestyle="--", label="No-cutoff limit")
    axes[1].set_ylabel("Mean extra-storage coherence factor (unitless)")
    axes[1].set_ylim(.6, 1.04)
    for ax in axes:
        ax.set_xlim(0, 40)
        ax.set_xticks(range(0, 41, 10))
        ax.grid(alpha=.2)
        ax.legend(fontsize=10)
    destination = root / "handbook/assets/round70-systems-cutoff.svg"
    fig.savefig(destination, metadata={"Date": None, "Description": "Analytic renewal model from chapter 12 section 6.4; not device data."})
    destination.write_text("\n".join(line.rstrip() for line in destination.read_text().splitlines()) + "\n")
    if args.preview:
        fig.savefig(args.preview, dpi=150)
    plt.close(fig)
    print(destination)


if __name__ == "__main__":
    main()
