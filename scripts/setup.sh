#!/bin/bash
set -euo pipefail

# Fixed version of NSphere for reproducibility
NSPHERE_REF="8f146665af4f1031d4c0c6008e034ec3de67afba"

echo "=== Checking dependencies ==="
for cmd in git make gcc g++ cmake; do
    command -v $cmd >/dev/null 2>&1 || { echo "Error: $cmd is required but not installed."; exit 1; }
done

echo "=== Setting up NSphere (ref: $NSPHERE_REF) ==="
mkdir -p refs
(
    cd refs
    if [ ! -d "NSphere" ]; then
        git clone https://github.com/kris-sigurdson/NSphere.git
    fi
    cd NSphere
    git checkout $NSPHERE_REF
    make all
)
echo "Done. NSphere built at refs/NSphere/bin/nsphere"
