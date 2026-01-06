# Federated-Learning

```mermaid
flowchart TB
  subgraph GitHubRepo["GitHub Repo: Federated-Learning"]
    R1["Rounds/round_0001/"]
    Rk["Rounds/round_000k/"]
  end

  subgraph Server["Main Server"]
    S0["git pull"]
    S1["Train global model (round k)"]
    S2["Write global files
    Rounds/round_000k/global.pt
    Rounds/round_000k/global.json"]
    S3["git commit & push"]
    S4["git pull (collect client updates)"]
    S5["Aggregate updates (FedAvg)
    Average/aggregate_round.py --round k"]
    S6["Write aggregated files
    Rounds/round_000k/aggregated.pt
    Rounds/round_000k/aggregated.json"]
    S7["Promote to next global
    Rounds/round_000(k+1)/global.pt,json"]
    S8["git commit & push"]
  end

  subgraph Client1["Client 1"]
    C1a["git pull"]
    C1b["Load global_k"]
    C1c["Local train on private CSV"]
    C1d["Write update files
    client_1.pt / client_1.json"]
    C1e["git commit & push"]
  end

  subgraph Client2["Client 2"]
    C2a["git pull"]
    C2b["Load global_k"]
    C2c["Local train on private CSV"]
    C2d["Write update files
    client_2.pt / client_2.json"]
    C2e["git commit & push"]
  end

  S0 --> S1 --> S2 --> S3 --> GitHubRepo
  GitHubRepo --> C1a --> C1b --> C1c --> C1d --> C1e --> GitHubRepo
  GitHubRepo --> C2a --> C2b --> C2c --> C2d --> C2e --> GitHubRepo
  GitHubRepo --> S4 --> S5 --> S6 --> S7 --> S8 --> GitHubRepo

