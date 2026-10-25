"""Validate the source and produce deterministic, versioned analytical data."""
from pathlib import Path
import hashlib
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data/raw/WA_Fn-UseC_-HR-Employee-Attrition.csv'
PROCESSED = ROOT / 'data/processed/v1'
DATA = PROCESSED / 'employee_attrition_v1.csv'
SOURCE_SHA256 = 'a5c31e38bd7fafc9bc333884eb181b06b41b8e5e488e8f7ccb27199fb3be7659'
AGE_ORDER = ['18–29', '30–39', '40–49', '50–60']
TENURE_ORDER = ['0–1 years', '2–5 years', '6–10 years', '11+ years']
ORDINALS = {
    'EnvironmentSatisfaction': {1: 'Low', 2: 'Medium', 3: 'High', 4: 'Very high'},
    'JobSatisfaction': {1: 'Low', 2: 'Medium', 3: 'High', 4: 'Very high'},
    'JobInvolvement': {1: 'Low', 2: 'Medium', 3: 'High', 4: 'Very high'},
    'RelationshipSatisfaction': {1: 'Low', 2: 'Medium', 3: 'High', 4: 'Very high'},
    'WorkLifeBalance': {1: 'Bad', 2: 'Good', 3: 'Better', 4: 'Best'},
    'Education': {1: 'Below college', 2: 'College', 3: 'Bachelor', 4: 'Master', 5: 'Doctor'},
    'PerformanceRating': {1: 'Low', 2: 'Good', 3: 'Excellent', 4: 'Outstanding'},
}
CATEGORIES = {
    'Attrition': {'Yes', 'No'}, 'OverTime': {'Yes', 'No'},
    'BusinessTravel': {'Non-Travel', 'Travel_Rarely', 'Travel_Frequently'},
    'Department': {'Sales', 'Research & Development', 'Human Resources'},
    'Gender': {'Female', 'Male'}, 'MaritalStatus': {'Single', 'Married', 'Divorced'},
    'JobRole': {'Sales Executive', 'Research Scientist', 'Laboratory Technician',
                'Manufacturing Director', 'Healthcare Representative', 'Manager',
                'Sales Representative', 'Research Director', 'Human Resources'},
    'EducationField': {'Life Sciences', 'Medical', 'Marketing', 'Technical Degree', 'Other', 'Human Resources'},
    'Over18': {'Y'},
}
SOURCE_COLUMNS = ['Age', 'Attrition', 'BusinessTravel', 'DailyRate', 'Department',
    'DistanceFromHome', 'Education', 'EducationField', 'EmployeeCount', 'EmployeeNumber',
    'EnvironmentSatisfaction', 'Gender', 'HourlyRate', 'JobInvolvement', 'JobLevel',
    'JobRole', 'JobSatisfaction', 'MaritalStatus', 'MonthlyIncome', 'MonthlyRate',
    'NumCompaniesWorked', 'Over18', 'OverTime', 'PercentSalaryHike', 'PerformanceRating',
    'RelationshipSatisfaction', 'StandardHours', 'StockOptionLevel', 'TotalWorkingYears',
    'TrainingTimesLastYear', 'WorkLifeBalance', 'YearsAtCompany', 'YearsInCurrentRole',
    'YearsSinceLastPromotion', 'YearsWithCurrManager']


def validate_source(df):
    """Fail visibly on changed schema or invalid values; never silently repair rows."""
    errors = []
    if list(df.columns) != SOURCE_COLUMNS:
        raise ValueError('Source schema changed; review before creating a new version.')
    if df.empty:
        errors.append('No source records')
    if df.isna().any().any():
        errors.append('Missing values')
    if df.duplicated().any():
        errors.append('Duplicate rows')
    if not df.EmployeeNumber.is_unique:
        errors.append('Non-unique employee identifier')
    for col, allowed in CATEGORIES.items():
        if not set(df[col]).issubset(allowed):
            errors.append(f'Unknown category: {col}')
    for col in set(SOURCE_COLUMNS) - set(CATEGORIES):
        if not pd.api.types.is_numeric_dtype(df[col]) or df[col].lt(0).any():
            errors.append(f'Invalid numeric values: {col}')
    for col, mapping in ORDINALS.items():
        if not df[col].isin(mapping).all():
            errors.append(f'Invalid ordinal values: {col}')
    if not df.Age.between(18, 60).all():
        errors.append('Age outside documented v1 bands')
    for col in ['YearsInCurrentRole', 'YearsSinceLastPromotion', 'YearsWithCurrManager']:
        if df[col].gt(df.YearsAtCompany).any():
            errors.append(f'{col} exceeds company tenure')
    if df.YearsAtCompany.gt(df.TotalWorkingYears).any():
        errors.append('Company tenure exceeds working years')
    for col, value in {'EmployeeCount': 1, 'StandardHours': 80, 'Over18': 'Y'}.items():
        if not df[col].eq(value).all():
            errors.append(f'Expected constant changed: {col}')
    if errors:
        raise ValueError('; '.join(errors))
    return {'rows': len(df), 'columns': len(df.columns), 'missing_values': int(df.isna().sum().sum()),
            'duplicate_rows': int(df.duplicated().sum()), 'identifier_unique': bool(df.EmployeeNumber.is_unique),
            'constant_columns': [c for c in df if df[c].nunique() == 1],
            'target_counts': df.Attrition.value_counts().to_dict()}


