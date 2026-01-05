# Clients/client_update.py
import argparse
import os
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

from Server.model_lstm import LSTMRegressor
from Clients.data_seq import make_windows
from Average.io_weights import load_state_dict, load_json, save_state_dict, save_json
from utils_git import git_pull, git_commit_push

def train_local(model, loader, device, epochs: int, lr: float):
    model.train()
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.MSELoss()

    total_last = None
    for _ in range(epochs):
        total = 0.0
        n = 0
        for xb, yb in loader:
            xb = xb.to(device)
            yb = yb.to(device)

            pred = model(xb)
            loss = loss_fn(pred, yb)

            opt.zero_grad()
            loss.backward()
            opt.step()

            total += float(loss.item()) * xb.size(0)
            n += xb.size(0)
        total_last = total / max(n, 1)
    return float(total_last)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--round", type=int, required=True)
    p.add_argument("--client_id", type=int, required=True)
    p.add_argument("--csv", type=str, required=True)          # 클라이언트 로컬 csv 경로
    p.add_argument("--feature_cols", type=str, required=True) # 예: "x1,x2,x3"
    p.add_argument("--target_col", type=str, required=True)   # 예: "y"
    p.add_argument("--seq_len", type=int, default=10)
    p.add_argument("--batch_size", type=int, default=32)
    p.add_argument("--epochs", type=int, default=5)
    p.add_argument("--lr", type=float, default=1e-3)
    p.add_argument("--device", type=str, default="cpu")
    args = p.parse_args()

    git_pull()

    rdir = os.path.join("Rounds", f"round_{args.round:04d}")
    gmeta = os.path.join(rdir, "global.json")
    gpath = os.path.join(rdir, "global.pt")
    if not os.path.exists(gmeta) or not os.path.exists(gpath):
        raise FileNotFoundError("global model not found. Did server push_global?")

    meta = load_json(gmeta)
    cfg = meta["config"]

    # 데이터 로드
    df = pd.read_csv(args.csv)
    fcols = [c.strip() for c in args.feature_cols.split(",") if c.strip()]
    tcol = args.target_col.strip()

    features = df[fcols].to_numpy(dtype=np.float32)
    targets = df[tcol].to_numpy(dtype=np.float32)

    X, y = make_windows(features, targets, seq_len=args.seq_len)

    ds = TensorDataset(torch.from_numpy(X), torch.from_numpy(y))
    loader = DataLoader(ds, batch_size=args.batch_size, shuffle=True, drop_last=False)

    device = torch.device(args.device)

    # 모델 구성(서버 config와 동일해야 함)
    model = LSTMRegressor(
        input_size=cfg["input_size"],
        hidden_size=cfg["hidden_size"],
        num_layers=cfg["num_layers"],
        output_size=cfg["output_size"],
        dropout=cfg["dropout"],
    ).to(device)

    # global state 로드
    global_sd = load_state_dict(gpath)
    model.load_state_dict({k: v.to(device) for k, v in global_sd.items()}, strict=True)

    # 로컬 학습
    loss = train_local(model, loader, device, epochs=args.epochs, lr=args.lr)

    # update 저장
    up_dir = os.path.join(rdir, "updates")
    up_path = os.path.join(up_dir, f"client_{args.client_id}.pt")
    up_meta = os.path.join(up_dir, f"client_{args.client_id}.json")

    save_state_dict(up_path, model.state_dict())
    save_json(up_meta, {
        "round": args.round,
        "client_id": args.client_id,
        "n_samples": len(ds),
        "local_loss": loss,
        "weights_path": up_path
    })

    git_commit_push(f"Client {args.client_id} update round {args.round:04d}")

if __name__ == "__main__":
    main()
