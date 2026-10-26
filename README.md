# Spherical DM N-body Pipeline

**An engineering pipeline for fast, reproducible N-body simulations of dark matter halos.** Built on top of the [NSphere](https://github.com/kris-sigurdson/NSphere) solver, optimized for local machines (no cluster required).

📊 **[Live HTML Report](https://regeditconsulting.github.io/spherical-dm-nbody/report.html)** | 📄 **[PDF Version](report.pdf)**

---

## ⚠️ Scope & Limitations (Read First)

This project is an **engineering portfolio piece**, not a peer-reviewed physics paper. The focus is on reproducibility, fast prototyping, and data visualization.
-   **Physics Validation:** We do not claim new astrophysical discoveries. The stability of the NFW profile is a standard numerical check.
-   **Spherical Symmetry:** The 6D phase-space is reduced to 3D. This explicitly ignores mergers, tidal stripping, and non-radial instabilities.
-   **SIDM Cross-section:** The demo uses 100 cm²/g to force core formation quickly on a laptop. Realistic bounds (0.1 - 10 cm²/g) require much longer integration times.
-   **Resolution:** The inner cusp of the NFW profile is not resolved (Power et al. 2003 convergence radius applies).

---

## Demonstration Outputs

| *Stable NFW halo after 10 dynamical times* | *SIDM core formation (demo)* |
|---|---|
| ![NFW Stability](assets/nfw_stability.png) | ![SIDM Core](assets/sidm_core.png) |

---

## Performance Benchmark

Speed is the main feature of this pipeline. By reducing the phase space to 3D, we achieve the following execution times (1000 timesteps, Apple M-series chip):

| N (particles) | Time (seconds) |
|---|---|
| 1,000 | ~0.15 |
| 10,000 | ~0.80 |
| 50,000 | ~5.50 |

*(Run `python scripts/benchmark.py` to reproduce on your hardware).*

---

## Quick Start

We provide a setup script to automate the installation of the NSphere backend.

1. Clone this repository:
    git clone https://github.com/regeditconsulting/spherical-dm-nbody.git
    cd spherical-dm-nbody

2. Setup dependencies and build NSphere:
    brew install gsl fftw eigen boost cmake
    python3 -m venv env/local/venv
    source env/local/venv/bin/activate
    pip install -r requirements.txt
    ./scripts/setup.sh

### Running the Demos

**Collisionless NFW (CDM):**
    ./refs/NSphere/bin/nsphere \
        --nparticles 50000 --ntimesteps 5000 --tfinal 10 \
        --profile nfw --halo-mass 1.0e9 --scale-radius 1.0 \
        --tag nfw_long --method 1 --sort 1

**Self-Interacting Dark Matter (SIDM):**
    ./refs/NSphere/bin/nsphere \
        --nparticles 30000 --ntimesteps 2000 --tfinal 5 \
        --profile nfw --halo-mass 1.0e9 --scale-radius 1.0 \
        --tag sidm_test --sidm --sidm-kappa 100.0 --method 1 --sort 1

**Generate the Report:**
    python scripts/make_report.py
    open report.html

---

## Architecture & Engineering Details

-   **Parser (`scripts/overlay_nfw.py`):** NSphere outputs raw binary `float32` arrays. We wrote a custom parser (`np.fromfile` + `reshape`) to bypass missing text-based tools.
-   **Report Generator (`scripts/make_report.py`):** Automatically compiles plots and metrics into a publication-style HTML file.
-   **Tests (`tests/`):** Unit tests for the binary parser to ensure format stability across updates.

## License

This project is licensed under the MIT License. It uses NSphere (Apache-2.0). See `NOTICE` for details.
