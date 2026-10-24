# RetainWise

**Responsible Employee Attrition Insights** · Unit 3 capstone · Ch Asim Arshad

RetainWise helps HR leaders explore workforce attrition patterns while keeping the limits of the evidence visible. Executive summaries, exact calculations and governance guidance sit in separate, connected views.

**Status:** working local Streamlit app; live deployment is outstanding. [Dashboard preview](docs/screenshots/overview-desktop.png) · [Deployment steps](docs/deployment.md) · [Unit 3 project board](https://github.com/users/chasimarshad-bot/projects/4) · [Assessment evidence](docs/evidence_matrix.md) · [PRD](docs/PRD.md)

The dataset is fictional. It does not describe IBM's actual workforce, predict who will leave, or justify employment decisions about individuals.

## Run locally

Use Python **3.12.8** and open this repository as its own workspace.

```powershell
py -3.12 -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe -m streamlit run app.py
```

Open the local address printed by Streamlit. The reviewed data is included; a Kaggle login is not needed to run the app. On macOS/Linux, use `python3.12` and `.venv/bin/python`.

## Business case and audience

Where is attrition concentrated, which workplace characteristics are associated with it, and what should HR investigate before acting? Counts alone favour large groups; RetainWise therefore shows rates with denominators. A difference is an observation, not an explanation of why someone left.

An HR Director gets a short overview and practical questions for discussion. A People Analyst can inspect group sizes, quartiles and decision rules. A governance reviewer can find provenance, demographic limitations and prohibited uses without reading code.

## Business requirements and dashboard design

| Requirement | Evidence | Question |
|---|---|---|
| BR1 · Overview | Executive Overview | What is the overall picture, including counts, proportions and department composition? |
| BR2 · Workplace | Workforce Patterns | How do rates differ by overtime, satisfaction, involvement, balance, travel and role? |
| BR3 · Tenure and compensation | Workforce Patterns | How do centre and spread differ between outcomes? |
| BR4 · Fairness | Fairness & Governance | What group differences are visible, and what safeguards apply? |
| BR5 · Responsible decisions | Overview recommendations; Governance | What could HR investigate, and what should it avoid concluding or automating? |

Five pages cover Overview, Patterns, Hypothesis Lab, Fairness & Governance, and Methodology & Project Plan. Department, role, travel and overtime filters apply to Overview, Patterns and Fairness. Active filters and cohort size are visible. Clearing a filter shows an empty state; Reset restores all records. The Lab always uses the full population and labels that scope explicitly.

Count/rate bars, precomputed box plots and shared-bin histograms serve different questions. Histograms use within-outcome percentages because outcome sizes differ. Major charts have explanations and caveats; technical tables supply textual alternatives. No individual points or raw-record download are offered in the dashboard.

## Dataset and preparation

[IBM HR Analytics Employee Attrition & Performance](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset), published by Pavan Subhash on Kaggle, has **1,470 fictional records and 35 source columns**. Kaggle describes it as created by IBM data scientists for analytics practice. Its listed terms are **Database: Open Database, Contents: Database Contents**, not CC0. See [source attribution and licence links](data/SOURCE.md).

1. [Notebook 01](jupyter_notebooks/01_data_collection.ipynb) inspects schema, types, categories, missing values, duplicates, identifier uniqueness, constants and target balance.
2. [Notebook 02](jupyter_notebooks/02_data_cleaning.ipynb) validates the source, excludes the identifier and three verified constants, derives transparent fields, and writes `data/processed/v1` programmatically.
3. [Notebook 03](jupyter_notebooks/03_analysis_and_hypotheses.ipynb) calculates BR1–BR4 comparisons and evaluates the original H1–H4.

This source has no missing values or duplicate rows. EmployeeNumber is unique; EmployeeCount, Over18 and StandardHours are constant. No imputation, outlier deletion, resampling or modelling is performed. Four exclusions and four derived fields leave 35 processed columns. The [dictionary](data/processed/v1/data_dictionary_v1.csv) explains them; [metadata](data/processed/v1/metadata_v1.json) records transformations and hashes.

Age bands are 18–29, 30–39, 40–49 and 50–60; tenure bands are 0–1, 2–5, 6–10 and 11+ years. These are display groupings, not risk categories. The app consumes reviewed v1 data rather than cleaning the source on a page visit.

## Findings and hypotheses

These are full-v1 descriptive results. “Supported” does not imply a significance test or causal finding. Exact evidence is saved in [hypothesis_evidence_v1.json](data/processed/v1/hypothesis_evidence_v1.json).

| Original hypothesis | Result | Calculated evidence |
|---|---|---|
| H1 · Overtime records have higher observed attrition | Supported | Yes: 127/416 = 30.53%; No: 110/1,054 = 10.44%; gap 20.09 percentage points |
| H2 · Attrited records have shorter company tenure | Supported | Attrited n=237: mean 5.13, median 3, Q1–Q3 1–7 years; retained n=1,233: mean 7.37, median 6, Q1–Q3 3–10 |
| H3 · Lower satisfaction categories have higher rates | Mixed | Categories 1–4: 66/289 = 22.84%, 46/280 = 16.43%, 73/442 = 16.52%, 52/459 = 11.33%; middle categories are not monotonic |
| H4 · Attrited records have lower median monthly income | Supported | Attrited n=237: median 3,202, Q1–Q3 2,373–5,916; retained n=1,233: median 5,204, Q1–Q3 3,211–8,834, in source units |

Overall, **237/1,470 records show attrition (16.12%)** and 1,233 show retention. Quartiles use pandas' linear interpolation. H2 requires both mean and median to be lower. H3 requires non-increasing rates across categories for full support; agreeing endpoints with an intervening rise give Mixed. The operational rules are recorded in notebook 03.

## Recommendations and limits

Use the overtime comparison to frame voluntary research about workload and scheduling. Review onboarding and role expectations alongside tenure patterns. Add role, level and employee-experience context before interpreting income or satisfaction differences. These are investigation areas, not prescriptions with estimated effects.

There are no dates, exit explanations or causal experiment. The attrition proportion is not an annual turnover rate. Shorter tenure among leavers can partly reflect less time to accumulate service. Income currency is undocumented; no currency symbols or savings estimates are invented. The imbalanced fictional population and unadjusted comparisons cannot establish why anyone left, generalise to an employer or predict what an intervention would achieve.

## Ethics, privacy and governance

The prototype does not process actual employee personal data. It nevertheless avoids unnecessary identifiers, individual scoring, rankings and demographic targeting. Groups below n=10 have attrition counts and rates withheld; cohorts below n=10 show no outcome metrics. Groups below n=30 are flagged; outcome distributions below n=10 are omitted.

This display rule is educational, not a guarantee of anonymity. Removing an identifier does not anonymise real workforce records. Repeated filtering can reveal information through differencing, so a real system needs disclosure controls and restricted access.

Real workforce analytics requires a defined purpose, documented lawful basis, fair and transparent processing, minimisation, accuracy, retention rules, accountability and appropriate human oversight. Employment consent can be problematic because of the power imbalance. Assess whether a DPIA is required, especially for high-risk monitoring or profiling. Consult workers and consider damaged trust, team stigma and managerial misuse as social risks.

## Legal and social implications

The [Equality Act 2010, section 4](https://www.legislation.gov.uk/ukpga/2010/15/section/4) includes age, sex, and marriage and civil partnership among protected characteristics. Source-labelled Gender is binary and incomplete; it is not a legal definition of sex. MaritalStatus does not establish civil-partnership status. Observed differences do not establish discrimination or justify differential treatment.

RetainWise prohibits solely automated employment decisions about individuals. A future individual-recommendation system needs a fresh legal assessment, meaningful human review and an effective challenge route. Reviewers need the authority to reject a recommendation, rather than routinely approve it.

See [ICO worker-monitoring guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/employment/monitoring-workers/) and [automated processes and oversight](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/employment/monitoring-workers/what-do-we-need-to-do-if-we-use-monitoring-tools-that-use-solely-automated-processes/). Checked **24 October 2026**: ICO flags guidance as under review after the Data (Use and Access) Act 2025. Check current law, commencement and guidance before real use. This is an educational prototype, not legal advice.

## Reproduce and test

```powershell
.venv/Scripts/python.exe -m pip install -r requirements-dev.txt
.venv/Scripts/python.exe -m ipykernel install --prefix .venv --name python3
.venv/Scripts/python.exe scripts/run_notebooks.py
.venv/Scripts/python.exe -m pytest -q
```

Each notebook runs in its own fresh kernel. The original CSV is included; `scripts/download_data.py` can reacquire it directly and rejects a changed checksum. Outputs are deterministic. `.gitattributes` preserves CSV bytes across operating systems. [Testing results](docs/testing.md) distinguish executed checks from outstanding gates; [usability scenarios](docs/user_testing.md) do not claim external participants.

## Accessibility and UX

Labelled controls, readable headings, tooltips, natural category order and technical tables accompany the visuals. Outcome labels and histogram patterns supplement colour. Streamlit columns adapt to narrower screens and the sidebar collapses. These are practical accessibility choices, not WCAG certification. Independent keyboard and screen-reader review remain follow-up work.

## Project lifecycle and reflection

The [Unit 3 board](https://github.com/users/chasimarshad-bot/projects/4) tracks Status and MoSCoW Priority. The [plan](docs/plan.md) records dependencies and acceptance evidence. The [lifecycle](docs/lifecycle.md) covers implementation, release, maintenance, versioned updates, evaluation and retirement. The static fictional source has no scheduled refresh; real use would require named HR data and governance owners.

[Build reflection](docs/retrospective.md) records actual issues: source terms, satisfaction's non-monotonic result, narrow filters, snapshot interpretation and hosting compatibility. It is not Ch Asim's personal reflection. The [changelog](docs/CHANGELOG.md) records delivered work.

## Deployment

Prepared for Streamlit Community Cloud or a Python container service; no live URL is claimed. There is no authenticated Streamlit hosting session in this environment. Sites uses Cloudflare Workers, which cannot host this persistent Python process. See [release instructions](docs/deployment.md). The repository remains private.

## Technologies and structure

Python 3.12.8, pandas, NumPy, Streamlit, Plotly, Jupyter/nbclient, pytest and Playwright. Runtime and development requirements are pinned separately.

```text
app.py                 Navigation and shared styling
retainwise/            Validation, analytics, charts and pages
data/raw/              Untouched source CSV
data/processed/v1/     Data, dictionary, metadata and evidence
jupyter_notebooks/     Three executed notebooks
scripts/               Acquisition, execution, board and browser QA
tests/                 Analytical and Streamlit regression checks
docs/                  PRD, plan, evidence, testing and release record
docs/ci-workflow.yml   Reproducibility workflow template (not activated)
```
