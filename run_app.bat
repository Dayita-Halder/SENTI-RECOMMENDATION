@echo off
REM ============================================================
REM Sentiment-Based Product Recommender - Quick Start
REM Windows Batch Script
REM ============================================================

echo.
echo ================================================================================
echo   SENTIMENT-BASED PRODUCT RECOMMENDER - QUICK START
echo ================================================================================
echo.

REM Check if pickle files exist
if not exist "tfidf_vectorizer.pkl" (
    echo.
    echo ERROR: Pickle files not found!
    echo ================================================================================
    echo.
    echo STEP 1 REQUIRED: Generate pickle files from the notebook
    echo.
    echo   1. Open sentiment_recommendation_notebook.ipynb in VS Code
    echo   2. Click "Run All" to execute all cells
    echo   3. Wait for completion (5-10 minutes)
    echo   4. Pickle files will be auto-saved to this directory
    echo.
    echo Files expected:
    echo   - tfidf_vectorizer.pkl
    echo   - sentiment_model.pkl
    echo   - user_based_cf.pkl
    echo   - master_reviews.pkl
    echo.
    echo ================================================================================
    pause
    exit /b 1
)

echo STEP 1: Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)
echo   ✓ Python found
echo.

echo STEP 2: Installing dependencies...
pip install -q flask nltk scikit-learn numpy pandas >nul 2>&1
if errorlevel 1 (
    echo WARNING: pip install returned errors. Continuing anyway...
) else (
    echo   ✓ Dependencies installed
)
echo.

echo STEP 3: Starting Flask server...
echo.
echo ================================================================================
echo   SERVER STARTING...
echo ================================================================================
echo.
echo   🌐 Open your browser: http://localhost:5000
echo.
echo   📊 API Endpoints:
echo      - POST /api/predict        Sentiment prediction
echo      - POST /api/recommend      Product recommendations
echo      - POST /api/combined       Sentiment + recommendations
echo      - GET  /api/health         Health check
echo.
echo   Press Ctrl+C to stop the server
echo.
echo ================================================================================
echo.

python app.py