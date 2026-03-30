def build_qubo(df, budget=3):
    """
    Build QUBO as dict for pure Python solvers.
    """
    n = len(df)
    variables = [f'x{i}' for i in range(n)]

    # Objective: minimize -sum x_i * Z_i (maximize Z)
    objective_linear = {f'x{i}': -df.iloc[i]['Z'] for i in range(n)}

    # Budget constraint: sum x_i <= budget
    constraint_linear = {f'x{i}': 1.0 for i in range(n)}
    constraints = [{'linear': constraint_linear, 'rhs': float(budget), 'sense': 'LE'}]

    return {
        'variables': variables,
        'objective': {'linear': objective_linear},
        'constraints': constraints
    }

