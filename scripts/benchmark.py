import subprocess
import time

print("| N (particles) | Steps | Time (seconds) |")
print("|---|---|---|")

for n, steps in [(1000, 1000), (10000, 1000), (50000, 1000), (50000, 5000)]:
    start = time.time()
    subprocess.run([
        "./refs/NSphere/bin/nsphere",
        "--nparticles", str(n),
        "--ntimesteps", str(steps),
        "--tfinal", "10",
        "--profile", "nfw",
        "--tag", f"bench_{n}_{steps}"
    ], capture_output=True)
    end = time.time()
    print(f"| {n} | {steps} | ~{end - start:.2f} |")
