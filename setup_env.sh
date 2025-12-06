#!/bin/bash

# --- Configuration ---
ENV_NAME="gemini_tree_env"
PYTHON_VERSION="3.11"

# 1. Check for Conda
if ! command -v conda &> /dev/null; then
    echo "Error: Conda is not installed or not in your PATH."
    exit 1
fi

echo "=========================================="
echo "Creating Conda Environment: $ENV_NAME"
echo "=========================================="

# 2. Create the environment
conda create -n $ENV_NAME python=$PYTHON_VERSION -y

# 3. Install Pip dependencies
# We use 'conda run' to ensure we install into the new env
echo "Installing dependencies..."
conda run -n $ENV_NAME pip install streamlit google-genai python-dotenv watchdog

# 4. Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file template..."
    echo 'GEMINI_API_KEY="YOUR_API_KEY_HERE"' > .env
    echo "⚠️  Created .env file. Please open it and paste your API Key!"
else
    echo ".env file already exists. Skipping."
fi

echo "=========================================="
echo "      SETUP COMPLETE! "
echo "=========================================="
echo "HOW TO RUN:"
echo "1. Ensure 'app.py' is in this folder."
echo "2. Paste your API Key into the '.env' file."
echo "3. Run this command:"
echo "   conda run -n $ENV_NAME streamlit run app.py"
echo "=========================================="
