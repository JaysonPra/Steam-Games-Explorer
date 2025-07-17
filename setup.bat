@echo off
echo Setting up your Streamlit Steam Explorer App...

REM Step 1: Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Step 2: Activate the virtual environment
call venv\Scripts\activate

REM Step 3: Install requirements
echo Installing required packages...
pip install --upgrade pip
pip install -r requirements.txt

REM Step 4: Check for dataset
IF EXIST data\games.csv (
    echo Dataset found in data\games.csv
) ELSE (
    echo WARNING: games.csv not found in /data
    echo Please download it from Kaggle and place it in the data\ folder.
    echo Create the data folder in the root directory if it does not exist.
)

REM Step 5: Done
echo Setup complete!
echo You can now run the app with:
echo     streamlit run streamlit-app\app.py

pause
