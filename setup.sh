#!/bin/bash

echo "🌱 AttenSync Frontend Setup Script 🌱"
echo "=================================="

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 14+ first."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

echo "✅ Node.js version: $(node --version)"
echo "✅ npm version: $(npm --version)"

# Navigate to project directory
cd "$(dirname "$0")"

echo ""
echo "📦 Installing dependencies..."
npm install

echo ""
echo "🎨 Setting up Tailwind CSS..."
# The dependencies should already be installed from package.json

echo ""
echo "🔧 Creating environment file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Environment file created from template"
else
    echo "⚠️  Environment file already exists"
fi

echo ""
echo "🚀 Starting development server..."
echo "The application will open in your browser at http://localhost:3000"
echo ""
echo "📋 Available commands:"
echo "  npm start          - Start development server"
echo "  npm run build      - Build for production"
echo "  npm test           - Run tests"
echo "  npm run eject      - Eject from Create React App"
echo ""

npm start
