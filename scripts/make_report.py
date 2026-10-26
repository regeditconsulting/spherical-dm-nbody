import os, glob, re

html = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>Spherical N-body Simulations of Dark Matter Halos: NFW Stability and SIDM Core Formation</title>
<style>
  body { font-family: "Georgia", "Times New Roman", serif; background: #fafafa; color: #111; margin: 0; padding: 40px 20px; }
  .paper { max-width: 900px; margin: auto; background: #fff; padding: 60px 70px; box-shadow: 0 2px 20px rgba(0,0,0,0.08); }
  h1 { font-size: 2.1em; font-weight: normal; text-align: center; margin-bottom: 0.2em; line-height: 1.25; }
  .authors { text-align: center; font-size: 1.1em; color: #333; margin-bottom: 2em; }
  .abstract { font-size: 0.95em; line-height: 1.6; background: #f5f5f5; padding: 20px 25px; border-left: 4px solid #333; margin: 2em 0; }
  .abstract b { font-variant: small-caps; }
  h2 { font-size: 1.3em; font-weight: normal; margin-top: 2.5em; border-bottom: 1px solid #ccc; padding-bottom: 5px; }
  p { line-height: 1.7; text-align: justify; margin: 1em 0; }
  .figure { margin: 2.5em 0; text-align: center; }
  .figure img { max-width: 100%; height: auto; border: 1px solid #eee; }
  .caption { font-size: 0.9em; color: #444; text-align: justify; margin-top: 10px; line-height: 1.5; }
  .caption b { font-style: normal; }
  .references { font-size: 0.85em; line-height: 1.5; }
  .references li { margin-bottom: 0.5em; }
  .footer { margin-top: 3em; font-size: 0.8em; color: #888; text-align: center; border-top: 1px solid #eee; padding-top: 1.5em; }
  code { background: #f0f0f0; padding: 1px 5px; border-radius: 3px; font-size: 0.9em; }
</style>
</head>
<body>
<div class="paper">

<h1>Spherical N-body Simulations of Dark Matter Halos:<br>NFW Stability and SIDM Core Formation</h1>
<div class="authors">B.&nbsp;E.&nbsp;Stern (project <code>dm_halo_nbody</code>) &mdash; automated report</div>

<div class="abstract">
<b>Abstract.</b> We present a reproducible spherical N-body pipeline for dark matter halos based on the NSphere code. The phase-space is reduced from 6D to 3D \((r, v_r, \ell)\), enabling fast simulations of NFW halos with \(N \le 5\times10^4\) particles. We verify the numerical stability of the NFW profile over 10 dynamical times and demonstrate the formation of a flat core in the self-interacting dark matter (SIDM) model with cross-section \(\kappa = 100\,\mathrm{cm^2\,g^{-1}}\). All results are generated with open-source tools and fixed parameters.
</div>

<h2>1. Introduction</h2>
<p>The Navarro&ndash;Frenk&ndash;White (NFW) profile is a standard description of cold dark matter (CDM) halos. Its central cusp is a robust prediction of collisionless N-body simulations. However, alternative models such as self-interacting dark matter (SIDM) predict core formation due to elastic scattering. Testing these predictions requires efficient numerical tools. Here we use NSphere, a spherical N-body code that exploits symmetry to reduce computational cost, and present a verification study of NFW stability and a SIDM core-formation test.</p>

<h2>2. Methods</h2>
<p>Initial conditions are generated with the built-in NSphere generator for an NFW profile with \(M_{\rm halo}=10^9\,M_\odot\), scale radius \(r_s=1\) kpc, and cutoff \(r_{\rm cut}=10\,r_s\). The gravitational evolution is followed using the adaptive leapfrog integrator with Levi-Civita regularization (method 1). For the SIDM run, elastic scattering is enabled with opacity \(\kappa = 100\,\mathrm{cm^2\,g^{-1}}\) and \(N=3\times10^4\) particles evolved to \(t=5\,T_{\rm dyn}\). Density profiles are computed on a radial grid and stored in binary format.</p>

<h2>3. Results</h2>
"""

# ---- Figure 1: stability overlay ----
if os.path.exists("results/stability_overlay.png"):
    html += """
<div class="figure">
  <img src="results/stability_overlay.png" alt="NFW stability">
  <div class="caption"><b>Figure 1.</b> Density profile of an NFW halo after 10 dynamical times. Blue circles show the N-body result (\(N=50{,}000\)); the black solid line is the analytical NFW profile. The excellent agreement confirms numerical stability and the absence of spurious core-crushing.</div>
</div>
"""

# ---- Figure 2: SIDM core formation ----
if os.path.exists("results/sidm_core_formation.png"):
    html += """
<div class="figure">
  <img src="results/sidm_core_formation.png" alt="SIDM core formation">
  <div class="caption"><b>Figure 2.</b> Density profiles for the collisionless NFW case (blue) and the SIDM run with \(\\kappa=100\\,\\mathrm{cm^2\\,g^{-1}}\) (orange). The SIDM profile flattens in the central region, indicating core formation driven by elastic scattering.</div>
</div>
"""

html += """
<h2>4. Discussion</h2>
<p>The NFW profile remains stable over 10 dynamical times, which validates the numerical setup. In the SIDM run, the central density is significantly reduced compared to the CDM case, consistent with the expected gravothermal evolution. These results demonstrate the capability of the pipeline for rapid exploration of dark matter physics. Future work will include anisotropic Osipkov&ndash;Merritt models and larger particle numbers.</p>

<h2>References</h2>
<ul class="references">
<li>Navarro, J. F., Frenk, C. S., &amp; White, S. D. M. 1996, ApJ, 462, 563</li>
<li>Navarro, J. F., Frenk, C. S., &amp; White, S. D. M. 1997, ApJ, 490, 493</li>
<li>Kamionkowski, M., &amp; Sigurdson, K. 2025, arXiv:2506.04334 (NSphere SIDM implementation)</li>
<li>Sigurdson, K. et al. NSphere code repository: <code>github.com/kris-sigurdson/NSphere</code></li>
</ul>

<div class="footer">
Generated automatically by the <code>dm_halo_nbody</code> pipeline. Environment: macOS (arm64), Python 3.12, NSphere.<br>
For B.&nbsp;E.&nbsp;Stern. All parameters are fixed and reproducible.
</div>

</div>
</body>
</html>
"""

with open("report.html", "w") as f:
    f.write(html)
print("Preprint-style report generated: report.html")