def prepare(df):
    """Preserve source labels; exclude identifiers/constants; add explicit bands."""
    validate_source(df)
    clean = df.drop(columns=['EmployeeNumber', 'EmployeeCount', 'Over18', 'StandardHours']).copy()
    clean['Attrition_Flag'] = clean.Attrition.map({'No': 0, 'Yes': 1})
    clean['AgeBand'] = pd.cut(clean.Age, bins=[17, 29, 39, 49, 60], labels=AGE_ORDER).astype(str)
    clean['TenureBand'] = pd.cut(clean.YearsAtCompany, bins=[-1, 1, 5, 10, float('inf')], labels=TENURE_ORDER).astype(str)
    clean['Status'] = clean.Attrition.map({'No': 'Retained', 'Yes': 'Attrited'})
    return clean


DESCRIPTIONS = {
    'Attrition': 'Source outcome: Yes / No; no exit date is supplied.',
    'Attrition_Flag': 'Derived: Yes=1, No=0; group mean is observed attrition proportion.',
    'Status': 'Derived display label: Yes=Attrited, No=Retained.',
    'Age': 'Age in years; used only for aggregate audit.',
    'AgeBand': 'Derived integer ages: 18–29, 30–39, 40–49, 50–60.',
    'TenureBand': 'Derived company tenure: 0–1, 2–5, 6–10, 11+ years.',
    'MonthlyIncome': 'Monthly income in source units; currency not documented.',
    'Gender': 'Source-labelled Female/Male; incomplete representation, not a legal definition of sex.',
    'MaritalStatus': 'Source marital-status category; does not establish civil-partnership status.',
    'OverTime': 'Source overtime category: Yes / No; hours are unavailable.',
    'BusinessTravel': 'Source travel-frequency category; no measured journey counts.',
    'Department': 'Source organisational department.', 'JobRole': 'Source job-role category.',
    'EducationField': 'Source education field category.',
    'DailyRate': 'Source daily rate; units and interpretation not documented.',
    'HourlyRate': 'Source hourly rate; currency not documented.',
    'MonthlyRate': 'Source monthly rate; interpretation and currency not documented.',
    'DistanceFromHome': 'Source distance from home; distance unit not documented.',
    'JobLevel': 'Source job level, integer category.',
    'StockOptionLevel': 'Source stock-option level, integer category.',
    'NumCompaniesWorked': 'Number of companies worked at in source.',
    'PercentSalaryHike': 'Source salary increase percentage.',
    'TrainingTimesLastYear': 'Source training instances in last year; no dated history.',
    'TotalWorkingYears': 'Total working years in source.',
    'YearsAtCompany': 'Years at company in source.',
    'YearsInCurrentRole': 'Years in current role in source.',
    'YearsSinceLastPromotion': 'Years since last promotion in source.',
    'YearsWithCurrManager': 'Years with current manager in source.',
}


def dictionary(df):
    records = []
    for col in df:
        description = DESCRIPTIONS.get(col)
        if col in ORDINALS:
            description = 'Source ordinal scale: ' + '; '.join(f'{k}={v}' for k, v in ORDINALS[col].items())
        records.append({'field': col, 'dtype': str(df[col].dtype), 'description': description,
                        'unique_values': df[col].nunique(), 'missing': int(df[col].isna().sum())})
    return pd.DataFrame(records)


def write_version():
    if hashlib.sha256(RAW.read_bytes()).hexdigest() != SOURCE_SHA256:
        raise ValueError('Source differs from the reviewed v1 snapshot. Review the change and create a new version before processing.')
    raw = pd.read_csv(RAW)
    report = validate_source(raw)
    clean = prepare(raw)
    PROCESSED.mkdir(parents=True, exist_ok=True)
    clean.to_csv(DATA, index=False, lineterminator='\n')
    dictionary(clean).to_csv(PROCESSED / 'data_dictionary_v1.csv', index=False, lineterminator='\n')
    metadata = {'version': 'v1', 'source': 'IBM HR Analytics Employee Attrition & Performance',
        'source_url': 'https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset',
        'source_sha256': hashlib.sha256(RAW.read_bytes()).hexdigest(),
        'processed_sha256': hashlib.sha256(DATA.read_bytes()).hexdigest(),
        'validation': report, 'rows': len(clean), 'columns': len(clean.columns),
        'excluded': ['EmployeeNumber', 'EmployeeCount', 'Over18', 'StandardHours'],
        'transformations': ['Attrition_Flag: Yes=1, No=0', 'Status: Yes=Attrited, No=Retained',
            'AgeBand: [18,29], [30,39], [40,49], [50,60]', 'TenureBand: [0,1], [2,5], [6,10], [11,infinity]'],
        'licence': 'Database: Open Database, Contents: Database Contents (Kaggle metadata)',
        'limitations': ['Fictional population', 'No dated exits', 'No causal identification', 'Income currency undocumented']}
    (PROCESSED / 'metadata_v1.json').write_text(json.dumps(metadata, indent=2), encoding='utf-8')
    return clean, metadata


def load_data():
    """Read the reviewed v1 output only; the app never cleans raw records."""
    return pd.read_csv(DATA)
