def compute_scores(df):
    df['Innovation'] = 0.4 * df['RD'] + 0.3 * df['Startups'] + 0.3 * df['VC']
    df['Return'] = (df['Patents'] + df['Innovation']) / (df['RD'] + df['VC'] + 1e-6)
    return df

def objective(df, alpha=0.5, beta=0.5):
    df['Z'] = alpha * df['Innovation'] + beta * df['Return']
    return df

def india_sector_recommendation(df, alpha=0.5, beta=0.5):
    """
    Prioritize positive India gaps (strengths to amplify) for allocation %.
    Varies with α Innovation vs β Return weights.
    """
    df_computed = compute_scores(df.copy())
    df_computed = objective(df_computed, alpha=alpha, beta=beta)
    
    sectors = ['RD', 'VC', 'Startups', 'Patents']
    
    # Global vs India
    global_inno = df_computed['Innovation'].mean()
    india_inno = df_computed[df_computed['Country'] == 'India']['Innovation'].mean()
    
    global_ret = df_computed['Return'].mean()
    india_ret = df_computed[df_computed['Country'] == 'India']['Return'].mean()
    
    inno_gap = india_inno - global_inno
    ret_gap = india_ret - global_ret
    
    gaps = {
        'RD': 0.4 * inno_gap + 0.3 * ret_gap,
        'VC': 0.3 * inno_gap + 0.4 * ret_gap,
        'Startups': 0.3 * inno_gap + 0.2 * ret_gap,
        'Patents': 0.2 * inno_gap + 0.5 * ret_gap
    }
    gaps_list = [gaps[s] for s in sectors]
    
    max_gap = max(gaps_list)
    if max_gap <= 0:
        weights = [25.0] * 4
    else:
        weights = [gap / max_gap * 100 for gap in gaps_list]
    
    recs = [f"{sector}: {w:.1f}% (gap: {gaps[sector]:.3f}, α={alpha:.1f} β={beta:.1f})" for sector, w in zip(sectors, weights)]
    
    return {
        'summary': f"🇮🇳 India Recs (α={alpha:.1f} Innovation, β={beta:.1f} Return | amplify positive gaps)",
        'details': recs,
        'weights': weights,
        'sectors': sectors,
        'gaps': gaps_list
    }

