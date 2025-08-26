# Sudoku Game

A complete Sudoku game implementation with multiple interfaces: CLI, Web GUI, Desktop application, and AWS Lambda deployment.

## Project Structure

```
sudoku/
├── src/                          # Source code
│   ├── core/                     # Core game logic
│   │   ├── sudoku.py            # Main Sudoku game class
│   │   └── test_sudoku.py       # Unit tests
│   ├── desktop/                  # Desktop application
│   │   ├── sudoku_app.py        # Flask-based desktop app
│   │   └── sudoku_gui.py        # Alternative GUI implementation
│   ├── web/                      # Web application
│   │   ├── app.py               # Flask web server
│   │   ├── lambda_app.py        # AWS Lambda handler
│   │   ├── web_gui.py           # Web interface utilities
│   │   └── templates/           # HTML templates
│   │       └── sudoku.html
│   └── cli/                      # Command-line interface
│       └── main.py              # CLI application
├── build/                        # Build configurations
│   ├── scripts/                 # Build scripts
│   │   └── build_windows.py     # Windows executable builder
│   └── specs/                   # PyInstaller spec files
│       └── SudokuGame-macOS.spec
├── deploy/                       # Deployment configurations
│   ├── cdk/                     # AWS CDK deployment
│   │   ├── cdk.json
│   │   └── cdk.out/
│   └── deploy.sh                # Deployment script
├── docs/                        # Documentation
│   ├── README.md               # Main documentation
│   ├── README_DEPLOYMENT.md    # Deployment guide
│   ├── README_WINDOWS.md       # Windows-specific docs
│   └── Windows_BUILD_INSTRUCTIONS.md
├── .github/workflows/           # GitHub Actions
│   ├── build-windows.yml      # Multi-platform build
│   └── release.yml             # Release automation
├── pyproject.toml              # Project configuration
└── uv.lock                     # Dependency lockfile
```

## Quick Start

### Desktop Application
```bash
python src/desktop/sudoku_app.py
```

### Web Application
```bash
python src/web/app.py
```

### Command Line
```bash
python src/cli/main.py
```

### Run Tests
```bash
python src/core/test_sudoku.py
```

## Building Executables

### Windows
```bash
python build/scripts/build_windows.py
```

### All Platforms (GitHub Actions)
Create a git tag to trigger automated builds:
```bash
git tag v1.0.1
git push origin v1.0.1
```

## Deployment

### AWS Lambda
```bash
cd deploy
./deploy.sh
```

### Local Development
```bash
uv sync
uv run python src/web/app.py
```

## Features

- **Multiple Interfaces**: CLI, Desktop GUI, Web interface
- **Three Difficulty Levels**: Easy, Medium, Hard
- **Smart Validation**: Real-time move checking
- **Hint System**: Get hints when stuck
- **Cross-Platform**: Windows, macOS, Linux support
- **Cloud Deployment**: Ready for AWS Lambda
- **Automatic Port Detection**: No port conflicts

## Development

The project uses a modular structure:
- `src/core/`: Pure game logic, no UI dependencies
- `src/desktop/`: Desktop application using Flask + browser
- `src/web/`: Web server and Lambda deployment
- `src/cli/`: Command-line interface
- `build/`: Build scripts and configurations
- `deploy/`: Deployment configurations and scripts

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes in the appropriate `src/` subfolder
4. Add tests if needed
5. Submit a pull request

## License

MIT License - see LICENSE file for details