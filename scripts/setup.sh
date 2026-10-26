#!/bin/bash
echo "Setting up NSphere..."
mkdir -p refs
cd refs
if [ ! -d "NSphere" ]; then
    git clone https://github.com/kris-sigurdson/NSphere.git
fi
cd NSphere
make all
echo "Done. NSphere built at refs/NSphere/bin/nsphere"
