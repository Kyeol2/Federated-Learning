# Average/aggregate_round.py
import argparse
import glob
import os
from Average.io_weights import load_state_dict, load_json, save_state_dict, save_json
from Average.fedavg import fedavg
from utils_git import git_pull, git_commit_push

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--round", type=int, required=True)
    p.add_argument("--min_clients", type=int, default=1)  # PoC는 1로도 가능, 보통 3
    args = p.parse_args()

    git_pull()

    rdir = os.path.join("Rounds", f"round_{args.round:04d}")
    up_dir = os.path.join(rdir, "updates")
    meta_paths = sorted(glob.glob(os.path.join(up_dir, "client_*.json")))

    if len(meta_paths) < args.min_clients:
        raise RuntimeError(f"not enough client updates: {len(meta_paths)} < {args.min_clients}")

    sds = []
    ns = []
    clients = []

    for mp in meta_paths:
        meta = load_json(mp)
        wpath = meta["weights_path"]
        sd = load_state_dict(wpath)
        sds.append(sd)
        ns.append(meta["n_samples"])
        clients.append(meta["client_id"])

    agg = fedavg(sds, ns)

    agg_path = os.path.join(rdir, "aggregated.pt")
    agg_meta_path = os.path.join(rdir, "aggregated.json")

    save_state_dict(agg_path, agg)
    save_json(agg_meta_path, {
        "round": args.round,
        "num_clients": len(clients),
        "clients": clients,
        "weights": ns,
        "aggregated_path": agg_path
    })

    git_commit_push(f"Aggregate round {args.round:04d}")

if __name__ == "__main__":
    main()
