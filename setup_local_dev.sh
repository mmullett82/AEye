#!/bin/bash
# setup_local_dev.sh

echo "Setting up local virtual environment..."
python3 -m venv venv
source venv/bin/activate
echo "Virtual environment activated."

echo "Installing requirements..."
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

echo "Setup complete! To activate the environment later, run:"
echo "source venv/bin/activate"
