"""Author the three reproducible notebooks; execution is a separate QA step."""
from pathlib import Path
import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP = '''from pathlib import Path
import sys
ROOT = Path.cwd()
if not (ROOT / 'retainwise').exists():
    ROOT = ROOT.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
import pandas as pd
from IPython.display import display
from retainwise.data import RAW, PROCESSED, DATA, validate_source, prepare, dictionary, write_version, load_data
from retainwise.analysis import rate_table, distribution, hypothesis_evidence, HYPOTHESES
pd.set_option('display.max_columns', 40)
'''


def write(name, cells):
    notebook = nbf.v4.new_notebook()
    notebook.metadata = {'kernelspec': {'display_name': 'Python 3 (RetainWise)', 'language': 'python', 'name': 'python3'},
                         'language_info': {'name': 'python', 'version': '3.12.8'}}
    notebook.cells = [nbf.v4.new_markdown_cell(text) if kind == 'md' else nbf.v4.new_code_cell(text) for kind, text in cells]
    nbf.write(notebook, ROOT / 'jupyter_notebooks' / name)


if __name__ == '__main__':
    write('01_data_collection.ipynb', [
        ('md', '# 01 · Data collection and understanding\n\nQuestion: what does the fictional source contain, and is it suitable for aggregate descriptive analysis? No cleaning happens in this notebook.\n\nSource: [IBM HR Analytics Employee Attrition & Performance](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset), published by Pavan Subhash. Kaggle lists Database: Open Database, Contents: Database Contents. Full attribution and licence links: `data/SOURCE.md`. The dataset does not represent IBM’s actual workforce.'),
        ('code', BOOTSTRAP),
        ('code', "raw = pd.read_csv(RAW)\nreport = validate_source(raw)\ndisplay(pd.Series(report, name='Validation evidence'))\nprint('Shape:', raw.shape)"),
        ('md', '## Schema, values and categories\n\nInspect every field without exposing employee-level rows in the dashboard. This notebook is a development artefact using fictional data.'),
        ('code', "profile = pd.DataFrame({'dtype': raw.dtypes.astype(str), 'missing': raw.isna().sum(), 'unique': raw.nunique()})\ndisplay(profile)\nfor col in raw:\n    if raw[col].nunique() <= 10:\n        print(col, sorted(raw[col].unique().tolist()))\nprint('Duplicates:', raw.duplicated().sum())\nprint('Identifier unique:', raw.EmployeeNumber.is_unique)\nprint('Constant columns:', [c for c in raw if raw[c].nunique() == 1])"),
        ('code', "display(raw.Attrition.value_counts().rename_axis('Attrition').to_frame('n').assign(share_pct=lambda x: 100*x.n/len(raw)))\ndisplay(dictionary(raw.drop(columns=['EmployeeNumber', 'EmployeeCount', 'Over18', 'StandardHours'])))"),
        ('md', '## Suitability and limits\n\nThe source passes the explicit v1 validation checks. The target is imbalanced, there is no dated observation window and currency is not documented. Department, role and other variables may confound crude comparisons. The binary Gender field is incomplete representation. Analysis can describe associations within this fictional population; it cannot explain departures, estimate policy effects or generalise to an employer. The identifier and constants will be removed only in notebook 02, after this evidence check.')])
    write('02_data_cleaning.ipynb', [
        ('md', '# 02 · Data preparation and versioning\n\nPreserve source evidence and make each transformation explicit. No imputation, target resampling or outlier removal is justified by the initial checks.'),
        ('code', BOOTSTRAP),
        ('code', "raw = pd.read_csv(RAW)\ndisplay(pd.Series(validate_source(raw)))\nassert raw.EmployeeNumber.is_unique\nassert raw[['EmployeeCount', 'Over18', 'StandardHours']].nunique().eq(1).all()"),
        ('md', '## Transformation decisions\n\nRemove EmployeeNumber (unnecessary identifier) and the verified constants EmployeeCount, Over18 and StandardHours. Retain Attrition; derive Attrition_Flag and readable Status. AgeBand uses closed integer intervals 18–29, 30–39, 40–49, 50–60. TenureBand uses 0–1, 2–5, 6–10, 11+ years. The implementation rejects ages outside its reviewed bands. Removing identifiers does not establish anonymisation.'),
        ('code', "clean = prepare(raw)\nPROCESSED.mkdir(parents=True, exist_ok=True)\nclean.to_csv(PROCESSED / 'employee_attrition_v1.csv', index=False, lineterminator='\\n')\ndictionary(clean).to_csv(PROCESSED / 'data_dictionary_v1.csv', index=False, lineterminator='\\n')\nclean, metadata = write_version()\nassert len(clean) == len(raw)\nassert clean.Attrition_Flag.eq(raw.Attrition.map({'Yes': 1, 'No': 0})).all()\nassert not clean[['AgeBand', 'TenureBand']].isna().any().any()\ndisplay(pd.Series(metadata))\ndisplay(dictionary(clean))"),
        ('md', '## Version contract\n\nThe dedicated `data/processed/v1` folder contains the dataset, dictionary and metadata with SHA-256 hashes. Repeated execution is deterministic. A different source population or revised transformation requires a reviewed v2, preserving v1. Original columns and outcome balance remain unchanged except for the four documented exclusions.')])
    write('03_analysis_and_hypotheses.ipynb', [
        ('md', '# 03 · Analysis and hypotheses\n\nThe PRD defines H1–H4 before interpretation. The rules below operationalise those statements without changing their direction. Outcomes describe observed support, not significance or causal effects. This notebook always uses the full v1 population.\n\nH1: Yes overtime rate > No rate. H2: both attrited mean and median tenure lower (Mixed if one is lower). H3: non-increasing satisfaction rates from 1 to 4 (Mixed if endpoints agree with the statement but the sequence is not monotonic). H4: lower attrited income median. Otherwise Not Supported.'),
        ('code', BOOTSTRAP + "\nfrom retainwise.data import AGE_ORDER, TENURE_ORDER\nfrom retainwise import charts\nimport json\ndf = load_data()\nevidence = hypothesis_evidence(df)\nprint(f'Employees={len(df)}, attrited={df.Attrition_Flag.sum()}, retained={(df.Attrition_Flag == 0).sum()}')\nprint(f'Observed attrition={100*df.Attrition_Flag.mean():.8f}%')"),
        ('md', '## BR1–BR2 · Organisational and workplace comparisons\n\nRates use each category’s own denominator. Small groups are flagged; n<10 cells are withheld in the dashboard. Source scales are ordered, but equal distances between ordinal values are not assumed.'),
        ('code', "for field in ['Department', 'JobRole', 'OverTime', 'BusinessTravel', 'JobSatisfaction', 'EnvironmentSatisfaction', 'JobInvolvement', 'WorkLifeBalance']:\n    display(rate_table(df, field))\ncharts.rates(rate_table(df, 'OverTime', ['No', 'Yes']), 'OverTime', 'Overtime and observed attrition').show(renderer='plotly_mimetype')"),
        ('md', '## BR3 · Tenure and compensation\n\nCompare both location and spread. Income is in source units. Quartiles use linear interpolation.'),
        ('code', "for field in ['YearsAtCompany', 'YearsInCurrentRole', 'TotalWorkingYears', 'YearsWithCurrManager', 'MonthlyIncome']:\n    print(field)\n    display(distribution(df, field))\ncharts.boxes(df, 'YearsAtCompany', 'Company tenure (years)').show(renderer='plotly_mimetype')\ncharts.boxes(df, 'MonthlyIncome', 'Monthly income (source units)').show(renderer='plotly_mimetype')\ncharts.histogram(df, 'YearsAtCompany', 'Company tenure (years)').show(renderer='plotly_mimetype')"),
        ('md', '## BR4 · Demographic audit\n\nThese comparisons are descriptive audit prompts. They do not establish discrimination or justify targeting. Gender is the source label, not a complete representation or legal definition.'),
        ('code', "for field, order in [('AgeBand', AGE_ORDER), ('Gender', None), ('MaritalStatus', None)]:\n    display(rate_table(df, field, order))"),
        ('md', '## H1–H4 · Full-population evidence\n\nKeep the statement, rule and result together. Exact values below support the dashboard and README.'),
        ('code', "for key, statement in HYPOTHESES.items():\n    print(key, statement)\n    print('Outcome:', evidence[key]['outcome'])\n    if key == 'H1':\n        print('Percentage-point difference:', evidence[key]['difference_pp'])\n    display(pd.DataFrame(evidence[key]['table']))\n(PROCESSED / 'hypothesis_evidence_v1.json').write_text(json.dumps(evidence, indent=2), encoding='utf-8')"),
        ('md', '## Interpretation and next questions\n\nH1 is Supported: overtime categories differ by about 20.09 percentage points. H2 is Supported: attrited tenure has a median of 3 years versus 6, with a lower mean too. H3 is Mixed: the rates are about 22.84%, 16.43%, 16.52%, 11.33%, so a monotonic claim fails. H4 is Supported: income medians are 3,202 and 5,204 source units.\n\nThese are crude associations. Role, level, age and tenure mix may contribute to differences, but this project does not estimate adjusted effects. Prioritise voluntary research into workload, onboarding and employee experience; do not infer individual departure risk, financial savings or intervention effectiveness. The smaller attrited population, absent dates and fictional data limit all conclusions.')])
    print('Authored three notebooks; run scripts/run_notebooks.py to execute them.')
