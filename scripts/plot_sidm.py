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

def read_profile(pattern):
    files = glob.glob(f"data/Psiprofile_{pattern}_*.dat")
    if not files: return None, None
    raw = np.fromfile(files[0], dtype=np.float32)
    cols = 4 if len(raw) % 4 == 0 else 2
    data = raw.reshape(-1, cols)
    return data[:, 0], data[:, 1]

r_sidm, rho_sidm = read_profile("sidm_test")
r_init, rho_init = read_profile("nfw_long")

fig, ax = plt.subplots(figsize=(9, 6))

r_th = np.logspace(-1, 1, 100)
rho0 = 1.0e9 / (4.0 * np.pi * 1.0**3)
rho_th = rho0 / (r_th * (1 + r_th)**2)
ax.loglog(r_th, rho_th, 'k:', linewidth=2.5, label='Analytical NFW (Initial)')

if r_init is not None:
    mask = (r_init > 0) & (rho_init > 0)
    ax.loglog(r_init[mask], rho_init[mask], 'C0-', linewidth=2, alpha=0.7, label='Collisionless N-body (NFW)')

if r_sidm is not None:
    mask = (r_sidm > 0) & (rho_sidm > 0)
    ax.loglog(r_sidm[mask], rho_sidm[mask], 'C1-', linewidth=3, label='SIDM ($\\kappa=100\\,$cm$^2$ g$^{-1}$)')

ax.set_xlabel('Radius  $r$  [kpc]')
ax.set_ylabel(r'Density  $\rho$  [$M_\odot$ kpc$^{-3}$]')
ax.set_title('SIDM: Core Formation vs Collisionless NFW', fontsize=16)
ax.legend(frameon=True, loc='lower left')
ax.grid(True, which='both', ls='--', alpha=0.4)
ax.text(0.05, 0.95, r'$N=3\\times10^4,\\; t_{\\rm final}=5\\,T_{\\rm dyn}$', transform=ax.transAxes, fontsize=12, va='top')
plt.tight_layout()
plt.savefig('results/sidm_core_formation.png', dpi=150)
print("Saved: results/sidm_core_formation.png")
