import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import glob

files = glob.glob("data/Psiprofile_nfw_long_*.dat")
if not files:
    print("Error: profile file not found.")
    exit()

filepath = files[0]
# Читаем как массив float32
raw_data = np.fromfile(filepath, dtype=np.float32)

# В NSphere Psiprofile обычно 4 колонки: r, rho, M, Psi (или 3: r, rho, M)
# Проверяем делимость, чтобы не упасть
if len(raw_data) % 4 == 0:
    cols = 4
    data = raw_data.reshape(-1, cols)
    r = data[:, 0]
    rho = data[:, 1]
    # M = data[:, 2]
    # Psi = data[:, 3]
elif len(raw_data) % 3 == 0:
    cols = 3
    data = raw_data.reshape(-1, cols)
    r = data[:, 0]
    rho = data[:, 1]
elif len(raw_data) % 2 == 0:
    cols = 2
    data = raw_data.reshape(-1, cols)
    r = data[:, 0]
    rho = data[:, 1]
else:
    print(f"Error: cannot determine shape for {len(raw_data)} floats")
    exit()

print(f"Loaded {cols} columns from {filepath}. Total bins: {len(r)}")

# Параметры NFW
rs = 1.0
M_halo = 1.0e9
rho0 = M_halo / (4.0 * np.pi * rs**3)
rho_an = rho0 / ((r/rs) * (1.0 + r/rs)**2)

# Убираем нули и отрицательные значения для логарифмического графика
mask = (r > 0) & (rho > 0)
r, rho, rho_an = r[mask], rho[mask], rho_an[mask]

plt.figure(figsize=(8, 6))
plt.loglog(r, rho, 'o', markersize=4, alpha=0.7, label='NSphere (N=50k, t=10 Tdyn)')
plt.loglog(r, rho_an, 'k-', linewidth=2, label='Analytical NFW')
plt.xlabel('r [kpc]')
plt.ylabel(r'\(\rho\) \([M_\odot / kpc^3]\)')
plt.title('Stability of NFW Halo over 10 Dynamical Times')
plt.legend()
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.savefig('results/stability_overlay.png', dpi=150)
print("Saved overlay plot to results/stability_overlay.png")
