# Federated Learning Workflow

```mermaid
%%{init: {
  "theme": "base",
  "themeVariables": {
    "background": "#e3f2fd",
    "lineColor": "#111111",
    "primaryColor": "#e3f2fd",
    "primaryTextColor": "#0d47a1",
    "primaryBorderColor": "#1565c0",
    "fontFamily": "Pretendard, Apple SD Gothic Neo, Malgun Gothic, Arial"
  },
  "flowchart": { "curve": "linear" }
}}%%

flowchart TB

classDef server fill:#e3f2fd,stroke:#1565c0,stroke-width:3px,color:#0d47a1
classDef client fill:#fff3e0,stroke:#ef6c00,stroke-width:3px,color:#e65100
classDef repo fill:#f3e5f5,stroke:#7b1fa2,stroke-width:3px,color:#4a148c
classDef step fill:#ffffff,stroke:#111111,stroke-width:2px,color:#111111
classDef file fill:#fff9c4,stroke:#f9a825,stroke-width:2px,color:#5d4037

%% =========================
%% GitHub Repository
%% =========================
subgraph GH["🌐 GitHub Repository: Federated-Learning"]
direction TB
GH1["📁 Rounds/round_0001/\n- global.pt\n- global.json\n- updates/"]:::file
GHk["📁 Rounds/round_000k/\n- aggregated.pt\n- aggregated.json\n- updates/"]:::file
GHk1["📁 Rounds/round_000(k+1)/\n- global.pt\n- global.json"]:::file
end
class GH repo

%% =========================
%% Main Server (Initial: once)
%% =========================
subgraph SV0["🖥️ Main Server (Initial: run once)"]
direction TB
S0A["A. FL 저장소로 이동\n환경: Windows PowerShell / Main server\nCmd: cd \"F:\\OneDrive\\문서\\GitHub\\Federated-Learning\""]:::step
S0B["B. 저장소 상태 최신화\n설명: GitHub 최신 상태를 서버 로컬에 반영\nCmd: git pull"]:::step
S0C["C. 실행 환경 확인\n설명: Python 버전 확인\nCmd: Phtion –version"]:::step
S0D["D. 글로벌 학습 스크립트 실행(초기 1회)\n설명: round_0001에 global.* 생성 후 자동 push\nCmd:\npython ./train_global_and_push.py\n--round 1\n--csv \"…\\Global.csv\"\n--feature_cols \"year\"\n--target_col \"chloride\"\n--seq_len 10"]:::step
S0E["E. 결과 생성 확인\n설명: round_0001 파일 확인\nCmd: dir .\\Rounds\\round_0001\\"]:::step

S0A --> S0B --> S0C --> S0D --> S0E
end
class SV0 server

%% =========================
%% Client 1
%% =========================
subgraph C1["👤 Client 1 (Round k)"]
direction TB
C1A["A. FL 저장소로 이동\n환경: Windows PowerShell / Client\nCmd: cd \"F:\\Users\\Ki-Yeol\\Documents\\GitHub\\Federated-Learning\""]:::step
C1B["B. MainServer 최신 Global 받기\n설명: 로컬 저장소 최신화\nCmd: Git pull"]:::step
C1C["C. 실행 환경 확인\n설명: Python 버전 확인\nCmd: Phtion –version"]:::step

C1D1["D1. 로컬 학습(파이썬 경로 OK)\n설명: round 1 update 생성+자동 push\nCmd:\npython .\\Clients\\client_update.py\n--round 1\n--client_id 1\n--csv \"C:\\Users\\Ki-Yeol\\Documents\\GitHub\\csv\\Client1.csv\"\n--feature_cols \"year\"\n--target_col \"chloride\"\n--seq_len 10"]:::step

C1D2["D2. 로컬 학습(파이썬 경로 문제)\n설명: python.exe 경로 직접 지정\nCmd: & \"c:\\Users\\Ki-Yeol\\anaconda3\\python.exe\" (이하 동문)"]:::step

C1A --> C1B --> C1C --> C1D1
C1C --> C1D2
end
class C1 client

%% =========================
%% Client 2 (same)
%% =========================
subgraph C2["👤 Client 2 (Round k)"]
direction TB
C2A["A. FL 저장소로 이동\n환경: Windows PowerShell / Client\nCmd: cd \"F:\\Users\\Ki-Yeol\\Documents\\GitHub\\Federated-Learning\""]:::step
C2B["B. MainServer 최신 Global 받기\n설명: 로컬 저장소 최신화\nCmd: Git pull"]:::step
C2C["C. 실행 환경 확인\n설명: Python 버전 확인\nCmd: Phtion –version"]:::step

C2D1["D1. 로컬 학습(파이썬 경로 OK)\n설명: round 1 update 생성+자동 push\nCmd:\npython .\\Clients\\client_update.py\n--round 1\n--client_id 2\n--csv \"C:\\Users\\Ki-Yeol\\Documents\\GitHub\\csv\\Client2.csv\"\n--feature_cols \"year\"\n--target_col \"chloride\"\n--seq_len 10"]:::step

C2D2["D2. 로컬 학습(파이썬 경로 문제)\n설명: python.exe 경로 직접 지정\nCmd: & \"c:\\Users\\Ki-Yeol\\anaconda3\\python.exe\" (이하 동문)"]:::step

C2A --> C2B --> C2C --> C2D1
C2C --> C2D2
end
class C2 client

%% =========================
%% Main Server (Round cycle: repeat)
%% =========================
subgraph SVK["🖥️ Main Server (Round k: repeat)"]
direction TB
SKA["A. FL 저장소로 이동\n환경: Windows PowerShell / Main server\nCmd: cd \"F:\\OneDrive\\문서\\GitHub\\Federated-Learning\""]:::step
SKB["B. 저장소 상태 최신화\n설명: client 업데이트 수집\nCmd: Git pull"]:::step
SKC["C. 업데이트 파일 확인\n설명: round_0001 updates 확인\nCmd: dir .\\Rounds\\round_0001\\updates\\"]:::step
SKD["D. 프로젝트 루트 import 경로 설정\n설명: 'No module named Average' 방지\nCmd: $env:PYTHONPATH = (Get-Location).Path"]:::step
SKE["E. 집계 실행(FedAvg)\n설명: aggregated 생성 + 다음 global 승격 + 자동 push\nCmd: python .\\Average\\aggregate_round.py --round 1 --min_clients 2"]:::step

SKA --> SKB --> SKC --> SKD --> SKE
end
class SVK server

%% =========================
%% Connections via GitHub
%% =========================
S0E -->|"Publish global (round 1)"| GH1
GH1 -->|"Fetch global_k"| C1B
GH1 -->|"Fetch global_k"| C2B

C1D1 -->|"Submit update_1"| GHk
C2D1 -->|"Submit update_2"| GHk
C1D2 -->|"Submit update_1"| GHk
C2D2 -->|"Submit update_2"| GHk

GHk -->|"Collect updates"| SKB
SKE -->|"Publish aggregated + promote"| GHk1

GHk1 -. "Next round (k+1)" .-> C1B
GHk1 -. "Next round (k+1)" .-> C2B
```