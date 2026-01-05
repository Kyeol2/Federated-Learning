# Average/io_weights.py
import os
import json
import torch

def save_state_dict(path: str, state_dict: dict):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    cpu_sd = {k: v.detach().cpu() for k, v in state_dict.items()}
    torch.save(cpu_sd, path)

def load_state_dict(path: str) -> dict:
    return torch.load(path, map_location="cpu")

def save_json(path: str, obj: dict):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

def load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
