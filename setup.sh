#!/bin/bash

echo "Setting up your Streamlit Steam Explorer App (Linux/Mac/WSL)..."

# Step 1: Create a virtual environment
echo "Creating virtual environment in ./venv..."
python3 -m venv venv

# Step 2: Activate the virtual environment
source venv/bin/activate

# Step 3: Install requirements
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Step 4: Check if dataset exists
if [ -f "data/games.csv" ]; then
    echo "Dataset found: data/games.csv"
else
    echo "WARNING: Dataset not found in data/games.csv"
    echo "Please download it from Kaggle and place it in the 'data/' folder."
fi

# Step 5: Done
echo "Setup complete!"
echo "Run the app with:"
echo "    streamlit run streamlit-app/app.py"
