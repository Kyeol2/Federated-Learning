# Federated Learning 프로젝트

## 환경 설정 (자동)

### 처음 설정하는 경우
```bash
python setup_fl_env.py
```

이 스크립트가 자동으로:
1. 가상환경 생성 (FL_env)
2. 필요한 패키지 설치
3. requirements.txt 생성
4. 활성화 스크립트 생성

### 가상환경 활성화

**PowerShell (권장):**
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

### PowerShell 실행 정책 오류가 발생하는 경우
PowerShell에서 스크립트 실행이 차단되면:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

또는 직접 활성화:
```powershell
.\FL_env\Scripts\Activate.ps1
```

### 가상환경 비활성화
```bash
deactivate
```

## 수동 설정 (선택사항)

### 1. 가상환경 생성
```bash
python -m venv FL_env
```

### 2. 가상환경 활성화
- PowerShell: `.\FL_env\Scripts\Activate.ps1`
- CMD: `FL_env\Scripts\activate.bat`
- Linux/Mac: `source FL_env/bin/activate`

### 3. 패키지 설치
```bash
pip install -r requirements.txt
```

## 프로젝트 구조
```
federated-learning/
├── FL_env/              # 가상환경 (Git에 포함하지 않음)
├── setup_fl_env.py      # 환경 설정 스크립트
├── requirements.txt     # 패키지 목록
├── activate_fl.ps1      # PowerShell 활성화 스크립트
├── activate_fl.bat      # CMD 활성화 스크립트
├── server/              # 서버 코드
└── client/              # 클라이언트 코드
```

## .gitignore 설정
가상환경을 Git에 올리지 않으려면 `.gitignore` 파일에 추가:
```
FL_env/
__pycache__/
*.pyc
.DS_Store
```

## 다른 사람이 환경 설정하는 방법
1. 이 저장소를 클론
2. `python setup_fl_env.py` 실행
3. 가상환경 활성화

또는

1. 가상환경 생성: `python -m venv FL_env`
2. 가상환경 활성화
3. 패키지 설치: `pip install -r requirements.txt`

## 문제 해결

### PowerShell에서 스크립트 실행 오류
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 가상환경이 활성화되었는지 확인
프롬프트 앞에 `(FL_env)`가 표시되면 활성화된 것입니다:
```
(FL_env) PS C:\your\project>
```
