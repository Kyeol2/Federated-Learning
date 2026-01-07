# Federated Learning Environment Setup Guide

## Automatic Setup

### First Time Setup
```bash
python setup_fl_env.py
```

This script automatically:
1. Creates virtual environment (FL_env)
2. Installs required packages
3. Generates requirements.txt
4. Creates activation scripts

### Activate Virtual Environment

**PowerShell (Recommended):**
```powershell
.\activate_fl.ps1
```

**CMD:**
```cmd
activate_fl.bat
```

**Linux/Mac:**
```bash
source activate_fl.sh
```

### PowerShell Execution Policy Error
If script execution is blocked in PowerShell:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Or activate directly:
```powershell
.\FL_env\Scripts\Activate.ps1
```

### Deactivate Virtual Environment
```bash
deactivate
```

## Manual Setup (Optional)

### 1. Create Virtual Environment
```bash
python -m venv FL_env
```

### 2. Activate Virtual Environment
- PowerShell: `.\FL_env\Scripts\Activate.ps1`
- CMD: `FL_env\Scripts\activate.bat`
- Linux/Mac: `source FL_env/bin/activate`

### 3. Install Packages
```bash
pip install -r requirements.txt
```

## Project Structure
```
federated-learning/
├── FL_env/              # Virtual environment (DO NOT commit to Git)
├── setup_fl_env.py      # Environment setup script
├── test_fl_env.py       # Environment test script
├── requirements.txt     # Package list
├── activate_fl.ps1      # PowerShell activation script
├── activate_fl.bat      # CMD activation script
├── FL_SETUP.md          # This file
├── server/              # Server code
└── client/              # Client code
```

## .gitignore Configuration
To exclude virtual environment from Git, add to `.gitignore`:
```
FL_env/
__pycache__/
*.pyc
.DS_Store
```

## For Other Users

### Method 1: Automatic
1. Clone this repository
2. Run `python setup_fl_env.py`
3. Activate virtual environment

### Method 2: Manual
1. Create virtual environment: `python -m venv FL_env`
2. Activate virtual environment
3. Install packages: `pip install -r requirements.txt`

## Testing Environment

After activation, test your environment:
```bash
python test_fl_env.py
```

This will verify:
- Python version
- Package installations
- PyTorch functionality
- NumPy functionality
- Federated Learning simulation

## Troubleshooting

### PowerShell Script Execution Error
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Check if Virtual Environment is Active
Look for `(FL_env)` prefix in your prompt:
```
(FL_env) PS C:\your\project>
```

### Verify Package Installation
```bash
pip list
python -c "import torch; print(torch.__version__)"
```

## Important Notes

- **DO NOT** commit the FL_env/ folder to GitHub
- Only share requirements.txt
- Other users can rebuild the same environment using `python setup_fl_env.py`
- Virtual environment only affects the current project
- Your system Python remains unchanged
