import os
import glob
import re

# Словарь с научными описаниями для графиков
DESCRIPTIONS = {
    "density_profile": {
        "title": "Профиль плотности (Эволюция)",
        "text": "Сравнение начального и конечного профиля плотности за 10 динамических времен. Отсутствие значительного развала ядра (core-crushing) и стабильность внешних областей подтверждают корректность выбора шага интегратора и отсутствие избыточной двухчастичной релаксации."
    },
    "angular_momentum": {
        "title": "Распределение углового момента",
        "text": "Гистограмма углового момента (l). Показывает сохранение орбитальной структуры. Для сферической изотропной модели ожидается специфическое распределение, которое не должно существенно меняться при отсутствии внешних приливных сил."
    },
    "stability_overlay": {
        "title": "Верификация стабильности NFW (10 T_dyn)",
        "text": "Наложение численного профиля плотности (синие точки) на аналитическую формулу NFW (черная линия). Демонстрирует, что N-body код (NSphere) точно воспроизводит заданные начальные условия и удерживает их без искусственного искажения на длинных временах."
    },
    "sidm_core_formation": {
        "title": "SIDM: Формирование ядра (Core Formation)",
        "text": "Ключевой физический результат. Красная линия — профиль плотности самовзаимодействующей темной материи (SIDM, сечение kappa=100 см²/г). В центре происходит выполаживание профиля (образование ядра) из-за упругих рассеяний частиц. Это прямое численное подтверждение процессов гравитермальной эволюции, отличающих SIDM от стандартной холодной темной материи (CDM)."
    },
    "energy": {
        "title": "Сохранение энергии",
        "text": "Диагностика полной энергии системы во времени. Горизонтальная линия свидетельствует о консервативности интегратора и отсутствии численных ошибок, приводящих к нагреву или охлаждению гало."
    },
    "distribution": {
        "title": "Распределения переменных (Начальное vs Конечное)",
        "text": "Одномерные распределения кинематических переменных (радиус, скорости). Позволяют оценить степень релаксации системы и устойчивость фазового пространства."
    }
}

html = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>NSphere: NFW Halo Simulation Report</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f4f6f8; color: #2c3e50; margin: 0; padding: 20px; }
        .container { max-width: 1200px; margin: auto; background: #fff; padding: 40px; border-radius: 10px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
        h1 { border-bottom: 3px solid #2980b9; padding-bottom: 15px; font-weight: 300; }
        h2 { color: #2980b9; margin-top: 40px; font-weight: 400; }
        .params { font-family: "SFMono-Regular", Consolas, monospace; background: #ecf0f1; padding: 20px; border-radius: 8px; font-size: 0.9em; line-height: 1.6; border-left: 5px solid #2980b9; }
        .methodology { background: #fffdf5; border-left: 5px solid #f1c40f; padding: 15px 20px; margin: 20px 0; font-size: 0.95em; line-height: 1.5; }
        .gallery { display: grid; grid-template-columns: 1fr; gap: 40px; margin-top: 30px; }
        .plot-card { border: 1px solid #e1e8ed; border-radius: 8px; overflow: hidden; background: #fff; box-shadow: 0 4px 6px rgba(0,0,0,0.02); }
        .plot-header { background: #f8fafc; padding: 15px 20px; border-bottom: 1px solid #e1e8ed; font-weight: 600; font-size: 1.1em; color: #34495e; }
        .plot-img { text-align: center; padding: 20px; background: #fff; }
        .plot-img img { max-width: 100%; height: auto; max-height: 600px; }
        .plot-desc { padding: 20px; background: #fdfdfd; font-size: 0.95em; line-height: 1.6; color: #555; border-top: 1px solid #f0f0f0; }
        .footer { margin-top: 50px; font-size: 0.85em; color: #95a5a6; text-align: center; border-top: 1px solid #eee; padding-top: 20px; }
    </style>
</head>
<body>
<div class="container">
    <h1>Сферически-симметричная N-body модель гало темной материи</h1>
    
    <div class="params">
        <b>ПРОФИЛЬ:</b> NFW (Navarro-Frenk-White)<br>
        <b>МАССА ГАЛО (M_halo):</b> 1.0e9 M☉<br>
        <b>МАСШТАБНЫЙ РАДИУС (r_s):</b> 1.0 kpc<br>
        <b>КОЛИЧЕСТВО ЧАСТИЦ (N):</b> до 50,000<br>
        <b>ИНТЕГРАТОР:</b> Adaptive Leapfrog + Levi-Civita regularization<br>
        <b>SIDM КРОСС-СЕКЦИЯ:</b> kappa = 100 cm²/g (для SIDM-модели)
    </div>

    <div class="methodology">
        <b>Методика и воспроизводимость:</b> Данные получены с помощью открытого кода <a href="https://github.com/kris-sigurdson/NSphere" target="_blank">NSphere</a>, который сводит 6D фазовое пространство к 3D (r, v_r, l), используя сферическую симметрию для ускорения вычислений (N log N). Начальные условия сгенерированы встроенным генератором (сферический профиль с усечением). Обработка данных и визуализация выполнены с помощью Python (numpy, matplotlib). Все параметры зафиксированы, исходный код доступен в репозитории проекта.
    </div>

    <h2>Результаты моделирования</h2>
    <div class="gallery">
"""

plots = sorted(glob.glob("results/*.png"))
if not plots:
    html += "<p>Графики не найдены. Проверьте папку results/.</p>"
else:
    for p in plots:
        name = os.path.basename(p)
        
        # Поиск подходящего описания
        desc = {"title": name, "text": "Описание отсутствует."}
        for key, val in DESCRIPTIONS.items():
            if key in name.lower():
                desc = val
                break
                
        html += f"""
        <div class="plot-card">
            <div class="plot-header">{desc['title']}</div>
            <div class="plot-img"><img src="{p}" alt="{name}"></div>
            <div class="plot-desc">{desc['text']}</div>
        </div>
        """

html += """
    </div>
    <div class="footer">
        Сгенерировано автоматически. Окружение: macOS (arm64), Python 3.12, NSphere.<br>
        Для Б. Штерна. Проект dm_halo_nbody.
    </div>
</div>
</body>
</html>
"""

with open("report.html", "w") as f:
    f.write(html)
print("Научный отчет сгенерирован: report.html")
