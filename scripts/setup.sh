#!/bin/bash
set -euo pipefail

echo "=== Checking dependencies ==="
for cmd in git make gcc g++ cmake; do
    command -v $cmd >/dev/null 2>&1 || { echo "Error: $cmd is required but not installed."; exit 1; }
done

echo "=== Setting up NSphere ==="
mkdir -p refs
(
    cd refs
    if [ ! -d "NSphere" ]; then
        git clone https://github.com/kris-sigurdson/NSphere.git
    fi
    cd NSphere
    # Фиксация версии NSphere для воспроизводимости (коммит 8f146665af4f1031d4c0c6008e034ec3de67afba)
    git checkout 8f146665af4f1031d4c0c6008e034ec3de67afba
    make all
)
echo "Done. NSphere built at refs/NSphere/bin/nsphere"
