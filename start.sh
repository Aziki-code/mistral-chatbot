#!/bin/bash
# Portable startup script for Mistral Chatbot

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if venv exists, create if not
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install dependencies if needed
if ! python -c "import flask" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install flask python-dotenv mistralai
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo "ERROR: .env file not found!"
    echo "Please create .env with: MISTRAL_API_KEY=your_key_here"
    exit 1
fi

# Start the chatbot
echo "Starting Mistral Chatbot..."
echo "Access at: https://localhost:5000"
python chatbot_sql.py
