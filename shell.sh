#!/bin/bash

# Print a message to indicate the start of the setup process
echo "=========================="
echo "  Setting up the project   "
echo "=========================="

# Ensure the script is run from the project root directory
if [ ! -f "requirements.dev" ]; then
  echo "Error: This script must be run from the project root directory."
  exit 1
fi

# Create a virtual environment (if not already created)
echo "Creating virtual environment..."
python3 -m venv venv
echo "Virtual environment created: venv/"

# Activate the virtual environment
echo "Activating the virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies from requirements.dev..."
pip install -r requirements.dev

# Inform the user about environment setup
echo "Virtual environment setup complete!"

# Run tests to verify the setup
echo "Running tests to verify setup..."
pytest --maxfail=1 --disable-warnings -q

# Provide instructions to the user
echo "=========================="
echo "  Setup Complete          "
echo "=========================="
echo "To activate the virtual environment again, use:"
echo "  source venv/bin/activate"
echo "To deactivate the virtual environment, use:"
echo "  deactivate"
