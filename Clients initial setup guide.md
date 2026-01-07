````md
# Federated-Learning Troubleshooting (Windows / PowerShell)

이 문서는 클라이언트/서버에서 Federated-Learning 워크플로우를 실행할 때 자주 발생하는 오류와 해결 방법을 정리한 것입니다.  
(Windows PowerShell 기준)

---

## 1) `git` 명령어가 인식되지 않음

### 증상
```powershell
git : 'git' 용어가 cmdlet, 함수, 스크립트 파일 또는 실행할 수 있는 프로그램 이름으로 인식되지 않습니다.
````

### 원인

* Git for Windows가 설치되지 않았거나
* 설치되어도 PATH에 등록되지 않아 `git` 명령이 인식되지 않음

### 해결

1. 설치 여부 확인

```powershell
where.exe git
git --version
```

2. Git 설치 후 PowerShell 재시작

* Git for Windows 설치 시 옵션에서 아래 항목 선택 권장:

  * `Git from the command line and also from 3rd-party software`

3. PATH만 안 잡힌 경우(임시 해결)

```powershell
$env:Path += ";C:\Program Files\Git\cmd"
git --version
```

---

## 2) `ModuleNotFoundError: No module named 'Average'` (서버 집계 실행)

### 증상

```text
ModuleNotFoundError: No module named 'Average'
```

### 원인

* 프로젝트 루트가 파이썬 import 경로에 포함되지 않아서 `Average.*` 모듈을 못 찾음

### 해결(권장)

리포지터리 루트에서 아래를 먼저 실행:

```powershell
cd "...\Federated-Learning"
$env:PYTHONPATH = (Get-Location).Path
python .\Average\aggregate_round.py --round 1 --min_clients 2
```

---

## 3) `ModuleNotFoundError: No module named 'Server'` (클라이언트 로컬 학습 실행)

### 증상

```text
ModuleNotFoundError: No module named 'Server'
```

### 원인

* `Clients/client_update.py`에서 `from Server...` 처럼 루트 기준 import를 사용하는데,
  실행 시 프로젝트 루트가 import 경로로 잡히지 않으면 발생함

### 해결(권장: PowerShell에서 PYTHONPATH 설정)

```powershell
cd "C:\Users\hopea\Federated-Learning"
$env:PYTHONPATH = (Get-Location).Path
python .\Clients\client_update.py --round 1 --client_id 3 --csv "C:\...\client3.csv" --feature_cols year --target_col chloride --seq_len 10
```

---

## 4) `Author identity unknown` / `fatal: unable to auto-detect email address` (자동 commit/push 실패)

### 증상

```text
Author identity unknown

*** Please tell me who you are.

fatal: unable to auto-detect email address (...)
subprocess.CalledProcessError: Command '['git', 'commit', ...]' returned non-zero exit status 128.
```

### 원인

* 해당 PC에서 Git 커밋 작성자 정보(`user.name`, `user.email`)가 설정되지 않아서
  `git commit`이 실패함
* `Clients/client_update.py` 내부에서 자동 commit/push를 수행하는 과정에서 에러가 터짐

### 해결(1회만 설정하면 됨)

#### 4-1) 전체 PC에 적용(권장: global)

```powershell
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

설정 확인:

```powershell
git config --global --list
```

#### 4-2) 현재 저장소에만 적용(글로벌 설정이 싫을 때)

```powershell
git config user.name "Your Name"
git config user.email "you@example.com"
```

설정 후 다시 실행:

```powershell
python .\Clients\client_update.py --round 1 --client_id 3 --csv "C:\...\client3.csv" --feature_cols year --target_col chloride --seq_len 10
```

---

## 5) (참고) 현재 위치/경로 확인 체크리스트

실행 전 아래 2개를 확인하면 경로 관련 오류를 많이 줄일 수 있음.

### 5-1) 현재 폴더가 리포지터리 루트인지 확인

```powershell
pwd
dir
```

* `Average/`, `Clients/`, `Server/` 폴더가 보여야 정상

### 5-2) 폴더 존재 확인(예: Server 폴더)

```powershell
dir .\Server
```

---

## 6) (옵션) 클라이언트 가상환경 생성 (처음 1회)

> 파이썬 자체 설치는 각 PC에서 필요합니다.
> 아래는 패키지 설치를 위한 venv 생성/활성화용 기본 절차입니다.

```powershell
cd "C:\Users\...\Federated-Learning"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version
pip --version
```

---

## 빠른 요약

* `git` 안 됨 → Git 설치/PATH 확인
* `No module named Server/Average` → 루트에서 `$env:PYTHONPATH = (Get-Location).Path` 후 실행
* `Author identity unknown` → `git config --global user.name / user.email` 설정

```
```
