def filter_years(df):
    return df[df['Year'].isin([2023, 2024, 2025])]


def normalize(df):
    # Rename columns based on your dataset
    df = df.rename(columns={
        'R&D ($B)': 'RD',
        'VC ($B)': 'VC'
    })

    cols = ['RD', 'VC', 'Startups', 'Patents']

    for col in cols:
        df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min() + 1e-9)

    return df