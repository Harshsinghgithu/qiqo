import itertools

def brute_force(df):
    """Classical brute force optimizer for binary investment allocation.

    Args:
        df (pd.DataFrame): DataFrame with 'Z' objective scores per country.

    Returns:
        Result object with .x (binary allocation vector) and .fval (max score).
    """
    n = len(df)
    best_score = -float('inf')
    best_combo = None

    for combo in itertools.product([0,1], repeat=n):
        score = sum(combo[i] * df.iloc[i]['Z'] for i in range(n))
        if score > best_score:
            best_score = score
            best_combo = combo

    class Result:
        def __init__(self, x, fval):
            self.x = x
            self.fval = fval
    return Result(list(best_combo), best_score)
