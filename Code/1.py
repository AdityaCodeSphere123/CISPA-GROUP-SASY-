def find_n_and_queue_size(V, d=10, p=0.25, epsilon=1e-80, max_k=1000):
    """
    Determines the smallest n such that after k compactions,
    all vertices are seen (within epsilon * V).
    
    Returns: n, final queue size
    """
    for n in range(1, 5000):
        S = 0  # initially seen vertices
        alpha = d * p
        seen = []

        for k in range(max_k):
            q_k = (V - S) / V
            new_reals = n * alpha * q_k
            S += new_reals
            seen.append(S)
            if S >= (1 - epsilon) * V:
                break
        else:
            continue  # didn't converge for this n

        # Compute total queue growth:
        Q_max = math.ceil(V)  # max real entries at any time
        Q_total = Q_max + n * d  # safe upper bound (conservative)

        return {
            "n": n,
            "queue_size": Q_total,
            "num_compactions": k + 1,
            "seen_vertices": int(S),
            "converged": True
        }

    return {"converged": False}
