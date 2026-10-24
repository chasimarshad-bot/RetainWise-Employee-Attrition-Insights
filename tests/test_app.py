"""Streamlit execution tests exercise rendering and filter state transitions."""
from pathlib import Path
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]


def test_overview_clear_and_reset_filters():
    app = AppTest.from_file(str(ROOT / 'app.py'), default_timeout=30).run()
    assert not app.exception
    assert [metric.value for metric in app.metric][:4] == ['1,470', '237', '16.1%', '1,233']
    app.multiselect(key='filter_Department').set_value([]).run()
    assert not app.exception
    assert any('No records match' in item.value for item in app.info)
    app.button[0].click().run()
    assert not app.exception
    assert app.metric[0].value == '1,470'


def test_all_page_functions_render():
    # Direct callable harness complements browser tests of the actual navigation.
    for name in ['patterns', 'hypotheses', 'governance', 'methodology']:
        app = AppTest.from_string(f'from retainwise.ui import {name}\n{name}()', default_timeout=30).run()
        assert not app.exception, name


def test_one_outcome_and_small_cohort_do_not_crash():
    app = AppTest.from_file(str(ROOT / 'app.py'), default_timeout=30).run()
    app.multiselect(key='filter_Department').set_value(['Human Resources'])
    app.multiselect(key='filter_JobRole').set_value(['Manager'])
    app.multiselect(key='filter_OverTime').set_value(['Yes']).run()
    assert not app.exception
    assert any('fewer than 10' in warning.value for warning in app.warning)


def test_explorer_and_demographic_selections_render():
    app = AppTest.from_string('from retainwise.ui import patterns\npatterns()', default_timeout=30).run()
    for factor in ['OverTime', 'JobSatisfaction', 'EnvironmentSatisfaction', 'JobInvolvement', 'WorkLifeBalance', 'BusinessTravel', 'JobRole']:
        app.selectbox[0].set_value(factor).run()
        assert not app.exception, factor
    for factor in ['YearsAtCompany', 'YearsInCurrentRole', 'TotalWorkingYears', 'YearsWithCurrManager', 'MonthlyIncome']:
        app.selectbox[1].set_value(factor).run()
        assert not app.exception, factor
    app = AppTest.from_string('from retainwise.ui import governance\ngovernance()', default_timeout=30).run()
    for field in ['AgeBand', 'Gender', 'MaritalStatus']:
        app.selectbox[0].set_value(field).run()
        assert not app.exception, field
