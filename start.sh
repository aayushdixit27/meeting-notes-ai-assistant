#!/bin/bash

# Meeting Notes AI Assistant - Quick Start Script
# This script helps you get up and running quickly

echo "🧠 Meeting Notes AI Assistant - Quick Start"
echo "============================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    echo "   Download from: https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo ""
    echo "You need to create a .env file with your Anthropic API key."
    echo ""
    read -p "Do you have an Anthropic API key? (y/n): " has_key

    if [ "$has_key" = "y" ] || [ "$has_key" = "Y" ]; then
        read -p "Enter your API key: " api_key
        echo "ANTHROPIC_API_KEY=$api_key" > .env
        echo "✅ .env file created!"
    else
        echo ""
        echo "📝 To get an API key:"
        echo "   1. Go to https://console.anthropic.com/"
        echo "   2. Sign up for an account"
        echo "   3. Navigate to 'API Keys'"
        echo "   4. Create a new key"
        echo "   5. Run this script again"
        echo ""
        exit 1
    fi
else
    echo "✅ .env file found"
fi

echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment found"
fi

echo ""

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -q -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "🚀 Starting the application..."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📝 Open http://localhost:5000 in your browser"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 PM Tip: Open DevTools (F12) > Network tab"
echo "   to see the API calls in action!"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the app
python3 app.py
