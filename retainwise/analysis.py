"""Deterministic descriptive statistics; no predictive or causal modelling."""
import pandas as pd

MIN_GROUP = 10


def rate_table(df, field, order=None, suppress=True):
    """Rates with denominators; cells n<10 withheld, including complementary outcome."""
    table = df.groupby(field, observed=True)['Attrition_Flag'].agg(n='size', attrited='sum').reset_index()
    table['rate_pct'] = 100 * table.attrited / table.n
    table['caution'] = table.n.map(lambda n: 'Withheld: n < 10' if n < MIN_GROUP else ('Small group: n < 30' if n < 30 else 'Descriptive only'))
    if order is not None:
        table[field] = pd.Categorical(table[field], categories=order, ordered=True)
        table = table.sort_values(field).reset_index(drop=True)
    if suppress:
        table.loc[table.n < MIN_GROUP, ['attrited', 'rate_pct']] = float('nan')
    return table


def distribution(df, field):
    """Quartiles use pandas' linear interpolation, reported for both outcomes."""
    return df.groupby('Status', observed=True)[field].agg(
        n='size', mean='mean', median='median', q1=lambda x: x.quantile(.25), q3=lambda x: x.quantile(.75)
    ).reset_index()


HYPOTHESES = {
    'H1': 'Employees recorded as working overtime have a higher observed attrition rate than employees not recorded as working overtime.',
    'H2': 'Attrited employees have shorter observed company tenure than retained employees.',
    'H3': 'Lower job-satisfaction categories have higher observed attrition rates than higher job-satisfaction categories.',
    'H4': 'Attrited employees have a lower observed median MonthlyIncome than retained employees.',
}


def hypothesis_evidence(df):
    """Fixed rules, defined before interpretation; full-population descriptive support."""
    overtime = rate_table(df, 'OverTime', ['No', 'Yes'], suppress=False)
    ot = overtime.set_index('OverTime').rate_pct
    tenure = distribution(df, 'YearsAtCompany')
    tn = tenure.set_index('Status')
    satisfaction = rate_table(df, 'JobSatisfaction', [1, 2, 3, 4], suppress=False)
    rates = satisfaction.rate_pct
    income = distribution(df, 'MonthlyIncome')
    inc = income.set_index('Status')
    shorter_mean = tn.loc['Attrited', 'mean'] < tn.loc['Retained', 'mean']
    shorter_median = tn.loc['Attrited', 'median'] < tn.loc['Retained', 'median']
    h3 = 'Supported' if rates.is_monotonic_decreasing else ('Mixed' if rates.iloc[0] > rates.iloc[-1] else 'Not Supported')
    return {
        'H1': {'outcome': 'Supported' if ot['Yes'] > ot['No'] else 'Not Supported',
               'difference_pp': float(ot['Yes'] - ot['No']), 'table': overtime.to_dict('records')},
        'H2': {'outcome': 'Supported' if shorter_mean and shorter_median else ('Mixed' if shorter_mean or shorter_median else 'Not Supported'),
               'table': tenure.to_dict('records')},
        'H3': {'outcome': h3, 'table': satisfaction.to_dict('records')},
        'H4': {'outcome': 'Supported' if inc.loc['Attrited', 'median'] < inc.loc['Retained', 'median'] else 'Not Supported',
               'table': income.to_dict('records')},
    }


def filter_data(df, selections):
    """An empty selection means no records; explicit reset restores the population."""
    mask = pd.Series(True, index=df.index)
    for field, values in selections.items():
        mask &= df[field].isin(values)
    return df.loc[mask].copy()
