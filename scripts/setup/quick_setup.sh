#!/bin/bash
# Quick Start Script for AttenSync
# Run this after cloning the repository

echo "🚀 AttenSync Quick Setup Script"
echo "=================================="

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Create virtual environment
echo "📦 Creating Python virtual environment..."
python -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install Python dependencies
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt

# Initialize database
echo "🗄️ Initializing database with sample data..."
python initialize_system.py

# Install Node.js dependencies
echo "⚛️ Installing React dependencies..."
cd client
npm install
cd ..

echo ""
echo "🎉 Setup Complete!"
echo "==================="
echo ""
echo "To run the application:"
echo "1️⃣ Backend:  python backend.py"
echo "2️⃣ Frontend: cd client && npm start"
echo ""
echo "Then visit: http://localhost:3000"
echo ""
echo "For RFID hardware: python direct_esp32_connection.py"
echo ""
echo "Happy coding! 🚀"