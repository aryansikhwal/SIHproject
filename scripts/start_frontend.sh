#!/bin/bash
# AttenSync Frontend Startup Script

echo "Starting AttenSync Frontend..."
cd "$(dirname "$0")/../src/frontend"
npm start
