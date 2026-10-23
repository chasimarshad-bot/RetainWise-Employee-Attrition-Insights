"""Regression evidence for headline statistics and responsible display boundaries."""
import pandas as pd
import pytest
from retainwise.data import load_data, RAW, prepare, validate_source, AGE_ORDER, TENURE_ORDER
from retainwise.analysis import rate_table, hypothesis_evidence, filter_data
from retainwise.charts import boxes, histogram


def test_fixed_population_and_hypothesis_evidence():
    df = load_data()
    assert len(df) == 1470 and df.Attrition_Flag.sum() == 237
    result = hypothesis_evidence(df)
    assert [result[key]['outcome'] for key in ['H1', 'H2', 'H3', 'H4']] == ['Supported', 'Supported', 'Mixed', 'Supported']
    assert result['H1']['difference_pp'] == pytest.approx(20.092413516275)
    assert result['H2']['table'][0]['median'] == 3
    assert result['H4']['table'][0]['median'] == 3202


def test_known_band_boundaries_and_exclusions():
    raw = pd.read_csv(RAW)
    clean = prepare(raw)
    for age, expected in [(18, 0), (29, 0), (30, 1), (39, 1), (40, 2), (49, 2), (50, 3), (60, 3)]:
        fixture = raw.iloc[[0]].copy()
        fixture['Age'] = age
        assert prepare(fixture).AgeBand.iloc[0] == AGE_ORDER[expected]
    for tenure, expected in [(0, 0), (1, 0), (2, 1), (5, 1), (6, 2), (10, 2), (11, 3)]:
        fixture = raw.iloc[[0]].copy()
        fixture[['YearsInCurrentRole', 'YearsSinceLastPromotion', 'YearsWithCurrManager']] = 0
        fixture['TotalWorkingYears'] = 40
        fixture['YearsAtCompany'] = tenure
        assert prepare(fixture).TenureBand.iloc[0] == TENURE_ORDER[expected]
    assert not {'EmployeeNumber', 'EmployeeCount', 'Over18', 'StandardHours'} & set(clean)
    assert clean.equals(load_data())


@pytest.mark.parametrize('change', ['missing', 'duplicate', 'unknown', 'age', 'tenure', 'identifier'])
def test_bad_sources_stop_instead_of_silent_cleaning(change):
    raw = pd.read_csv(RAW)
    if change == 'missing': raw.loc[0, 'MonthlyIncome'] = float('nan')
    if change == 'duplicate': raw = pd.concat([raw, raw.iloc[[0]]])
    if change == 'unknown': raw.loc[0, 'OverTime'] = 'Maybe'
    if change == 'age': raw.loc[0, 'Age'] = 90
    if change == 'tenure': raw.loc[0, 'YearsWithCurrManager'] = 100
    if change == 'identifier': raw.loc[0, 'EmployeeNumber'] = raw.loc[1, 'EmployeeNumber']
    with pytest.raises(ValueError):
        validate_source(raw)


def test_small_cells_are_withheld_and_empty_filters_stay_empty():
    df = pd.DataFrame({'team': ['Small']*9 + ['Larger']*10, 'Attrition_Flag': [1]*19})
    table = rate_table(df, 'team').set_index('team')
    assert pd.isna(table.loc['Small', 'rate_pct']) and pd.isna(table.loc['Small', 'attrited'])
    assert table.loc['Larger', 'rate_pct'] == 100
    assert filter_data(load_data(), {'Department': []}).empty
    assert rate_table(df.iloc[:0], 'team').empty


def test_distribution_charts_send_aggregates_without_individual_points():
    df = load_data()
    for trace in boxes(df, 'MonthlyIncome', 'Income').data:
        assert trace.y is None and trace.boxpoints is False
        assert len(trace.median) == 1
    fig = histogram(df, 'YearsAtCompany', 'Tenure')
    assert len(fig.data) == 2
    for trace in fig.data:
        assert len(trace.y) == 12
        assert sum(trace.y) == pytest.approx(100)
