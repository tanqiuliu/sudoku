#!/usr/bin/env python3
"""
Script to build Windows executable using PyInstaller
Run this on a Windows machine or use GitHub Actions
"""

import subprocess
import sys
import os

def build_windows_exe():
    """Build Windows executable using PyInstaller"""
    
    print("🏗️  Building Windows executable for Sudoku Game...")
    
    # PyInstaller command for Windows
    cmd = [
        "pyinstaller",
        "--onefile",                    # Single file executable
        "--console",                    # Show console window
        "--name", "SudokuGame",         # Executable name
        "--add-data", "templates;templates",  # Include templates (Windows separator)
        "--add-data", "sudoku.py;.",          # Include sudoku module
        "--distpath", "dist_windows",         # Output directory
        "--workpath", "build_windows",        # Work directory
        "--specpath", ".",                    # Spec file location
        "--clean",                            # Clean build
        "sudoku_app.py"                       # Main script
    ]
    
    try:
        # Run PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Windows executable built successfully!")
        print(f"📍 Location: dist_windows/SudokuGame.exe")
        print(f"📦 Size: {get_file_size('dist_windows/SudokuGame.exe')}")
        
        # Create distribution package
        create_distribution_package()
        
    except subprocess.CalledProcessError as e:
        print("❌ Build failed!")
        print(f"Error: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error output: {e.stderr}")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ PyInstaller not found!")
        print("Install it with: pip install pyinstaller")
        sys.exit(1)

def get_file_size(filepath):
    """Get human-readable file size"""
    try:
        size = os.path.getsize(filepath)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"
    except:
        return "Unknown"

def create_distribution_package():
    """Create a complete distribution package"""
    print("📦 Creating distribution package...")
    
    # Create distribution directory
    os.makedirs("SudokuGame_Windows_Distribution", exist_ok=True)
    
    # Copy files
    import shutil
    
    # Copy executable (if it exists, otherwise create placeholder)
    if os.path.exists("dist_windows/SudokuGame.exe"):
        shutil.copy2("dist_windows/SudokuGame.exe", "SudokuGame_Windows_Distribution/")
        print("✅ Copied SudokuGame.exe")
    else:
        # Create placeholder message for when building on non-Windows
        placeholder = """This folder contains the distribution structure for Windows.

To get the actual SudokuGame.exe, you need to:

1. Build on a Windows machine using: python build_windows.py
2. Use GitHub Actions (see .github/workflows/build-windows.yml)
3. Use Docker with Windows container

The batch file and README are ready to use once you have the .exe file.
"""
        with open("SudokuGame_Windows_Distribution/BUILD_ON_WINDOWS.txt", "w") as f:
            f.write(placeholder)
        print("⚠️  Created BUILD_ON_WINDOWS.txt (no .exe available on macOS)")
    
    # Create batch file
    batch_content = """@echo off
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
"""
    
    with open("SudokuGame_Windows_Distribution/START_SUDOKU_GAME.bat", "w") as f:
        f.write(batch_content)
    print("✅ Created START_SUDOKU_GAME.bat")
    
    # Create README
    readme_content = """# Sudoku Game - Windows Desktop Application

🎮 **A complete Sudoku game with beautiful web-based GUI**

## Quick Start
1. Double-click `START_SUDOKU_GAME.bat` (recommended)
   OR
2. Double-click `SudokuGame.exe` directly

The game will open in your web browser automatically!

## Features
- ✅ Beautiful colorful interface (light yellow & blue checkerboard)
- ✅ Three difficulty levels: Easy, Medium, Hard
- ✅ Real-time move validation with visual feedback
- ✅ Hint system when you get stuck
- ✅ Auto-completion detection with celebration
- ✅ Completely offline - no internet required
- ✅ No installation needed - just run and play!

## System Requirements
- Windows 7, 8, 10, or 11 (64-bit)
- Any modern web browser (Chrome, Firefox, Edge, etc.)
- ~12MB disk space

## How to Play
1. Click on empty cells and enter numbers 1-9
2. Each row, column, and 3x3 box must contain all digits 1-9
3. Green cells = valid moves, Red cells = invalid moves
4. Use "Get Hint" button if you need help
5. Complete the puzzle to win!

## Troubleshooting
- If browser doesn't open: Go to http://localhost:5050
- If Windows shows security warning: Click "Run anyway" (app is safe)
- To quit: Close the console window or visit http://localhost:5050/quit

Enjoy playing Sudoku! 🧩✨
"""
    
    with open("SudokuGame_Windows_Distribution/README.txt", "w") as f:
        f.write(readme_content)
    print("✅ Created README.txt")
    
    print(f"🎉 Distribution package ready: SudokuGame_Windows_Distribution/")
    print("📂 Contains:")
    print("   - SudokuGame.exe (main executable)")
    print("   - START_SUDOKU_GAME.bat (launcher with nice interface)")
    print("   - README.txt (user instructions)")

if __name__ == "__main__":
    print("Windows Sudoku Game Builder")
    print("=" * 50)
    
    # Check if running on Windows for optimal build
    if sys.platform != "win32":
        print("⚠️  This script is designed for Windows.")
        print("   For best results, run on a Windows machine.")
        print("   Alternatively, use GitHub Actions for cross-platform builds.")
        print("   Creating distribution package structure anyway...")
        print()
        
        # Skip interactive prompt and just create the distribution structure
        create_distribution_package()
        print("\n🎯 Windows distribution package created!")
        print("📂 See: SudokuGame_Windows_Distribution/")
        print("📄 See: Windows_BUILD_INSTRUCTIONS.md for build options")
        sys.exit(0)
    
    build_windows_exe()
    
    print("\n🎯 Next Steps:")
    print("1. Test SudokuGame.exe on a Windows machine")
    print("2. Share the SudokuGame_Windows_Distribution folder")
    print("3. Users can run START_SUDOKU_GAME.bat to play!")