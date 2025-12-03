#!/bin/bash

# Quick Start Script for FastAPI Calculator
# This script helps you get started quickly

echo "🚀 FastAPI Calculator - Quick Start"
echo "===================================="
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Creating one..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "✅ Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -q -r requirements.txt

# Check if PostgreSQL is running
echo "🔍 Checking PostgreSQL..."
if ! pg_isready > /dev/null 2>&1; then
    echo "⚠️  PostgreSQL is not running. Please start PostgreSQL first."
    echo "   You can start it with: brew services start postgresql"
    echo ""
    echo "   Or use Docker Compose instead:"
    echo "   docker-compose up"
    exit 1
fi

# Check if databases exist
echo "🗄️  Checking databases..."
if ! psql -lqt | cut -d \| -f 1 | grep -qw calculator_db; then
    echo "Creating calculator_db..."
    createdb calculator_db
fi

if ! psql -lqt | cut -d \| -f 1 | grep -qw test_calculator_db; then
    echo "Creating test_calculator_db..."
    createdb test_calculator_db
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Choose an option:"
echo "1) Run tests"
echo "2) Start the application"
echo "3) Both (run tests, then start app)"
echo ""
read -p "Enter choice [1-3]: " choice

case $choice in
    1)
        echo ""
        echo "🧪 Running tests..."
        pytest -v
        ;;
    2)
        echo ""
        echo "🌐 Starting FastAPI server..."
        echo "   API: http://localhost:8000"
        echo "   Docs: http://localhost:8000/docs"
        echo ""
        uvicorn app.main:app --reload
        ;;
    3)
        echo ""
        echo "🧪 Running tests..."
        pytest -v
        if [ $? -eq 0 ]; then
            echo ""
            echo "✅ All tests passed!"
            echo ""
            echo "🌐 Starting FastAPI server..."
            echo "   API: http://localhost:8000"
            echo "   Docs: http://localhost:8000/docs"
            echo ""
            uvicorn app.main:app --reload
        else
            echo ""
            echo "❌ Tests failed. Please fix errors before starting the server."
        fi
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac
