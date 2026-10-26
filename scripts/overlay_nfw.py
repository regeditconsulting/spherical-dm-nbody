import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import glob

plt.rcParams.update({
    'font.size': 14,
    'axes.labelsize': 15,
    'legend.fontsize': 12,
    'xtick.labelsize': 13,
    'ytick.labelsize': 13,
    'font.family': 'serif',
    'mathtext.fontset': 'cm',
})

files = glob.glob("data/Psiprofile_nfw_long_*.dat")
if not files:
    print("Error: profile file not found.")
    exit()

raw = np.fromfile(files[0], dtype=np.float32)
cols = 4 if len(raw) % 4 == 0 else 2
data = raw.reshape(-1, cols)
r, rho = data[:, 0], data[:, 1]

rs = 1.0
rho0 = 1.0e9 / (4.0 * np.pi * rs**3)
rho_an = rho0 / ((r/rs) * (1.0 + r/rs)**2)
mask = (r > 0) & (rho > 0)
r, rho, rho_an = r[mask], rho[mask], rho_an[mask]

fig, ax = plt.subplots(figsize=(8, 6))
ax.loglog(r, rho, 'o', markersize=5, markerfacecolor='C0', markeredgecolor='C0', alpha=0.75, label='NSphere (N=50k, t=10 T$_{\\rm dyn}$)')
ax.loglog(r, rho_an, 'k-', linewidth=2.5, label='Analytical NFW')
ax.set_xlabel('Radius  $r$  [kpc]')
ax.set_ylabel(r'Density  $\rho$  [$M_\odot$ kpc$^{-3}$]')
ax.set_title('Stability of NFW Halo over 10 Dynamical Times', fontsize=16)
ax.legend(frameon=True, loc='lower left')
ax.grid(True, which='both', ls='--', alpha=0.4)
ax.text(0.05, 0.95, r'$M_{\\rm halo}=10^9\\,M_\\odot,\\; r_s=1\\,$kpc', transform=ax.transAxes, fontsize=12, va='top')
plt.tight_layout()
plt.savefig('results/stability_overlay.png', dpi=150)
print("Saved: results/stability_overlay.png")
