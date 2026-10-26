#!/usr/bin/env python3
"""
Генерация начальных условий для сферически-симметричного NFW-гало.
Использует galpy для сэмплирования из аналитической функции распределения.
Изотропный случай. Усечение на r_t обязательно для конечности массы.
"""
import sys
import numpy as np
from galpy import potential
from galpy.df import isotropicNFWdf

def main():
    rs = 1.0
    rt = 10.0 * rs
    N = 10000

    print(f"Initializing NFW halo: rs={rs}, rt={rt}, N={N}")

    # Потенциал NFW. amp=1.0, a=rs
    pot = potential.NFWPotential(amp=1.0, a=rs)

    # Изотропная функция распределения NFW
    df = isotropicNFWdf(pot=pot, rmax=rt)

    print("Sampling...")
    samples = df.sample(n=N)

    # Сохраняем в текстовый формат (r, vr, vt)
    outfile = "data/ic_nfw.txt"
    data = np.column_stack([samples.r(), samples.vr(), samples.vt()])
    np.savetxt(outfile, data, header="r vr vt", comments='')
    print(f"Saved {N} particles to {outfile}")

if __name__ == "__main__":
    main()
