# Federated Learning Client Setup Guide (Windows)

## 📌 목차
1. [초기 환경 세팅](#초기-환경-세팅)
2. [클라이언트 실행 방법](#클라이언트-실행-방법)
3. [문제 해결 (Troubleshooting)](#문제-해결-troubleshooting)
4. [FAQ](#faq)

---

## 🚀 초기 환경 세팅

### 사전 준비물
- Windows 10/11
- Python 3.7 이상
- Git for Windows
- 인터넷 연결

---

### Step 1: Git 설치 확인

PowerShell을 열고 Git이 설치되어 있는지 확인하세요:

```powershell
git --version
```

**Git이 없다면:**
1. [Git for Windows](https://git-scm.com/download/win) 다운로드
2. 설치 시 옵션: `Git from the command line and also from 3rd-party software` 선택
3. 설치 후 PowerShell 재시작

---

### Step 2: Git 사용자 정보 설정

Git을 처음 사용한다면 사용자 정보를 설정해야 합니다:

```powershell
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

**확인:**
```powershell
git config --global --list
```

💡 **팁:** 이 정보는 커밋 이력에 표시됩니다. 실제 이름과 이메일을 사용하세요.

---

### Step 3: 저장소 클론

프로젝트를 다운로드할 위치로 이동한 후 저장소를 클론하세요:

```powershell
# 원하는 폴더로 이동 (예: 문서 폴더)
cd "C:\Users\YourName\Documents"

# 저장소 클론
git clone [REPOSITORY_URL]
cd Federated-Learning
```

**폴더 구조 확인:**
```powershell
dir
```

다음 폴더들이 보여야 합니다:
```
📁 Average/
📁 Clients/
📁 Server/
📁 FL_env/       (나중에 생성됨)
📄 setup_fl_env.py
📄 README.md
```

---

### Step 4: 가상환경 자동 생성

프로젝트 루트 폴더에서 자동 설정 스크립트를 실행하세요:

```powershell
# 현재 위치가 Federated-Learning 폴더인지 확인
pwd

# 자동 환경 설정 실행
python setup_fl_env.py
```

**이 스크립트가 자동으로 수행하는 작업:**
- ✅ 가상환경 생성 (`FL_env` 폴더)
- ✅ 필요한 패키지 설치 (PyTorch, NumPy, Pandas 등)
- ✅ requirements.txt 생성
- ✅ 활성화 스크립트 생성
- ✅ .gitignore 설정 (가상환경 제외)

⏱️ **소요 시간:** 5-10분 (인터넷 속도에 따라 다름)

**성공 메시지:**
```
============================================================
  [SUCCESS] Federated Learning Environment Setup Complete!
============================================================
```

---

### Step 5: 가상환경 활성화

#### PowerShell 사용 시 (권장):

```powershell
.\activate_fl.ps1
```

**만약 실행 정책 오류가 발생한다면:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\activate_fl.ps1
```

#### CMD 사용 시:
```cmd
activate_fl.bat
```

**✅ 활성화 확인:**
프롬프트 앞에 `(FL_env)`가 표시됩니다:
```powershell
(FL_env) PS C:\Users\YourName\Documents\Federated-Learning>
```

---

### Step 6: 환경 테스트

모든 패키지가 제대로 설치되었는지 확인:

```powershell
python test_fl_env.py
```

**예상 출력:**
```
============================================================
  Python Version Check
============================================================
[OK] Python version: 3.12.7
...
============================================================
  [SUCCESS] All tests passed!
  Your FL environment is ready to use!
============================================================
```

---

### Step 7: 데이터 준비

훈련 데이터를 CSV 형식으로 준비하세요:

**CSV 포맷:**
```csv
feature1,feature2,feature3,...,target
1.2,3.4,5.6,...,10.5
2.3,4.5,6.7,...,12.3
```

**중요 사항:**
- ✅ 마지막 열이 타겟(예측할 값)
- ✅ 나머지 열은 입력 특성
- ✅ 헤더 행 포함
- ✅ 콤마(,)로 구분

**데이터 위치:**
```
Federated-Learning/
├── FL_env/
├── Clients/
├── my_client_data.csv  ← 여기에 배치
└── ...
```

---

## 🏃 클라이언트 실행 방법

### 방법 1: 명령줄에서 실행 (기본)

```powershell
# 1. 가상환경 활성화
.\activate_fl.ps1

# 2. 프로젝트 루트를 Python 경로에 추가
$env:PYTHONPATH = (Get-Location).Path

# 3. 클라이언트 스크립트 실행
python .\Clients\client_update.py `
  --round 1 `
  --client_id 1 `
  --csv "C:\path\to\your\data.csv" `
  --feature_cols year,month `
  --target_col chloride `
  --seq_len 10
```

**파라미터 설명:**
- `--round`: 현재 훈련 라운드 번호
- `--client_id`: 클라이언트 ID (1, 2, 3 등)
- `--csv`: 데이터 파일 전체 경로
- `--feature_cols`: 입력 특성 열 이름 (콤마로 구분)
- `--target_col`: 타겟 열 이름
- `--seq_len`: 시퀀스 길이 (LSTM용)

---

### 방법 2: 웹 인터페이스 사용 (간편)

서버가 웹 인터페이스를 제공하는 경우:

1. **브라우저 열기**
   - Chrome, Firefox, Edge 등

2. **서버 주소 접속**
   ```
   http://[SERVER_IP]:5000
   ```
   예: `http://192.168.0.10:5000`

3. **데이터 업로드**
   - 자신의 클라이언트 카드 찾기 (Client 1, 2, 3 등)
   - "Upload CSV" 버튼 클릭
   - 데이터 파일 선택

4. **훈련 시작 대기**
   - 서버가 훈련을 시작하면 자동으로 진행
   - 실시간 로그 확인 가능

---

### 훈련 프로세스

```
1️⃣ 서버가 글로벌 모델 초기화
         ↓
2️⃣ 클라이언트가 모델 파라미터 수신
         ↓
3️⃣ 로컬 데이터로 모델 훈련
         ↓
4️⃣ 업데이트된 파라미터를 서버에 전송
         ↓
5️⃣ 서버가 모든 클라이언트 모델 집계
         ↓
6️⃣ 새로운 글로벌 모델 생성
         ↓
7️⃣ 다음 라운드 반복 (2번으로)
```

---

## 🔧 문제 해결 (Troubleshooting)

### 문제 1: `git` 명령어가 인식되지 않음

**증상:**
```powershell
git : 'git' 용어가 cmdlet, 함수, 스크립트 파일 또는 실행할 수 있는 프로그램 이름으로 인식되지 않습니다.
```

**원인:**
- Git이 설치되지 않았거나
- PATH 환경변수에 등록되지 않음

**해결 방법:**

1. **Git 설치 확인:**
   ```powershell
   where.exe git
   ```

2. **Git 설치:**
   - [Git for Windows](https://git-scm.com/download/win) 다운로드
   - 설치 후 PowerShell 재시작

3. **임시 해결 (PATH 수동 추가):**
   ```powershell
   $env:Path += ";C:\Program Files\Git\cmd"
   git --version
   ```

---

### 문제 2: `ModuleNotFoundError: No module named 'Average'`

**증상:**
```
ModuleNotFoundError: No module named 'Average'
```

**원인:**
- 프로젝트 루트가 Python import 경로에 포함되지 않음
- 상대 경로 import가 실패함

**해결 방법:**

**옵션 1: PYTHONPATH 설정 (권장)**
```powershell
# 프로젝트 루트로 이동
cd "C:\Users\YourName\Documents\Federated-Learning"

# Python 경로에 추가
$env:PYTHONPATH = (Get-Location).Path

# 확인
echo $env:PYTHONPATH

# 이제 스크립트 실행
python .\Average\aggregate_round.py --round 1 --min_clients 2
```

**옵션 2: 매번 자동 설정 (편리함)**

`run_client.ps1` 스크립트 생성:
```powershell
@'
# 가상환경 활성화
& .\activate_fl.ps1

# Python 경로 설정
$env:PYTHONPATH = (Get-Location).Path

# 클라이언트 실행
python .\Clients\client_update.py @args
'@ | Out-File -FilePath run_client.ps1 -Encoding UTF8
```

사용:
```powershell
.\run_client.ps1 --round 1 --client_id 1 --csv "data.csv" --feature_cols year --target_col chloride --seq_len 10
```

---

### 문제 3: `ModuleNotFoundError: No module named 'Server'`

**증상:**
```
ModuleNotFoundError: No module named 'Server'
```

**원인:**
- `client_update.py`에서 `from Server...` 형태로 import
- 프로젝트 루트가 import 경로에 없음

**해결 방법:**

문제 2와 동일하게 PYTHONPATH 설정:

```powershell
cd "C:\Users\YourName\Documents\Federated-Learning"
$env:PYTHONPATH = (Get-Location).Path
python .\Clients\client_update.py [args...]
```

---

### 문제 4: `Author identity unknown` (Git 커밋 실패)

**증상:**
```
Author identity unknown

*** Please tell me who you are.

fatal: unable to auto-detect email address
```

**원인:**
- Git 사용자 정보가 설정되지 않음
- `client_update.py`가 자동으로 커밋/푸시를 시도함

**해결 방법:**

**전역 설정 (권장):**
```powershell
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

**로컬 설정 (현재 저장소만):**
```powershell
cd "C:\Users\YourName\Documents\Federated-Learning"
git config user.name "Your Name"
git config user.email "you@example.com"
```

**설정 확인:**
```powershell
git config --global --list
# 또는
git config --list
```

**설정 후 다시 실행:**
```powershell
python .\Clients\client_update.py [args...]
```

---

### 문제 5: PowerShell 스크립트 실행 정책 오류

**증상:**
```
이 시스템에서 스크립트를 실행할 수 없으므로 activate_fl.ps1 파일을 로드할 수 없습니다.
```

**원인:**
- Windows 보안 정책으로 스크립트 실행이 차단됨

**해결 방법:**

**옵션 1: 실행 정책 변경 (권장)**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**옵션 2: 일회성 우회**
```powershell
PowerShell -ExecutionPolicy Bypass -File .\activate_fl.ps1
```

**옵션 3: 직접 활성화**
```powershell
.\FL_env\Scripts\Activate.ps1
```

---

### 문제 6: 패키지 설치 오류 (pip install 실패)

**증상:**
```
ERROR: Could not find a version that satisfies the requirement torch
```

**원인:**
- 인터넷 연결 문제
- pip 버전이 오래됨
- Python 버전 호환성 문제

**해결 방법:**

**1. pip 업그레이드:**
```powershell
python -m pip install --upgrade pip
```

**2. 개별 패키지 설치 시도:**
```powershell
pip install torch
pip install numpy pandas scikit-learn matplotlib
```

**3. 프록시 사용 환경이라면:**
```powershell
pip install --proxy http://proxy-server:port torch
```

**4. PyTorch 공식 사이트에서 설치 명령 확인:**
[https://pytorch.org/get-started/locally/](https://pytorch.org/get-started/locally/)

---

### 문제 7: CSV 파일 경로 오류

**증상:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'client_data.csv'
```

**원인:**
- 파일 경로가 잘못됨
- 상대 경로 대신 절대 경로가 필요함

**해결 방법:**

**1. 절대 경로 사용:**
```powershell
python .\Clients\client_update.py --csv "C:\Users\YourName\Documents\data.csv" [other args...]
```

**2. 경로 확인:**
```powershell
# 파일 존재 확인
Test-Path "C:\path\to\your\data.csv"

# 현재 폴더의 파일 목록
dir *.csv
```

**3. 경로에 공백이 있다면 따옴표로 감싸기:**
```powershell
--csv "C:\My Documents\Federated Learning\data.csv"
```

---

### 문제 8: 메모리 부족 (Out of Memory)

**증상:**
```
RuntimeError: CUDA out of memory
또는
MemoryError
```

**원인:**
- 데이터가 너무 큼
- 배치 크기가 너무 큼
- GPU 메모리 부족

**해결 방법:**

**1. 배치 크기 줄이기:**
```python
# client_update.py 또는 config 파일에서
batch_size = 16  # 32 → 16으로 줄임
```

**2. 시퀀스 길이 줄이기:**
```powershell
--seq_len 5  # 10 → 5로 줄임
```

**3. 데이터 샘플링:**
```python
# 데이터의 일부만 사용
data = data.sample(frac=0.5)  # 50%만 사용
```

**4. CPU 사용:**
```python
device = 'cpu'  # GPU 대신 CPU 사용
```

---

### 문제 9: 가상환경이 활성화되지 않음

**증상:**
- `(FL_env)` 표시가 안 보임
- 패키지를 찾을 수 없음

**원인:**
- 가상환경이 제대로 활성화되지 않음

**해결 방법:**

**1. 직접 활성화:**
```powershell
.\FL_env\Scripts\Activate.ps1
```

**2. 활성화 확인:**
```powershell
# Python 경로 확인
Get-Command python | Select-Object Source

# FL_env 안의 python.exe를 사용해야 함
# 예: C:\...\Federated-Learning\FL_env\Scripts\python.exe
```

**3. 패키지 설치 위치 확인:**
```powershell
pip list
pip show torch
```

**4. 가상환경 재생성:**
```powershell
# 기존 가상환경 삭제
Remove-Item -Recurse -Force FL_env

# 다시 생성
python setup_fl_env.py
```

---

## 📚 자주 확인할 체크리스트

실행 전에 항상 확인하세요:

### ✅ 기본 체크리스트

```powershell
# 1. 현재 위치가 프로젝트 루트인가?
pwd
# 출력: ...\Federated-Learning

# 2. 필요한 폴더들이 있는가?
dir
# Average/, Clients/, Server/ 폴더가 보여야 함

# 3. 가상환경이 활성화되었는가?
# 프롬프트에 (FL_env) 표시 확인

# 4. PYTHONPATH가 설정되었는가?
echo $env:PYTHONPATH
# 프로젝트 루트 경로가 출력되어야 함

# 5. Git 사용자 정보가 설정되었는가?
git config --list | Select-String "user"
```

---

## 🎯 빠른 실행 가이드

매번 같은 명령어를 입력하기 번거롭다면, 이 스크립트를 사용하세요:

**`start_client.ps1` 생성:**

```powershell
@'
# Federated Learning Client 시작 스크립트

Write-Host "Federated Learning Client Starting..." -ForegroundColor Cyan

# 1. 가상환경 활성화
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\activate_fl.ps1

# 2. Python 경로 설정
Write-Host "Setting PYTHONPATH..." -ForegroundColor Yellow
$env:PYTHONPATH = (Get-Location).Path

# 3. Git 설정 확인
$gitUser = git config user.name
if (-not $gitUser) {
    Write-Host "WARNING: Git user not configured!" -ForegroundColor Red
    Write-Host "Run: git config --global user.name 'Your Name'" -ForegroundColor Yellow
    exit 1
}

Write-Host "Environment ready!" -ForegroundColor Green
Write-Host "You can now run: python .\Clients\client_update.py [args]" -ForegroundColor Green
'@ | Out-File -FilePath start_client.ps1 -Encoding UTF8
```

**사용:**
```powershell
.\start_client.ps1
python .\Clients\client_update.py --round 1 --client_id 1 ...
```

---

## 💡 유용한 PowerShell 명령어

### 경로 관련
```powershell
# 현재 경로 확인
pwd
Get-Location

# 상위 폴더로 이동
cd ..

# 특정 폴더로 이동
cd "C:\Users\YourName\Documents\Federated-Learning"

# 폴더 내용 확인
dir
Get-ChildItem
```

### 파일 관련
```powershell
# 파일 존재 확인
Test-Path "file.csv"

# 파일 내용 미리보기
Get-Content "file.csv" | Select-Object -First 10

# 파일 검색
Get-ChildItem -Recurse -Filter "*.csv"
```

### 환경변수 관련
```powershell
# 환경변수 확인
$env:PYTHONPATH
$env:PATH

# 환경변수 설정
$env:PYTHONPATH = "C:\path\to\project"

# 환경변수 추가
$env:PATH += ";C:\new\path"
```

### Git 관련
```powershell
# 현재 브랜치 확인
git branch

# 상태 확인
git status

# 최근 커밋 보기
git log --oneline -5

# 원격 저장소 확인
git remote -v
```

---

## 📞 도움 받기

### 문제가 계속 발생한다면:

1. **로그 파일 확인**
   ```powershell
   Get-Content .\logs\client.log | Select-Object -Last 50
   ```

2. **시스템 정보 수집**
   ```powershell
   python --version
   pip --version
   git --version
   $PSVersionTable.PSVersion
   ```

3. **오류 메시지 전체 복사**
   - 빨간색 오류 메시지 전체를 복사
   - 실행한 명령어도 함께 기록

4. **연락처**
   - 프로젝트 관리자: [이메일]
   - GitHub Issues: [Repository URL]/issues
   - 문서: `FL_SETUP.md`, `CLIENT_GUIDE.md`

---

## ✨ 성공적인 실행 예시

모든 것이 제대로 설정되면 이렇게 실행됩니다:

```powershell
PS C:\Users\YourName\Documents\Federated-Learning> .\start_client.ps1
Federated Learning Client Starting...
Activating virtual environment...
[OK] Virtual environment activated successfully!
Setting PYTHONPATH...
Environment ready!

(FL_env) PS C:\Users\YourName\Documents\Federated-Learning> python .\Clients\client_update.py --round 1 --client_id 1 --csv "data.csv" --feature_cols year --target_col chloride --seq_len 10

[INFO] Starting client 1 training for round 1
[INFO] Loading data from data.csv
[INFO] Data loaded: 1000 samples
[INFO] Sequence length: 10
[INFO] Training...
[INFO] Epoch 1/5 - Loss: 0.4523
[INFO] Epoch 2/5 - Loss: 0.3421
[INFO] Epoch 3/5 - Loss: 0.2876
[INFO] Epoch 4/5 - Loss: 0.2443
[INFO] Epoch 5/5 - Loss: 0.2156
[INFO] Training complete!
[INFO] Saving model parameters...
[INFO] Committing and pushing changes...
[SUCCESS] Client 1 finished round 1
```

---

## 🎓 다음 단계

환경 설정이 완료되었다면:

1. ✅ **테스트 실행**: `python test_fl_env.py`
2. ✅ **데이터 준비**: CSV 파일 포맷 확인
3. ✅ **서버 정보 확인**: 서버 IP 주소와 라운드 번호 받기
4. ✅ **첫 훈련 시작**: 위의 명령어로 실행
5. ✅ **결과 확인**: GitHub 또는 서버에서 모델 업데이트 확인

**Happy Training! 🚀**

---

*마지막 업데이트: 2025-01-07*
*더 자세한 정보: `FL_SETUP.md`, `README.md`*