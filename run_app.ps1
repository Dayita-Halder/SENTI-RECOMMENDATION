# ============================================================
# Sentiment-Based Product Recommender - Quick Start
# PowerShell Script for Windows
# ============================================================
# Run with: powershell -ExecutionPolicy Bypass -File run_app.ps1

Write-Host ""
Write-Host "=" * 80
Write-Host "  SENTIMENT-BASED PRODUCT RECOMMENDER - QUICK START" -ForegroundColor Cyan
Write-Host "=" * 80
Write-Host ""

# Check if pickle files exist
$pickleFiles = @(
    "tfidf_vectorizer.pkl",
    "sentiment_model.pkl",
    "user_based_cf.pkl",
    "master_reviews.pkl"
)

$missingFiles = @()
foreach ($file in $pickleFiles) {
    if (-not (Test-Path $file)) {
        $missingFiles += $file
    }
}

if ($missingFiles.Count -gt 0) {
    Write-Host ""
    Write-Host "ERROR: Pickle files not found!" -ForegroundColor Red
    Write-Host "=" * 80
    Write-Host ""
    Write-Host "STEP 1 REQUIRED: Generate pickle files from the notebook" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  1. Open sentiment_recommendation_notebook.ipynb in VS Code"
    Write-Host "  2. Click 'Run All' to execute all cells"
    Write-Host "  3. Wait for completion (5-10 minutes)"
    Write-Host "  4. Pickle files will be auto-saved to this directory"
    Write-Host ""
    Write-Host "Missing files:" -ForegroundColor Yellow
    foreach ($file in $missingFiles) {
        Write-Host "  - $file"
    }
    Write-Host ""
    Write-Host "=" * 80
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Check Python
Write-Host "STEP 1: Checking Python installation..." -ForegroundColor Cyan
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✓ Python found: $pythonVersion"
} catch {
    Write-Host "  ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "  Please install Python 3.8+ from https://www.python.org/" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

# Install dependencies
Write-Host "STEP 2: Installing dependencies..." -ForegroundColor Cyan
pip install -q flask nltk scikit-learn numpy pandas 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Dependencies installed"
} else {
    Write-Host "  ⚠ Warning: Some dependencies may not have installed. Continuing anyway..."
}
Write-Host ""

# Start Flask server
Write-Host "STEP 3: Starting Flask server..." -ForegroundColor Cyan
Write-Host ""
Write-Host "=" * 80
Write-Host "  SERVER STARTING..." -ForegroundColor Green
Write-Host "=" * 80
Write-Host ""
Write-Host "  🌐 Open your browser: http://localhost:5000" -ForegroundColor Green
Write-Host ""
Write-Host "  📊 API Endpoints:" -ForegroundColor Cyan
Write-Host "     - POST /api/predict        Sentiment prediction"
Write-Host "     - POST /api/recommend      Product recommendations"
Write-Host "     - POST /api/combined       Sentiment + recommendations"
Write-Host "     - GET  /api/health         Health check"
Write-Host ""
Write-Host "  Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""
Write-Host "=" * 80
Write-Host ""

python app.py
