#!/bin/bash
# AttenSync Backend Startup Script

echo "Starting AttenSync Backend Server..."
cd "$(dirname "$0")/../src/backend"
python backend.py
