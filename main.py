from src.data_loader import load_data
from src.preprocessing import filter_years, normalize
from src.model import compute_scores, objective, india_sector_recommendation
from src.qubo_formulation import build_qubo
from src.quantum_solver import solve_quantum
from src.classical_solver import brute_force
from src.evaluation import save_results, plot

def main(path='data/dataset.xlsx', budget=3, alpha=0.5, beta=0.5):
    """Main pipeline for QIOM.

    Args:
        path (str): Path to dataset Excel.
        budget (int): Max investments.
        alpha, beta (float): Weights for Z = alpha*I + beta*R
    """
    df = load_data(path)

    df = filter_years(df)
    df = normalize(df)
    df = compute_scores(df)
    df = objective(df, alpha=alpha, beta=beta)

    print("Processed Data:\n", df.head())

    qp = build_qubo(df, budget=budget)

    print("\nRunning Quantum Solver (QAOA)...")
    quantum_res = solve_quantum(qp)

    print("\nRunning Classical Solver (Brute Force)...")
    classical_res = brute_force(df)

    save_results(df, quantum_res, classical_res)
    plot(df)

    print("\n=== Results Comparison ===")
    print("Quantum allocation:", quantum_res.x, "score:", quantum_res.fval)
    print("Classical allocation:", classical_res.x, "score:", classical_res.fval)

    # India sector recommendation
    recs = india_sector_recommendation(df)
    print("\n" + recs['summary'])
    for detail in recs['details']:
        print(detail)

if __name__ == '__main__':
    main()

