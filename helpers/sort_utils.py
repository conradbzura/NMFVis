import numpy as np

def bar_sort_order(mat: np.ndarray) -> np.ndarray:
    """Return indices that order samples by winning component, then activity."""
    winners = np.argmax(mat, axis=1)
    order = []
    for comp in range(mat.shape[1]):
        idx = np.argsort(-mat[:, comp])
        order.extend(idx[winners[idx] == comp])
    return np.asarray(order, dtype=int)
