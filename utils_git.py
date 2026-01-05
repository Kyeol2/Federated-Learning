# utils_git.py
import subprocess

def _run(cmd: list[str]):
    subprocess.run(cmd, check=True)

def git_pull():
    _run(["git", "pull"])

def git_commit_push(message: str):
    # 변경사항이 없으면 commit이 실패하므로, add 후 diff 확인
    _run(["git", "add", "-A"])
    # 변경 없으면 그냥 종료
    r = subprocess.run(["git", "diff", "--cached", "--quiet"])
    if r.returncode == 0:
        return
    _run(["git", "commit", "-m", message])
    _run(["git", "push"])
