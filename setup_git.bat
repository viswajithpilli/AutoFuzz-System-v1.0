@echo off
echo [*] Cleaning old git files...
rmdir /s /q .git
echo [*] Initializing Git...
git init
git config user.email "fuzzer@bot.local"
git config user.name "Fuzzer Bot"
echo [*] Adding files...
git add .
echo [*] Committing...
git commit -m "Initial commit of AutoFuzz System"
git branch -M main
echo.
echo [SUCCESS] Repository Ready!
echo.
echo To push to GitHub, run these commands:
echo 1. git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
echo 2. git push -u origin main
echo.
pause
