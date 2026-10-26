import os
import glob

html = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>NSphere: NFW Halo Simulation</title>
    <style>
        body { font-family: -apple-system, sans-serif; background: #f9f9f9; color: #333; margin: 0; padding: 20px; }
        .container { max-width: 1000px; margin: auto; background: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        h1 { border-bottom: 2px solid #0056b3; padding-bottom: 10px; }
        .params { font-family: monospace; background: #f4f4f4; padding: 15px; border-radius: 5px; margin-bottom: 20px; line-height: 1.5; }
        .gallery { display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 20px; }
        .plot { border: 1px solid #ddd; padding: 10px; border-radius: 5px; text-align: center; }
        .plot img { max-width: 100%; height: auto; }
        .footer { margin-top: 40px; font-size: 0.8em; color: #777; text-align: center; }
    </style>
</head>
<body>
<div class="container">
    <h1>Сферически-симметричная N-body симуляция (NFW)</h1>
    <div class="params">
        <b>Профиль:</b> NFW<br>
        <b>Масса гало:</b> 1.0e9 M☉<br>
        <b>Масштабный радиус (rs):</b> 1.0 kpc<br>
        <b>Усечение (r_cut):</b> 10.0 rs<br>
        <b>Количество частиц:</b> 10,000<br>
        <b>Время симуляции:</b> 1.0 T_dyn<br>
        <b>Интегратор:</b> Adaptive Leapfrog + Levi-Civita (Method 1)
    </div>
    <h2>Галерея результатов</h2>
    <div class="gallery">
"""

plots = glob.glob("results/*.png")
if not plots:
    html += "<p>Графики не найдены. Проверьте папку results/.</p>"
else:
    for p in plots:
        name = os.path.basename(p)
        html += f'<div class="plot"><h3>{name}</h3><img src="{p}" alt="{name}"></div>\n'

html += """
    </div>
    <div class="footer">
        Сгенерировано автоматически. Окружение: macOS (arm64), NSphere, Clang 21.
    </div>
</div>
</body>
</html>
"""

with open("report.html", "w") as f:
    f.write(html)
print("Report generated: report.html")
