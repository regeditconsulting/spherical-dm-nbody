import numpy as np
import matplotlib
matplotlib.use('Agg') # headless mode для терминала
import matplotlib.pyplot as plt

# Загружаем сгенерированные данные (пропускаем заголовок)
data = np.loadtxt("data/ic_nfw.txt", skiprows=1)
r = data[:, 0]

# Биннинг по радиальным оболочкам (от 0.1 до 10 rs)
bins = np.logspace(np.log10(0.1), np.log10(10.0), 30)
hist, edges = np.histogram(r, bins=bins)
r_centers = 0.5 * (edges[1:] + edges[:-1])

# Вычисляем объем сферической оболочки
volume = (4.0/3.0) * np.pi * (edges[1:]**3 - edges[:-1]**3)
rho_num = hist / volume / len(r)

# Аналитический NFW (без усечения, для сравнения во внутренней области)
# rs=1, rho0=1/(4*pi) => rho(r) = 1 / (4*pi * r * (1+r)^2)
rho_an = 1.0 / (4.0 * np.pi * r_centers * (1.0 + r_centers)**2)

print("\n  r_center    rho_numerical    rho_analytical   ratio")
for i in range(len(r_centers)):
    if hist[i] > 0:
        print(f"  {r_centers[i]:.3f}       {rho_num[i]:.4e}      {rho_an[i]:.4e}    {rho_num[i]/rho_an[i]:.2f}")

plt.figure(figsize=(8,6))
plt.loglog(r_centers, rho_num, 'o', label='Numerical (N=10000)')
plt.loglog(r_centers, rho_an, 'k-', label='Analytical NFW')
plt.xlabel('r [rs]')
plt.ylabel('rho')
plt.legend()
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.savefig('data/profile_check.png', dpi=150)
print("\nSaved plot to data/profile_check.png")
