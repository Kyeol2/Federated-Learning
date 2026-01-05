# Clients/client_update.py
import argparse
import os
from Average.io_weights import load_state_dict, save_state_dict, save_json
from utils_git import git_pull, git_commit_push

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--round", type=int, required=True)
    p.add_argument("--client_id", type=int, required=True)
    p.add_argument("--n_samples", type=int, required=True)  # 로컬 데이터 개수
    args = p.parse_args()

    git_pull()

    rdir = os.path.join("Rounds", f"round_{args.round:04d}")
    gpath = os.path.join(rdir, "global.pt")
    if not os.path.exists(gpath):
        raise FileNotFoundError(f"global not found: {gpath}")

    global_sd = load_state_dict(gpath)

    # 여기서 네 로컬 모델 생성 후 global_sd 로드 → 로컬 학습 → updated_sd 추출
    # model = BayesianNN(...)
    # model.load_state_dict(global_sd, strict=True)
    # train(model, local_loader, ...)
    # updated_sd = model.state_dict()

    raise NotImplementedError("여기에 로컬 학습 코드를 연결해야 함")

    up_dir = os.path.join(rdir, "updates")
    up_path = os.path.join(up_dir, f"client_{args.client_id}.pt")
    meta_path = os.path.join(up_dir, f"client_{args.client_id}.json")

    save_state_dict(up_path, updated_sd)
    save_json(meta_path, {
        "round": args.round,
        "client_id": args.client_id,
        "n_samples": args.n_samples,
        "weights_path": up_path,
    })

    git_commit_push(f"Client {args.client_id} update round {args.round:04d}")

if __name__ == "__main__":
    main()
