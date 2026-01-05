# Average/fedavg.py
import torch

def fedavg(state_dicts: list[dict], n_samples: list[int]) -> dict:
    if not state_dicts:
        raise ValueError("state_dicts is empty")
    if len(state_dicts) != len(n_samples):
        raise ValueError("length mismatch")

    total = float(sum(n_samples))
    alphas = [ns / total for ns in n_samples]

    keys = state_dicts[0].keys()
    for sd in state_dicts[1:]:
        if sd.keys() != keys:
            raise ValueError("state_dict keys mismatch")

    out = {}
    for k in keys:
        acc = None
        for sd, a in zip(state_dicts, alphas):
            v = sd[k].float()
            acc = v.mul(a) if acc is None else acc.add(v.mul(a))
        out[k] = acc.type_as(state_dicts[0][k])
    return out
