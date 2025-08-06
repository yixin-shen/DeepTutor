#!/bin/bash

# Offline Zotero Assistant Deployment Script

echo "🚀 Starting deployment of Offline Zotero Assistant..."

# Check if we're in the right directory
if [ ! -f "simple_test.py" ]; then
    echo "❌ Error: simple_test.py not found. Please run this script from the project root."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python $python_version is installed, but Python $required_version+ is required."
    exit 1
fi

echo "✅ Python version check passed: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
if [ -f "requirements_streamlit.txt" ]; then
    pip install -r requirements_streamlit.txt
else
    echo "❌ Error: requirements_streamlit.txt not found."
    exit 1
fi

# Run tests
echo "🧪 Running tests..."
if [ -f "test_simple_test.py" ]; then
    python -m pytest test_simple_test.py -v
else
    echo "⚠️ Warning: No test file found. Skipping tests."
fi

# Check if Streamlit is installed
if ! python -c "import streamlit" &> /dev/null; then
    echo "❌ Error: Streamlit is not installed. Please check your requirements file."
    exit 1
fi

echo "✅ All checks passed!"
echo ""
echo "🎉 Deployment completed successfully!"
echo ""
echo "To run the application:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the app: streamlit run simple_test.py"
echo "3. Open your browser to: http://localhost:8501"
echo ""
echo "Happy researching! 📚" 