def compute_scores(df):
    df['Innovation'] = 0.4 * df['RD'] + 0.3 * df['Startups'] + 0.3 * df['VC']
    df['Return'] = (df['Patents'] + df['Innovation']) / (df['RD'] + df['VC'] + 1e-6)
    return df


def objective(df, alpha=0.5, beta=0.5):
    df['Z'] = alpha * df['Innovation'] + beta * df['Return']
    return df


def india_sector_recommendation(df, alpha=0.5, beta=0.5):
    """
    Recommend fund allocation for India sectors vs other countries.
    Weights now respond to alpha/beta via Innovation/Return gaps.
    """
    from src.model import compute_scores, objective  # self-import for recompute
    
    # Recompute weighted scores
    df_computed = compute_scores(df.copy())
    df_computed = objective(df_computed, alpha=alpha, beta=beta)
    
    sectors = ['RD', 'VC', 'Startups', 'Patents']
    
    # Global vs India Innovation/Return averages
    global_inno = df_computed['Innovation'].mean()
    india_inno = df_computed[df_computed['Country'] == 'India']['Innovation'].mean()
    
    global_ret = df_computed['Return'].mean()
    india_ret = df_computed[df_computed['Country'] == 'India']['Return'].mean()
    
    # Weighted Innovation gap (alpha affects relative priority)
    inno_gap = india_inno - global_inno
    ret_gap = india_ret - global_ret
    
    gaps = {
        'RD': 0.4 * inno_gap + 0.5 * ret_gap,      # RD heavy Innovation
        'VC': 0.3 * inno_gap + 0.5 * ret_gap,      # VC balanced
        'Startups': 0.3 * inno_gap + 0.3 * ret_gap,  # Startups Innovation
        'Patents': 0.2 * inno_gap + 1.0 * ret_gap    # Patents Return heavy
    }
    gaps_list = list(gaps.values())
    
    # Weight = -gap normalized (negative gap = higher priority)
    max_weight = max(-g for g in gaps_list)
    weights = [max(0, -gaps[s]) / max_weight * 100 for s in ['RD','VC','Startups','Patents']]
    
    recs = []
    for sector in ['RD','VC','Startups','Patents']:
        priority = weights[['RD','VC','Startups','Patents'].index(sector)]
        recs.append(f"{sector}: {priority:.1f}% (weighted gap: {gaps[sector]:.3f}, α={alpha}, β={beta})")
    
    return {
        'summary': f"🇮🇳 India Sector Recs (α={alpha:.1f} Innovation, β={beta:.1f} Return | total 100%)",
        'details': recs,
        'weights': weights,
        'sectors': ['RD','VC','Startups','Patents'],
        'gaps': gaps_list,
        'alpha': alpha,
        'beta': beta
    }

