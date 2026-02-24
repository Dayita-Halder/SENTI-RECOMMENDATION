# Push to GitHub Script
Write-Host "================================================" -ForegroundColor Cyan
Write-Host " Pushing to GitHub Repository" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check if remote exists
Write-Host "Checking remote configuration..." -ForegroundColor Yellow
git remote -v

Write-Host ""
Write-Host "Current commit:" -ForegroundColor Yellow
git log --oneline -1

Write-Host ""
Write-Host "Pushing to GitHub..." -ForegroundColor Green
git push -u origin main

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host " Done! Check your repository at:" -ForegroundColor Green
Write-Host " https://github.com/Dayita-Halder/SENTI-RECOMMENDATION" -ForegroundColor White
Write-Host "================================================" -ForegroundColor Cyan
