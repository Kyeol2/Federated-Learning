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
        print("❌ Python 3.7 이상이 필요합니다!")
        return False
    
    print("✓ Python 버전이 적합합니다.")
    return True

def create_virtual_environment():
    """가상환경 생성"""
    print_step("가상환경 생성 중...")
    
    venv_name = "FL_env"
    
    if os.path.exists(venv_name):
        print(f"⚠️  '{venv_name}' 폴더가 이미 존재합니다.")
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
        print(f"✓ 가상환경 '{venv_name}' 생성 완료!")
        return venv_name
    else:
        print(f"❌ 가상환경 생성 실패: {output}")
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
        print("✓ pip 업그레이드 완료")
    except:
        print("⚠️  pip 업그레이드 실패, 계속 진행합니다...")
    
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
        print(f"📦 {package} 설치 중...", end=" ", flush=True)
        try:
            subprocess.run([pip_cmd, "install", package], 
                          check=True, 
                          stdout=subprocess.DEVNULL, 
                          stderr=subprocess.DEVNULL,
                          encoding='utf-8', 
                          errors='ignore')
            print("✓")
        except subprocess.CalledProcessError:
            print("❌")
            print(f"  {package} 설치 실패. 수동으로 설치해주세요: pip install {package}")
            response = input("  계속 진행하시겠습니까? (y/n): ")
            if response.lower() != 'y':
                return False
    
    print("\n✓ 패키지 설치 완료!")
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
        print("✓ requirements.txt 파일 생성 완료!")
        print("  다른 사람들은 'pip install -r requirements.txt'로 같은 환경을 구축할 수 있습니다.")
        return True
    except Exception as e:
        print(f"❌ requirements.txt 생성 실패: {e}")
        return False

def create_activation_scripts(venv_name):
    """가상환경 활성화 스크립트 생성"""
    print_step("편의 스크립트 생성 중...")
    
    system = platform.system()
    
    if system == "Windows":
        # Windows용 배치 파일
        with open("activate_fl.bat", "w") as f:
            f.write(f"@echo off\n")
            f.write(f"echo Federated Learning 가상환경 활성화 중...\n")
            f.write(f"call {venv_name}\\Scripts\\activate.bat\n")
            f.write(f"echo.\n")
            f.write(f"echo ✓ 가상환경이 활성화되었습니다!\n")
            f.write(f"echo   종료하려면 'deactivate'를 입력하세요.\n")
        print("✓ 'activate_fl.bat' 파일 생성 완료!")
        print("  사용법: activate_fl.bat")
    else:
        # Linux/Mac용 쉘 스크립트
        with open("activate_fl.sh", "w") as f:
            f.write(f"#!/bin/bash\n")
            f.write(f"echo 'Federated Learning 가상환경 활성화 중...'\n")
            f.write(f"source {venv_name}/bin/activate\n")
            f.write(f"echo ''\n")
            f.write(f"echo '✓ 가상환경이 활성화되었습니다!'\n")
            f.write(f"echo '  종료하려면 deactivate를 입력하세요.'\n")
        
        # 실행 권한 부여
        os.chmod("activate_fl.sh", 0o755)
        print("✓ 'activate_fl.sh' 파일 생성 완료!")
        print("  사용법: source activate_fl.sh")
    
    return True

def create_readme():
    """README 파일 생성"""
    print_step("README.md 파일 생성 중...")
    
    system = platform.system()
    activate_cmd = "activate_fl.bat" if system == "Windows" else "source activate_fl.sh"
    
    readme_content = f"""# Federated Learning 프로젝트

## 환경 설정 (자동)

### 처음 설정하는 경우
```bash
python setup_fl_env.py
```

이 스크립트가 자동으로:
1. 가상환경 생성
2. 필요한 패키지 설치
3. requirements.txt 생성
4. 활성화 스크립트 생성

### 가상환경 활성화
```bash
{activate_cmd}
```

### 가상환경 비활성화
```bash
deactivate
```

## 수동 설정 (선택사항)

### 1. 가상환경 생성
```bash
python -m venv fl_env
```

### 2. 가상환경 활성화
- Windows: `fl_env\\Scripts\\activate`
- Linux/Mac: `source fl_env/bin/activate`

### 3. 패키지 설치
```bash
pip install -r requirements.txt
```

## 프로젝트 구조
```
federated-learning/
├── fl_env/              # 가상환경 (Git에 포함하지 않음)
├── setup_fl_env.py      # 환경 설정 스크립트
├── requirements.txt     # 패키지 목록
├── activate_fl.{('bat' if system == 'Windows' else 'sh')}      # 활성화 스크립트
├── server/              # 서버 코드
└── client/              # 클라이언트 코드
```

## .gitignore 설정
가상환경을 Git에 올리지 않으려면 `.gitignore` 파일에 추가:
```
fl_env/
__pycache__/
*.pyc
.DS_Store
```

## 다른 사람이 환경 설정하는 방법
1. 이 저장소를 클론
2. `python setup_fl_env.py` 실행
3. 가상환경 활성화

또는

1. 가상환경 생성: `python -m venv fl_env`
2. 가상환경 활성화
3. 패키지 설치: `pip install -r requirements.txt`
"""
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("✓ README.md 파일 생성 완료!")
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
        print("⚠️  .gitignore 파일이 이미 존재합니다.")
        response = input("덮어쓰시겠습니까? (y/n): ")
        if response.lower() != 'y':
            print("기존 .gitignore 파일을 유지합니다.")
            return True
    
    with open(".gitignore", "w") as f:
        f.write(gitignore_content)
    
    print("✓ .gitignore 파일 생성 완료!")
    return True

def print_final_instructions(venv_name):
    """최종 안내 메시지 출력"""
    system = platform.system()
    
    print("\n" + "="*60)
    print("  🎉 Federated Learning 환경 설정 완료!")
    print("="*60)
    
    print("\n📝 다음 단계:")
    print("\n1. 가상환경 활성화:")
    if system == "Windows":
        print(f"   activate_fl.bat")
    else:
        print(f"   source activate_fl.sh")
    
    print("\n2. 코드 작성 및 실행")
    
    print("\n3. 가상환경 비활성화:")
    print("   deactivate")
    
    print("\n📦 생성된 파일:")
    print(f"   - {venv_name}/          (가상환경 폴더)")
    print("   - requirements.txt     (패키지 목록)")
    if system == "Windows":
        print("   - activate_fl.bat      (활성화 스크립트)")
    else:
        print("   - activate_fl.sh       (활성화 스크립트)")
    print("   - README.md            (사용 설명서)")
    print("   - .gitignore           (Git 제외 목록)")
    
    print("\n⚠️  중요:")
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
        print("\n❌ 패키지 설치 중 오류가 발생했습니다.")
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
        print("\n\n❌ 사용자에 의해 중단되었습니다.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ 예상치 못한 오류 발생: {e}")
        sys.exit(1)