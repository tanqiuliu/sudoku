@echo off
title Sudoku Game - Windows Desktop App
cls
echo.
echo ==========================================
echo          🎮 SUDOKU GAME 🎮
echo ==========================================  
echo.
echo Starting Sudoku Desktop Application...
echo The game will open in your web browser.
echo.
echo Features:
echo  - Three difficulty levels
echo  - Colorful checkerboard design  
echo  - Real-time validation
echo  - Hint system
echo.
echo To quit: Close this window or visit http://localhost:5050/quit
echo.
echo ==========================================
echo.

SudokuGame.exe

echo.
echo Game closed. Press any key to exit...
pause > nul
