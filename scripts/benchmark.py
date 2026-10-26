import subprocess
import time

print("| N (particles) | Time (seconds) |")
print("|---|---|")

for n in [1000, 10000, 50000]:
    start = time.time()
    subprocess.run([
        "./refs/NSphere/bin/nsphere",
        "--nparticles", str(n),
        "--ntimesteps", "1000",
        "--tfinal", "1",
        "--profile", "nfw",
        "--tag", f"bench_{n}"
    ], capture_output=True)
    end = time.time()
    print(f"| {n} | {end - start:.2f} |")
