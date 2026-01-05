# Server/push_global.py
import argparse
import os
from Average.io_weights import save_state_dict, save_json
from utils_git import git_pull, git_commit_push

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--round", type=int, required=True)
    args = p.parse_args()

    git_pull()

    # 여기서 네가 실제로 모델을 만들고 state_dict를 뽑아야 함
    # 예) model = BayesianNN(...)
    #     state_dict = model.state_dict()

    raise NotImplementedError("여기에 글로벌 모델 생성 + state_dict 추출 코드를 연결해야 함")

    rdir = os.path.join("Rounds", f"round_{args.round:04d}")
    gpath = os.path.join(rdir, "global.pt")
    gmeta = os.path.join(rdir, "global.json")

    save_state_dict(gpath, state_dict)
    save_json(gmeta, {"round": args.round, "global_path": gpath})

    git_commit_push(f"Push global round {args.round:04d}")

if __name__ == "__main__":
    main()
