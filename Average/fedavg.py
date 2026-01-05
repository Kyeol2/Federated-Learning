# Average/fedavg.py
import torch

def fedavg(state_dicts: list[dict], weights: list[float] | None = None) -> dict:
    if not state_dicts:
        raise ValueError("state_dicts is empty")

    if weights is None:
        weights = [1.0] * len(state_dicts)

    total = float(sum(weights))
    alphas = [float(w) / total for w in weights]

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
