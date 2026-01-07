#!/usr/bin/env python3
"""
Federated Learning 환경 자동 설정 스크립트
이 스크립트를 실행하면 자동으로 가상환경을 만들고 필요한 패키지를 설치합니다.

사용법:
    python setup_fl_env.py
"""

import os
import sys
import subprocess
import platform

def print_step(message):
    """단계별 메시지 출력"""
    print(f"\n{'='*60}")
    print(f"  {message}")
    print(f"{'='*60}\n")

def run_command(command, shell=False):
    """명령어 실행"""
    try:
        if shell:
            result = subprocess.run(command, shell=True, check=True, 
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   encoding='utf-8', errors='ignore')
        else:
            result = subprocess.run(command, check=True, 
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   encoding='utf-8', errors='ignore')
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr if e.stderr else str(e)

def check_python_version():
    """Python 버전 확인"""
    print_step("Python 버전 확인 중...")
    version = sys.version_info
    print(f"현재 Python 버전: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("[ERROR] Python 3.7 이상이 필요합니다!")
        return False
    
    print("[OK] Python 버전이 적합합니다.")
    return True

def create_virtual_environment():
    """가상환경 생성"""
    print_step("가상환경 생성 중...")
    
    venv_name = "FL_env"
    
    if os.path.exists(venv_name):
        print(f"[WARNING] '{venv_name}' 폴더가 이미 존재합니다.")
        response = input("기존 가상환경을 삭제하고 새로 만들까요? (y/n): ")
        if response.lower() == 'y':
            print("기존 가상환경 삭제 중...")
            if platform.system() == "Windows":
                run_command(f"rmdir /s /q {venv_name}", shell=True)
            else:
                run_command(f"rm -rf {venv_name}", shell=True)
        else:
            print("기존 가상환경을 사용합니다.")
            return venv_name
    
    print(f"'{venv_name}' 가상환경 생성 중...")
    success, output = run_command([sys.executable, "-m", "venv", venv_name])
    
    if success:
        print(f"[OK] 가상환경 '{venv_name}' 생성 완료!")
        return venv_name
    else:
        print(f"[ERROR] 가상환경 생성 실패: {output}")
        return None

def get_pip_command(venv_name):
    """OS별 pip 명령어 경로 반환"""
    system = platform.system()
    if system == "Windows":
        return os.path.join(venv_name, "Scripts", "pip.exe")
    else:
        return os.path.join(venv_name, "bin", "pip")

def get_python_command(venv_name):
    """OS별 python 명령어 경로 반환"""
    system = platform.system()
    if system == "Windows":
        return os.path.join(venv_name, "Scripts", "python.exe")
    else:
        return os.path.join(venv_name, "bin", "python")

def install_packages(venv_name):
    """필요한 패키지 설치"""
    print_step("필요한 패키지 설치 중...")
    
    pip_cmd = get_pip_command(venv_name)
    
    # pip 업그레이드
    print("pip 업그레이드 중...")
    try:
        subprocess.run([pip_cmd, "install", "--upgrade", "pip"], 
                      check=True, 
                      stdout=subprocess.DEVNULL, 
                      stderr=subprocess.DEVNULL,
                      encoding='utf-8', 
                      errors='ignore')
        print("[OK] pip 업그레이드 완료")
    except:
        print("[WARNING] pip 업그레이드 실패, 계속 진행합니다...")
    
    # 필요한 패키지 목록
    packages = [
        "torch",
        "numpy",
        "pandas",
        "scikit-learn",
        "matplotlib",
        "flask",  # 서버 통신용
        "requests",  # 클라이언트 통신용
    ]
    
    print("\n설치할 패키지:")
    for pkg in packages:
        print(f"  - {pkg}")
    
    print("\n패키지 설치 시작... (시간이 걸릴 수 있습니다)\n")
    
    for package in packages:
        print(f"[INSTALL] {package} 설치 중...", end=" ", flush=True)
        try:
            subprocess.run([pip_cmd, "install", package], 
                          check=True, 
                          stdout=subprocess.DEVNULL, 
                          stderr=subprocess.DEVNULL,
                          encoding='utf-8', 
                          errors='ignore')
            print("[OK]")
        except subprocess.CalledProcessError:
            print("[ERROR]")
            print(f"  {package} 설치 실패. 수동으로 설치해주세요: pip install {package}")
            response = input("  계속 진행하시겠습니까? (y/n): ")
            if response.lower() != 'y':
                return False
    
    print("\n[OK] 패키지 설치 완료!")
    return True

def create_requirements_file(venv_name):
    """requirements.txt 파일 생성"""
    print_step("requirements.txt 파일 생성 중...")
    
    pip_cmd = get_pip_command(venv_name)
    
    try:
        result = subprocess.run([pip_cmd, "freeze"], 
                               check=True,
                               stdout=subprocess.PIPE,
                               encoding='utf-8',
                               errors='ignore')
        output = result.stdout
        
        with open("requirements.txt", "w", encoding='utf-8') as f:
            f.write(output)
        print("[OK] requirements.txt 파일 생성 완료!")
        print("  다른 사람들은 'pip install -r requirements.txt'로 같은 환경을 구축할 수 있습니다.")
        return True
    except Exception as e:
        print(f"[ERROR] requirements.txt 생성 실패: {e}")
        return False

def create_activation_scripts(venv_name):
    """가상환경 활성화 스크립트 생성"""
    print_step("Creating convenience scripts...")
    
    system = platform.system()
    
    if system == "Windows":
        # PowerShell script
        with open("activate_fl.ps1", "w", encoding='utf-8') as f:
            f.write(f"# Federated Learning Virtual Environment Activation Script\n")
            f.write(f"Write-Host 'Activating Federated Learning virtual environment...' -ForegroundColor Cyan\n")
            f.write(f"& .\\{venv_name}\\Scripts\\Activate.ps1\n")
            f.write(f"Write-Host ''\n")
            f.write(f"Write-Host '[OK] Virtual environment activated successfully!' -ForegroundColor Green\n")
            f.write(f"Write-Host '  Type deactivate to exit.' -ForegroundColor Yellow\n")
        
        # CMD batch file
        with open("activate_fl.bat", "w", encoding='utf-8') as f:
            f.write(f"@echo off\n")
            f.write(f"echo Activating Federated Learning virtual environment...\n")
            f.write(f"call {venv_name}\\Scripts\\activate.bat\n")
            f.write(f"echo.\n")
            f.write(f"echo [OK] Virtual environment activated successfully!\n")
            f.write(f"echo   Type 'deactivate' to exit.\n")
        
        print("[OK] 'activate_fl.ps1' created! (PowerShell)")
        print("[OK] 'activate_fl.bat' created! (CMD)")
        print("\n  Usage:")
        print("    PowerShell: .\\activate_fl.ps1")
        print("    CMD:        activate_fl.bat")
    else:
        # Linux/Mac shell script
        with open("activate_fl.sh", "w", encoding='utf-8') as f:
            f.write(f"#!/bin/bash\n")
            f.write(f"echo 'Activating Federated Learning virtual environment...'\n")
            f.write(f"source {venv_name}/bin/activate\n")
            f.write(f"echo ''\n")
            f.write(f"echo '[OK] Virtual environment activated successfully!'\n")
            f.write(f"echo '  Type deactivate to exit.'\n")
        
        # Set execute permission
        os.chmod("activate_fl.sh", 0o755)
        print("[OK] 'activate_fl.sh' created!")
        print("  Usage: source activate_fl.sh")
    
    return True

def create_readme():
    """README 파일 생성"""
    print_step("Creating FL_SETUP.md file...")
    
    system = platform.system()
    
    readme_content = f"""# Federated Learning Environment Setup Guide

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
.\\activate_fl.ps1
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
.\\FL_env\\Scripts\\Activate.ps1
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
- PowerShell: `.\\FL_env\\Scripts\\Activate.ps1`
- CMD: `FL_env\\Scripts\\activate.bat`
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
(FL_env) PS C:\\your\\project>
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
"""
    
    with open("FL_SETUP.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("[OK] FL_SETUP.md file created!")
    print("  This file contains FL environment setup instructions")
    print("  Your original README.md is preserved")
    return True

def create_gitignore():
    """`.gitignore` 파일 생성"""
    print_step(".gitignore 파일 생성 중...")
    
    gitignore_content = """# 가상환경
FL_env/
fl_env/
venv/
env/

# Python 캐시
__pycache__/
*.py[cod]
*$py.class
*.so

# 배포 파일
build/
dist/
*.egg-info/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# 데이터 파일
*.csv
*.json
data/
logs/

# 모델 파일
*.pth
*.pt
models/
checkpoints/
"""
    
    if os.path.exists(".gitignore"):
        print("[WARNING] .gitignore 파일이 이미 존재합니다.")
        response = input("덮어쓰시겠습니까? (y/n): ")
        if response.lower() != 'y':
            print("기존 .gitignore 파일을 유지합니다.")
            return True
    
    with open(".gitignore", "w") as f:
        f.write(gitignore_content)
    
    print("[OK] .gitignore 파일 생성 완료!")
    return True

def print_final_instructions(venv_name):
    """최종 안내 메시지 출력"""
    system = platform.system()
    
    print("\n" + "="*60)
    print("  [SUCCESS] Federated Learning 환경 설정 완료!")
    print("="*60)
    
    print("\n[NEXT STEPS] 다음 단계:")
    print("\n1. 가상환경 활성화:")
    if system == "Windows":
        print(f"   PowerShell: .\\activate_fl.ps1")
        print(f"   CMD:        activate_fl.bat")
    else:
        print(f"   source activate_fl.sh")
    
    print("\n2. 코드 작성 및 실행")
    
    print("\n3. 가상환경 비활성화:")
    print("   deactivate")
    
    print("\n[FILES] 생성된 파일:")
    print(f"   - {venv_name}/          (가상환경 폴더)")
    print("   - requirements.txt     (패키지 목록)")
    if system == "Windows":
        print("   - activate_fl.ps1      (PowerShell 활성화 스크립트)")
        print("   - activate_fl.bat      (CMD 활성화 스크립트)")
    else:
        print("   - activate_fl.sh       (활성화 스크립트)")
    print("   - FL_SETUP.md          (FL 환경 설정 가이드)")
    print("   - .gitignore           (Git 제외 목록)")
    
    print("\n[POWERSHELL] PowerShell 사용자:")
    print("   스크립트 실행이 차단되면:")
    print("   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser")
    
    print("\n[IMPORTANT] 중요:")
    print("   - 가상환경 폴더는 GitHub에 올리지 마세요!")
    print("   - requirements.txt만 공유하면 됩니다.")
    print("   - 다른 사람들은 'python setup_fl_env.py'로 같은 환경을 구축할 수 있습니다.")
    
    print("\n" + "="*60 + "\n")

def main():
    """메인 함수"""
    print("\n" + "="*60)
    print("  Federated Learning 환경 자동 설정 스크립트")
    print("="*60)
    
    # 1. Python 버전 확인
    if not check_python_version():
        sys.exit(1)
    
    # 2. 가상환경 생성
    venv_name = create_virtual_environment()
    if not venv_name:
        sys.exit(1)
    
    # 3. 패키지 설치
    if not install_packages(venv_name):
        print("\n[ERROR] 패키지 설치 중 오류가 발생했습니다.")
        sys.exit(1)
    
    # 4. requirements.txt 생성
    create_requirements_file(venv_name)
    
    # 5. 활성화 스크립트 생성
    create_activation_scripts(venv_name)
    
    # 6. README 생성
    create_readme()
    
    # 7. .gitignore 생성
    create_gitignore()
    
    # 8. 최종 안내 메시지
    print_final_instructions(venv_name)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[CANCELLED] 사용자에 의해 중단되었습니다.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n[ERROR] 예상치 못한 오류 발생: {e}")
        sys.exit(1)