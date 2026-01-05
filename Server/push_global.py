# Server/push_global.py
import argparse
import os
import torch
from Server.model_lstm import LSTMRegressor
from Average.io_weights import save_state_dict, save_json
from utils_git import git_pull, git_commit_push

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--round", type=int, required=True)
    p.add_argument("--input_size", type=int, required=True)     # feature 개수
    p.add_argument("--hidden_size", type=int, default=64)
    p.add_argument("--num_layers", type=int, default=1)
    p.add_argument("--output_size", type=int, default=1)
    p.add_argument("--dropout", type=float, default=0.0)
    args = p.parse_args()

    git_pull()

    model = LSTMRegressor(
        input_size=args.input_size,
        hidden_size=args.hidden_size,
        num_layers=args.num_layers,
        output_size=args.output_size,
        dropout=args.dropout,
    )

    rdir = os.path.join("Rounds", f"round_{args.round:04d}")
    gpath = os.path.join(rdir, "global.pt")
    gmeta = os.path.join(rdir, "global.json")

    save_state_dict(gpath, model.state_dict())
    save_json(gmeta, {
        "round": args.round,
        "model": "LSTMRegressor",
        "config": {
            "input_size": args.input_size,
            "hidden_size": args.hidden_size,
            "num_layers": args.num_layers,
            "output_size": args.output_size,
            "dropout": args.dropout,
        },
        "global_path": gpath
    })

    git_commit_push(f"Push global round {args.round:04d}")

if __name__ == "__main__":
    main()
