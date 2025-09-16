#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
cd "$SCRIPT_DIR"
echo "Starting React development server from: $(pwd)"
echo "Package.json exists: $(test -f package.json && echo "YES" || echo "NO")"
ls -la | head -5
npm start
