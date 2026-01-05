# Clients/data_seq.py
import numpy as np

def make_windows(features: np.ndarray, targets: np.ndarray, seq_len: int):
    """
    features: (N, F)
    targets:  (N,) 또는 (N,1)
    return:
      X: (M, seq_len, F)
      y: (M, 1)
    """
    if targets.ndim == 1:
        targets = targets.reshape(-1, 1)

    N, F = features.shape
    M = N - seq_len
    if M <= 0:
        raise ValueError(f"Not enough rows for seq_len={seq_len}. N={N}")

    X = np.zeros((M, seq_len, F), dtype=np.float32)
    y = np.zeros((M, 1), dtype=np.float32)

    for i in range(M):
        X[i] = features[i:i+seq_len]
        y[i] = targets[i+seq_len]   # 다음 시점 예측
    return X, y
