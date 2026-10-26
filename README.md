# Spherical DM N-body Pipeline

A reproducible pipeline for spherical N-body simulations of dark matter halos, based on the NSphere code. Optimized to run efficiently on standard laptops (no cluster required).

## Features

- **NFW Profile**: Initial conditions for Navarro-Frenk-White halos with configurable mass, scale radius, and cutoff.
- **Self-Interacting Dark Matter (SIDM)**: Core formation and gravothermal collapse via Monte Carlo scattering.
- **Fast**: N log N solver reduces 6D phase space to 3D (r, v_r, l).
- **Automated Reports**: Generates publication-style HTML reports with annotated plots.

## Quick Start

### Prerequisites
- macOS (arm64) or Linux
- Python 3.10+
- C compiler (clang/gcc), GNU Make, CMake
- Homebrew (for system dependencies)

### Installation

1. Clone the repository:
   git clone https://github.com/regeditconsulting/spherical-dm-nbody.git
   cd spherical-dm-nbody

2. Install system dependencies (macOS example):
   brew install gsl fftw eigen boost cmake

3. Set up Python environment:
   python3 -m venv env/local/venv
   source env/local/venv/bin/activate
   pip install numpy scipy matplotlib astropy galpy h5py tqdm psutil

4. Build NSphere from source (see refs/NSphere/README.md)

### Running a Simulation

./refs/NSphere/bin/nsphere \
    --nparticles 50000 --ntimesteps 5000 --tfinal 10 \
    --dtwrite 500 --nout 20 --profile nfw \
    --halo-mass 1.0e9 --scale-radius 1.0 --cutoff-factor 10.0 \
    --tag nfw_long --method 1 --sort 1

# Generate the HTML report
python scripts/make_report.py
open report.html

## License

This project is licensed under the MIT License. It uses NSphere, which is licensed under Apache-2.0 (see NOTICE).

## References

- Navarro, J. F., Frenk, C. S., & White, S. D. M. 1996, ApJ, 462, 563
- Kamionkowski, M., & Sigurdson, K. 2025, arXiv:2504.13996
- NSphere repository: https://github.com/kris-sigurdson/NSphere
