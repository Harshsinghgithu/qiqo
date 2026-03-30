import matplotlib.pyplot as plt
import os

def save_results(df, quantum_res, classical_res):
    """Save optimization results to CSV.

    Args:
        df (pd.DataFrame): DataFrame with scores.
        quantum_res, classical_res: Solver results with .x
    """
    df['Selected_Q'] = quantum_res.x
    df['Selected_C'] = classical_res.x
    os.makedirs('results', exist_ok=True)
    df.to_csv('results/output.csv', index=False)

def plot(df):
    """Generate plots for scores and allocations.

    Args:
        df (pd.DataFrame): Results DataFrame.
    """
    os.makedirs('results/plots', exist_ok=True)

    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    axs[0,0].bar(df['Country'], df['Innovation'])
    axs[0,0].set_title('Innovation Score')
    axs[0,0].tick_params(axis='x', rotation=45)

    axs[0,1].bar(df['Country'], df['Return'])
    axs[0,1].set_title('Return Score')
    axs[0,1].tick_params(axis='x', rotation=45)

    axs[1,0].bar(df['Country'], df['Z'])
    axs[1,0].set_title('Objective Z')
    axs[1,0].tick_params(axis='x', rotation=45)

    x = range(len(df))
    width = 0.35
    axs[1,1].bar([i - width/2 for i in x], df['Selected_Q'], width, label='Quantum')
    axs[1,1].bar([i + width/2 for i in x], df['Selected_C'], width, label='Classical')
    axs[1,1].set_title('Allocation Comparison')
    axs[1,1].set_xticks(x)
    axs[1,1].set_xticklabels(df['Country'], rotation=45)
    axs[1,1].legend()

    plt.tight_layout()
    plt.savefig('results/plots/comparison.png')
    plt.close()
