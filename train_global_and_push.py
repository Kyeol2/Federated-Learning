import argparse
import os
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

from Server.model_lstm import LSTMRegressor
from Clients.data_seq import make_windows
from Average.io_weights import save_state_dict, save_json
from utils_git import git_pull, git_commit_push


def train(model, loader, device, epochs: int, lr: float):
    model.train()
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.MSELoss()

    last_loss = None
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
        last_loss = total / max(n, 1)
    return float(last_loss)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--round", type=int, required=True)

    # 서버 데이터
    p.add_argument("--csv", type=str, required=True)
    p.add_argument("--feature_cols", type=str, required=True)  # 예: "x1,x2,x3"
    p.add_argument("--target_col", type=str, required=True)    # 예: "y"
    p.add_argument("--seq_len", type=int, default=10)

    # 모델/학습 설정
    p.add_argument("--hidden_size", type=int, default=64)
    p.add_argument("--num_layers", type=int, default=1)
    p.add_argument("--output_size", type=int, default=1)
    p.add_argument("--dropout", type=float, default=0.0)
    p.add_argument("--epochs", type=int, default=10)
    p.add_argument("--batch_size", type=int, default=32)
    p.add_argument("--lr", type=float, default=1e-3)
    p.add_argument("--device", type=str, default="cpu")
    args = p.parse_args()

    git_pull()

    # 데이터 로드
    df = pd.read_csv(args.csv)
    fcols = [c.strip() for c in args.feature_cols.split(",") if c.strip()]
    tcol = args.target_col.strip()

    features = df[fcols].to_numpy(dtype=np.float32)
    targets = df[tcol].to_numpy(dtype=np.float32)

    # 시계열 윈도우
    X, y = make_windows(features, targets, seq_len=args.seq_len)
    ds = TensorDataset(torch.from_numpy(X), torch.from_numpy(y))
    loader = DataLoader(ds, batch_size=args.batch_size, shuffle=True, drop_last=False)

    input_size = X.shape[-1]
    device = torch.device(args.device)

    # 모델 생성
    model = LSTMRegressor(
        input_size=input_size,
        hidden_size=args.hidden_size,
        num_layers=args.num_layers,
        output_size=args.output_size,
        dropout=args.dropout,
    ).to(device)

    # 서버에서 먼저 학습
    loss = train(model, loader, device, epochs=args.epochs, lr=args.lr)

    # global 저장 + 업로드
    rdir = os.path.join("Rounds", f"round_{args.round:04d}")
    gpath = os.path.join(rdir, "global.pt")
    gmeta = os.path.join(rdir, "global.json")

    save_state_dict(gpath, model.state_dict())
    save_json(gmeta, {
        "round": args.round,
        "model": "LSTMRegressor",
        "trained_on": "server_csv",
        "server_train_loss": loss,
        "config": {
            "input_size": int(input_size),
            "hidden_size": args.hidden_size,
            "num_layers": args.num_layers,
            "output_size": args.output_size,
            "dropout": args.dropout,
            "seq_len": args.seq_len,
        },
        "global_path": gpath
    })

    git_commit_push(f"Train+Push global round {args.round:04d}")


if __name__ == "__main__":
    main()
