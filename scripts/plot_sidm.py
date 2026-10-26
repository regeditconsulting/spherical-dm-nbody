import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import glob

def read_profile(pattern):
    files = glob.glob(f"data/Psiprofile_{pattern}_*.dat")
    if not files: return None, None
    raw = np.fromfile(files[0], dtype=np.float32)
    cols = 4 if len(raw) % 4 == 0 else 2
    data = raw.reshape(-1, cols)
    return data[:, 0], data[:, 1]

r_sidm, rho_sidm = read_profile("sidm_test")
r_init, rho_init = read_profile("nfw_long") # берем изотропный для сравнения

plt.figure(figsize=(9, 6))

# Исходный аналитический NFW (эталон)
r_th = np.logspace(-1, 1, 100)
rho0 = 1.0e9 / (4.0 * np.pi * 1.0**3)
rho_th = rho0 / (r_th * (1 + r_th)**2)
plt.loglog(r_th, rho_th, 'k:', linewidth=2, label='Analytical NFW (Initial)')

if r_init is not None:
    mask = (r_init > 0) & (rho_init > 0)
    plt.loglog(r_init[mask], rho_init[mask], 'b-', linewidth=2, alpha=0.6, label='Collisionless N-body (NFW)')

if r_sidm is not None:
    mask = (r_sidm > 0) & (rho_sidm > 0)
    plt.loglog(r_sidm[mask], rho_sidm[mask], 'r-', linewidth=2.5, label='SIDM (kappa=100, Core Formation)')

plt.xlabel('r [kpc]')
plt.ylabel(r'\(\rho\) \([M_\odot / kpc^3]\)')
plt.title('SIDM: Core Formation vs Collisionless NFW')
plt.legend()
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.savefig('results/sidm_core_formation.png', dpi=150)
print("Saved: results/sidm_core_formation.png")
