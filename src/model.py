def compute_scores(df):
    df['Innovation'] = 0.4 * df['RD'] + 0.3 * df['Startups'] + 0.3 * df['VC']
    df['Return'] = (df['Patents'] + df['Innovation']) / (df['RD'] + df['VC'] + 1e-6)
    return df


def objective(df, alpha=0.5, beta=0.5):
    df['Z'] = alpha * df['Innovation'] + beta * df['Return']
    return df


def india_sector_recommendation(df):
    """
    Recommend fund allocation for India sectors vs other countries.
    Sectors: RD, VC, Startups, Patents. Fixed: Largest gap priority.
    """
    sectors = ['RD', 'VC', 'Startups', 'Patents']
    
    # Average metrics
    global_avg = df[sectors].mean()
    india_avg = df[df['Country'] == 'India'][sectors].mean()
    
    # Relative gaps: negative = India weak → HIGHER priority (invert for weight)
    gaps = (india_avg - global_avg).to_dict()
    gaps_list = [gaps[s] for s in sectors]
    
    # Weight = -gap normalized (more negative gap = higher weight)
    max_weight = max(-g for g in gaps_list)
    weights = [max(0, -g) / max_weight for g in gaps_list]
    total_weight = sum(weights)
    weights = [w / total_weight * 100 if total_weight > 0 else 25 for w in weights]
    
    recs = []
    for i, sector in enumerate(sectors):
        priority = weights[i]
        recs.append(f"{sector}: {priority:.1f}% (gap: {gaps[sector]:.3f})")
    
    return {
        'summary': f"India Sector Allocation Recs (total 100%, prioritize negative gaps):",
        'details': recs,
        'weights': weights,
        'sectors': sectors,
        'gaps': gaps_list
    }

