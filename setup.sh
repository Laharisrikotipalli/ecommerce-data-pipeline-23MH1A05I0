#!/bin/bash

# 1. Detect the correct Python command (try 'python', 'python3', or 'py')
if command -v python &>/dev/null; then
    PYTHON_CMD="python"
elif command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v py &>/dev/null; then
    PYTHON_CMD="py"
else
    echo "Error: Python is not installed or not in your PATH."
    exit 1
fi

echo "Using command: $PYTHON_CMD"

# 2. Create the Virtual Environment if it doesn't exist
if [ ! -d "venv" ]; then
    $PYTHON_CMD -m venv venv
    echo "Virtual environment 'venv' created."
fi

# 3. Activate the environment (Git Bash uses the POSIX path)
# Windows venv contains 'Scripts', but Git Bash needs 'source'
source venv/Scripts/activate

# 4. Install dependencies inside the virtual environment
# This bypasses the 'externally-managed-environment' error
echo "Installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt

# 5. Create mandatory project directories
mkdir -p data/raw data/staging data/processed logs

echo "Setup complete! Virtual environment is active."