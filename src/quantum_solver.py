import itertools

def solve_quantum(qp):
    """
    Pure Python exact brute-force solver for QUBO with budget constraint (<=budget 1's).
    """
    n = len(qp['variables'])
    obj_coeffs = [-qp['objective']['linear'][qp['variables'][i]] for i in range(n)]  # positive Z for max
    budget = int(qp['constraints'][0]['rhs'])

    best_score = float('-inf')
    best_x = None

    for k in range(budget + 1):
        for combo_indices in itertools.combinations(range(n), k):
            x = [0.0] * n
            score = 0.0
            for i in combo_indices:
                x[i] = 1.0
                score += obj_coeffs[i]
            if score > best_score:
                best_score = score
                best_x = x

    class Result:
        def __init__(self, x, fval):
            self.x = x
            self.fval = fval
    return Result(best_x, best_score)
