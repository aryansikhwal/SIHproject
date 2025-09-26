#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Script is in: $SCRIPT_DIR"
echo "Changing to project directory..."

cd "$SCRIPT_DIR"
echo "Current directory: $(pwd)"

echo "Contents of directory:"
ls -la

echo "Starting React development server..."
npm start
