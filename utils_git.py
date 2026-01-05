# utils_git.py
import subprocess

def _run(cmd: list[str]):
    subprocess.run(cmd, check=True)

def git_pull():
    _run(["git", "pull"])

def git_commit_push(message: str):
    _run(["git", "add", "-A"])
    r = subprocess.run(["git", "diff", "--cached", "--quiet"])
    if r.returncode == 0:
        return
    _run(["git", "commit", "-m", message])
    _run(["git", "push"])
