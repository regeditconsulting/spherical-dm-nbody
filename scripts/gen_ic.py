#!/usr/bin/env python3
"""
Генерация начальных условий для сферически-симметричного NFW-гало.
Использует galpy для сэмплирования из аналитической функции распределения.
Изотропный случай. Усечение на r_t обязательно для конечности массы.
"""
import sys
import numpy as np
import galpy.df

def main():
    # Параметры NFW (в единицах: r_s = 1.0, G = 1.0)
    rs = 1.0
    rho0 = 1.0 / (4.0 * np.pi * rs**3) # Масса внутри rs равна 1.0
    rt = 10.0 * rs                      # Усечение
    N = 10000                           # Количество частиц для первого теста

    print(f"Initializing NFW halo: rs={rs}, rt={rt}, N={N}")
    
    # В galpy профиль NFW задается через массу или плотность.
    # Мы используем galpy.df.isotropicNFW для изотропной DF.
    # Замечание: galpy оперирует безразмерными единицами (ро = 1, vо = 1).
    # Для физической корректности нужно будет отмасштабировать.
    # Сейчас проверим работоспособность конвейера.
    try:
        # Инициализация изотропной модели NFW
        # (параметры: amax=rt/rs, normalize=True)
        df = galpy.df.isotropicNFW(amax=rt/rs)
        
        # Сэмплируем (x, v) 
        # В galpy сэмплирование из DF возвращает (R, vR, vT, z, vz, phi) в цилиндрических координатах.
        # Для сферической модели мы берем (R, vR, vT) и предполагаем z=0.
        # Но лучше взять сферические координаты напрямую.
        print("Sampling...")
        # Возвращает массив кортежей (x,v)
        # Для isotropicNFW метод sample возвращает (r, vr, vt) в сферической системе.
        samples = df.sample(n=N)
        
        # Сохраняем в текстовый формат для NSphere
        # Формат NSphere мы уточним ниже, пока сохраним сырые данные
        outfile = "data/ic_nfw.txt"
        np.savetxt(outfile, samples, header="r vr vt")
        print(f"Saved {N} particles to {outfile}")
        
    except Exception as e:
        print(f"Error during sampling: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
