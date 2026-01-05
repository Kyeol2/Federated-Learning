# Average/aggregate_round.py
import shutil
import argparse
import glob
import os
from Average.io_weights import load_state_dict, load_json, save_state_dict, save_json
from Average.fedavg import fedavg
from utils_git import git_pull, git_commit_push

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--round", type=int, required=True)
    p.add_argument("--min_clients", type=int, default=1)  # PoC는 1도 가능, 보통 3
    args = p.parse_args()

    git_pull()

    rdir = os.path.join("Rounds", f"round_{args.round:04d}")
    up_dir = os.path.join(rdir, "updates")
    meta_paths = sorted(glob.glob(os.path.join(up_dir, "client_*.json")))

    if len(meta_paths) < args.min_clients:
        raise RuntimeError(f"not enough client updates: {len(meta_paths)} < {args.min_clients}")

    sds, ns, clients = [], [], []
    for mp in meta_paths:
        meta = load_json(mp)
        if meta.get("round") != args.round:
            continue
        sd = load_state_dict(meta["weights_path"])
        sds.append(sd)
        ns.append(int(meta["n_samples"]))
        clients.append(int(meta["client_id"]))

    if len(sds) < args.min_clients:
        raise RuntimeError("not enough valid updates after filtering by round")

    agg = fedavg(sds, ns)

    agg_path = os.path.join(rdir, "aggregated.pt")
    agg_meta_path = os.path.join(rdir, "aggregated.json")

    save_state_dict(agg_path, agg)
    save_json(agg_meta_path, {
        "round": args.round,
        "num_clients": len(clients),
        "clients": clients,
        "n_samples": ns,
        "aggregated_path": agg_path
    })

     # ------------------------------------------------------------
    # (NEW) Promote aggregated -> next round global (auto)
    # ------------------------------------------------------------
    next_round = args.round + 1
    next_rdir = os.path.join("Rounds", f"round_{next_round:04d}")
    os.makedirs(next_rdir, exist_ok=True)

    next_global_pt = os.path.join(next_rdir, "global.pt")
    next_global_json = os.path.join(next_rdir, "global.json")

    # 방법 A: 파일 복사로 빠르게 처리 (가장 단순/안전)
    shutil.copyfile(agg_path, next_global_pt)

    # config는 현재 round의 global.json을 그대로 승계
    cur_global_json = os.path.join(rdir, "global.json")
    if os.path.exists(cur_global_json):
        shutil.copyfile(cur_global_json, next_global_json)
    else:
        # 혹시 global.json이 없으면 aggregated meta 기반으로 최소한 생성
        save_json(next_global_json, {"config": load_json(agg_meta_path).get("config", {})})

    git_commit_push(f"Aggregate round {args.round:04d}")

if __name__ == "__main__":
    main()