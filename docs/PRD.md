# Product Requirements Document

## RetainWise — Responsible Employee Attrition Insights

**Assessment:** Unit 3 Capstone — Ethical Practice and Communication in Data  
**Student:** Ch Asim Arshad  
**Product type:** Interactive Streamlit Data App  
**Primary audience:** HR / People Analytics leadership  
**Secondary audiences:** People Analysts, HR Business Partners, Data Protection / Governance stakeholders  
**Status:** Build specification  
**Submission deadline:** Sunday 25 October 2026, 23:59:59  
**Priority:** Submission-critical

---

# 1. Product Vision

RetainWise will be a professional, interactive workforce analytics dashboard that helps HR leaders understand patterns associated with employee attrition while demonstrating responsible handling of sensitive workforce information.

The application will not attempt to decide which individual employee is likely to leave, nor recommend employment action against individuals.

Its purpose is to:

- explain workforce attrition patterns clearly;
- allow non-technical users to explore important workforce characteristics;
- provide technical users with transparent supporting metrics;
- test clearly defined business hypotheses;
- demonstrate ethical, privacy-aware and fair use of employee analytics;
- show how analytical findings can support further investigation without implying causation;
- demonstrate a full analytics project lifecycle, including planning, implementation, maintenance, evaluation and reflection.

The finished product must look and behave like something that could be presented to an HR leadership team, not like a collection of coursework charts.

---

# 2. Assessment Strategy

The project must produce explicit evidence for every Unit 3 Pass criterion.

The current handbook requires:

| Criterion | Required evidence in RetainWise |
|---|---|
| **1.1** Ethical issues, privacy and governance | Dedicated Ethics & Governance page + README analysis of privacy, fairness, demographic variables, responsible-use boundaries |
| **1.2** Legal and social implications | UK employment/data-protection context, Equality Act discussion, responsible processing controls, limitations on automated decision-making |
| **2.1** Communicate complex insights to technical and non-technical audiences | Executive summaries plus technical expanders containing calculations, sample sizes and methodology |
| **2.2** Appropriate visualisations and narratives | Interactive dashboard with several plot types, filters, explanatory text and clear data story |
| **2.3** Structured documentation | Complete README, documented notebooks/code, labels, help text, tooltips, chart explanations and methodology |
| **3.1** Complete project plan | GitHub Project / MoSCoW board plus README lifecycle covering implementation, release, maintenance, updating and evaluation |
| **3.2** Reflection on execution | Development retrospective covering data, analytical, ethical, technical, UX, scope and time challenges |

The project must also meet the handbook’s higher-quality expectations: a functioning professional web dashboard, clear real-world audience, responsive design, accessibility consideration, hypotheses validated against evidence, at least two different plot types tied to business requirements, clean code, sensible Git history and versioned data outputs.

---

# 3. Dataset

## 3.1 Selected dataset

Use:

**IBM HR Analytics Employee Attrition & Performance**

The source describes it as a fictional dataset created by IBM data scientists for analytics practice.

Expected source structure:

- approximately **1,470 employee records**
- approximately **35 source columns**
- target: `Attrition`
- workforce attributes covering job role, department, overtime, tenure, satisfaction, compensation and demographics

The dataset is fictional and must never be described as IBM's actual employee population.

Source licensing and attribution must be recorded accurately from the original Kaggle dataset page.

## 3.2 Important source limitations

The application must explicitly recognise that:

- the data is synthetic/fictional;
- there is no date dimension showing when employees left;
- no causal experiment was performed;
- compensation fields do not have a clearly documented currency in the source;
- attrition is imbalanced;
- the dataset is relatively small;
- the dataset cannot establish why an employee left;
- the analysis cannot establish what would happen after an intervention.

Do not invent:

- monthly attrition trends;
- hire/exit dates;
- financial savings;
- employee replacement costs;
- currency symbols;
- causal explanations;
- demographic motivations.

---

# 4. Problem Statement

HR leaders need to understand where attrition is concentrated and which workplace characteristics are associated with employees leaving.

A poorly designed attrition system could create serious problems by:

- treating correlation as causation;
- profiling individuals;
- over-relying on age, sex or marital status;
- making employment decisions using opaque scores;
- exposing employee-level data unnecessarily;
- presenting small-group statistics without context.

RetainWise will therefore be an **aggregate decision-support dashboard**, not an employee-ranking system.

The business question is:

> How can HR leaders identify meaningful workforce attrition patterns while ensuring the analysis remains transparent, fair, privacy-aware and appropriate for responsible human decision-making?

---

# 5. Target Users

## Persona A — HR Director

Non-technical.

Needs to understand quickly:

- overall attrition;
- where meaningful differences appear;
- what HR should investigate;
- what the dashboard cannot prove.

The HR Director should not need to understand Python or statistics.

## Persona B — People Analyst

Technical/analytical.

Needs access to:

- group sizes;
- exact rates;
- medians/means;
- filters;
- data-quality information;
- hypothesis calculations;
- methodological rationale.

## Persona C — Governance / Data Protection Stakeholder

Needs to understand:

- what data is being used;
- whether real people are identifiable;
- which characteristics are sensitive;
- how demographic analysis is constrained;
- the intended and prohibited uses of the dashboard;
- what governance controls would be needed if the prototype were used with real employee data.

The dashboard must intentionally serve all three audiences.

---

# 6. Business Requirements

## BR1 — Workforce attrition overview

The user must be able to understand:

- total employee population;
- number and proportion attrited;
- number and proportion retained;
- distribution across major organisational categories.

The dashboard must answer:

> What is the overall attrition picture in this dataset?

## BR2 — Workplace factors associated with attrition

Analyse factors such as:

- `OverTime`
- `JobSatisfaction`
- `EnvironmentSatisfaction`
- `JobInvolvement`
- `WorkLifeBalance`
- `BusinessTravel`

The dashboard must answer:

> Which workplace and engagement characteristics show observable differences in attrition?

All findings must be described as associations.

## BR3 — Tenure and compensation patterns

Analyse:

- `YearsAtCompany`
- `YearsInCurrentRole`
- `TotalWorkingYears`
- `YearsWithCurrManager`
- `MonthlyIncome`

The dashboard must answer:

> How do tenure and compensation measures differ between Attrited and Retained employees?

Do not attach a currency symbol to `MonthlyIncome` unless the original source explicitly establishes one.

## BR4 — Fairness and responsible-use lens

Analyse demographic variables only for aggregate audit and fairness understanding, including where appropriate:

- `Age`
- source-labelled `Gender`
- `MaritalStatus`

The dashboard must answer:

> Do observed attrition rates vary across demographic groups, and what safeguards should apply before using those results operationally?

Demographic characteristics must **not** be used to recommend targeting individuals.

## BR5 — Responsible decision support

Every recommendation must distinguish:

- what the dataset shows;
- what the dataset does not show;
- what HR could reasonably investigate next;
- what HR should not conclude or automate.

---

# 7. Project Hypotheses

The hypotheses must be defined before final interpretation.

Each must ultimately be labelled:

**Supported / Not Supported / Mixed**

based on calculated notebook evidence.

## H1 — Overtime

> Employees recorded as working overtime have a higher observed attrition rate than employees not recorded as working overtime.

Evidence required:

- group sizes;
- attrited counts;
- attrition rates;
- percentage-point difference.

No causal claim.

## H2 — Tenure

> Attrited employees have shorter observed company tenure than retained employees.

Evidence required:

- n;
- mean;
- median;
- quartiles;
- appropriate distribution visualisation.

Use `YearsAtCompany`.

## H3 — Job satisfaction

> Lower job-satisfaction categories have higher observed attrition rates than higher job-satisfaction categories.

Evidence required:

- natural satisfaction order;
- group sizes;
- attrition count;
- attrition rate.

Do not force a monotonic conclusion if the data does not support one.

## H4 — Compensation

> Attrited employees have a lower observed median `MonthlyIncome` than retained employees.

Evidence required:

- medians;
- quartiles;
- group size;
- box/distribution visualisation.

Do not infer that income causes attrition.

## Hypothesis integrity rule

If a hypothesis is not supported, retain it and mark it **Not Supported**.

Do not alter a hypothesis after seeing the result simply to make it succeed.

That is stronger analytical evidence than forcing every hypothesis to be true.

---

# 8. Product Scope

## In scope

- Python data preparation
- Jupyter notebooks
- versioned processed data
- Streamlit web application
- interactive filtering
- Plotly and/or Streamlit-native charts
- descriptive statistics
- hypothesis validation
- group-level attrition analysis
- ethics and governance content
- accessibility considerations
- technical and non-technical explanations
- project planning
- maintenance/update plan
- project retrospective
- GitHub Project / MoSCoW tracking
- deployment
- complete README
- user testing
- reproducibility and QA

## Explicitly out of scope

- individual employee attrition risk scores
- employee ranking
- automated HR decisions
- recommendations to dismiss, promote or retain named employees
- facial/biometric analysis
- real employee records
- machine-learning prediction unless subsequently justified and genuinely understood
- deep learning
- synthetic historical trends
- unsupported financial ROI calculations
- demographic targeting
- pretending correlations are causal

This narrow scope is intentional.

---

# 9. Data Pipeline

## Notebook 01 — Data Collection & Understanding

Responsibilities:

- load source data;
- record source and licence;
- verify shape;
- inspect data types;
- inspect unique values;
- identify duplicate rows;
- check employee identifier uniqueness;
- check missing values;
- inspect category consistency;
- identify constant columns;
- describe target balance;
- create/verify data dictionary.

No cleaning decisions should be silently made here.

## Notebook 02 — Data Cleaning & Versioning

Required validation before transformation:

- duplicates;
- missing data;
- impossible values;
- inconsistent category values;
- constant columns;
- employee identifier behaviour;
- target encoding.

Likely transformations, subject to evidence:

- derive binary `Attrition_Flag`;
- derive transparent age bands;
- derive transparent tenure bands where useful;
- remove constant columns such as fields with a single value if verified;
- remove employee-level identifier from the analytical dashboard dataset if not required;
- preserve the original target label for readability.

Do not blindly alter fields simply because another project did.

## Versioned output

Notebook 02 must programmatically create:

`data/processed/v1/employee_attrition_v1.csv`

This directly demonstrates the handbook requirement for files being stored under a dedicated project-version folder.

Also create if useful:

`data/processed/v1/data_dictionary_v1.csv`

and/or

`data/processed/v1/metadata_v1.json`

containing:

- project version;
- row count;
- column count;
- processing date if appropriate;
- source dataset name;
- transformations;
- excluded fields.

The notebook must demonstrate the directory creation and save operation in code.

## Notebook 03 — Analysis & Hypotheses

This notebook must:

- calculate all evidence for BR1–BR4;
- validate H1–H4;
- print group sizes;
- print exact values used in dashboard narratives;
- separate evidence from interpretation;
- identify small groups;
- avoid causal wording;
- provide data-quality and methodological caveats.

The Streamlit app should consume the processed dataset rather than duplicate data-cleaning logic.

---

# 10. Dashboard Information Architecture

Use a multi-page Streamlit application.

## Page 1 — Executive Overview

Purpose:

> Give an HR leader the whole story within one screen and a small amount of scrolling.

Required content:

### Hero section

Title:

**RetainWise**

Subtitle:

**Responsible Employee Attrition Insights**

Short explanation:

> Explore workforce attrition patterns while keeping fairness, privacy and responsible interpretation visible.

### KPI cards

At minimum:

- total employees;
- attrited employees;
- overall attrition rate;
- retained employees;
- median tenure or another genuinely useful headline metric.

All values calculated from data.

### Headline visualisations

Use at least:

- bar chart for Attrition distribution;
- bar chart for attrition rate by overtime;
- ordered attrition chart by tenure band or other strong business variable.

Below every major chart include:

**What this shows**  
Plain-English explanation.

**Why it matters**  
Business relevance.

**Caution**  
Limitations/association warning where appropriate.

### Executive recommendations

No more than 3–4.

Recommendations must be framed as investigation/action areas rather than causal prescriptions.

---

# 11. Page 2 — Workforce Patterns

Purpose:

> Allow users to explore workplace characteristics associated with attrition.

Sidebar or top filters:

- Department
- JobRole
- BusinessTravel
- OverTime
- optional age band

Show active filters clearly.

Required chart types should include multiple distinct visual forms.

Examples:

- grouped/ordered bar chart;
- box plot;
- histogram/distribution;
- scatter plot if analytically meaningful.

Minimum requirement: the final dashboard must include at least **three distinct plot types**, exceeding the handbook minimum of two.

Each visualisation must have:

- human-readable title;
- labelled axes;
- readable legend;
- useful tooltip;
- sample size where rates are presented;
- explanatory narrative;
- no unnecessary decoration.

Avoid pie charts unless they genuinely improve understanding.

---

# 12. Page 3 — Hypothesis Lab

Purpose:

> Provide the technical bridge between analysis and business narrative.

Display H1–H4 as individual cards or sections.

Each hypothesis section must show:

- hypothesis statement;
- calculation used;
- relevant group sizes;
- key statistic(s);
- supporting visualisation;
- outcome: Supported / Not Supported / Mixed;
- plain-English interpretation;
- limitation;
- explicit “association is not causation” reminder where relevant.

Use Streamlit expanders for:

**Technical detail**

This allows technical users to inspect calculations without overwhelming the executive audience.

This page is important evidence for criterion 2.1.

---

# 13. Page 4 — Fairness, Ethics & Governance

This must be a first-class dashboard page, not a token paragraph.

## 13.1 Dataset reality

State prominently:

> This project uses a fictional employee dataset created for analytics practice. It must not be interpreted as representing IBM's real workforce.

Because the records are fictional, the prototype does not process actual employee personal data.

Then distinguish that from a real deployment.

## 13.2 If real workforce data were used

Explain that employee analytics would require responsible governance including:

- a defined purpose;
- lawful and fair processing;
- transparency;
- data minimisation;
- accuracy;
- access control;
- retention rules;
- accountability;
- appropriate human oversight;
- consideration of a DPIA where the processing may create high risk.

Current ICO worker-monitoring guidance stresses lawful/fair processing, transparency, purpose limitation, minimisation and accountability; it also notes that high-risk worker processing may require a DPIA.

## 13.3 Automated decision-making boundary

RetainWise must state:

> This prototype is intended for aggregate decision support. It must not be used to make solely automated employment decisions about individuals.

If a future system produced individual recommendations, meaningful human review would be required and the organisation would need to assess its applicable data-protection obligations.

## 13.4 Equality and fairness

The source includes age and a field labelled `Gender`.

UK law protects characteristics including age and sex, as well as marriage and civil partnership among others.

The dashboard must make clear that:

- the dataset field name is not itself a legal definition;
- sensitive demographic patterns are shown for fairness/audit understanding;
- observed group differences do not justify differential treatment;
- demographic characteristics must not automatically determine retention interventions.

## 13.5 Small-group caution

Every demographic visual must show group size.

If a subgroup is very small:

- flag it;
- avoid strong recommendations;
- explain statistical instability.

For a real production system, consider minimum-cell suppression.

## 13.6 Responsible-use statement

Display a visible panel:

**Appropriate uses**
- aggregate workforce planning;
- identifying questions for further investigation;
- monitoring organisational patterns;
- evaluating where more research is needed.

**Inappropriate uses**
- automatically labelling individuals as “flight risks”;
- employment decisions based solely on the dashboard;
- targeting workers because of protected characteristics;
- treating association as proof of cause.

---

# 14. Page 5 — Methodology, Project Plan & Reflection

This page ensures criteria 2.3, 3.1 and 3.2 have visible evidence inside the app as well as the README.

Sections:

## Methodology

Explain:

1. source acquisition;
2. validation;
3. cleaning;
4. versioned storage;
5. analysis;
6. hypothesis evaluation;
7. dashboard construction;
8. user testing;
9. QA;
10. deployment.

## Project lifecycle

Show the complete lifecycle:

**Discovery → Planning → Data preparation → Analysis → Dashboard → Testing → Release → Maintenance → Evaluation**

## Maintenance plan

A real implementation would define:

- dataset refresh ownership;
- refresh frequency;
- schema checks;
- data-quality checks;
- version increments;
- regression testing;
- governance review;
- access review;
- documentation update;
- retirement process.

## Update strategy

For a future release:

- create `v2` processed folder;
- preserve v1 for reproducibility;
- record changes in changelog;
- rerun notebooks;
- compare headline metrics;
- rerun dashboard tests;
- update README;
- review ethical implications.

## Evaluation

Evaluate success through:

- dashboard task completion;
- stakeholder comprehension;
- accuracy of metrics;
- user feedback;
- accessibility review;
- data-quality checks;
- broken-link/error checks;
- governance review.

## Reflection

Document genuine practical challenges encountered during this project and what changed because of them.

Possible categories only if they actually occur:

- data limitations;
- ambiguous field meaning;
- class imbalance;
- responsive Streamlit design;
- chart selection;
- deployment;
- accessibility;
- misleading correlations;
- scope control;
- time constraints;

Never fabricate a challenge.

---

# 15. UX Requirements

The handbook expects professional-grade UX.

Therefore:

## Information hierarchy

Every page should follow:

**Question → Metric/visual → explanation → implication → limitation**

Avoid dumping charts with no narrative.

## Navigation

Pages should have clear names and appear in logical order:

1. Executive Overview
2. Workforce Patterns
3. Hypothesis Lab
4. Fairness & Governance
5. Methodology & Project Plan

## Visual consistency

Use a restrained design system:

- consistent typography;
- consistent KPI formatting;
- consistent chart sizing;
- one primary accent;
- one warning colour;
- status colours used consistently.

Do not use colour alone to distinguish meaning.

## Responsive design

Manually inspect at approximately:

- mobile width;
- tablet width;
- desktop width.

Avoid rigid wide layouts that break on smaller screens.

## Accessibility

Target practical WCAG-inspired good practice:

- strong contrast;
- meaningful headings;
- plain English;
- readable font sizes;
- charts accompanied by textual summaries;
- no colour-only distinctions;
- descriptive chart titles;
- tooltips;
- keyboard-friendly Streamlit controls where possible.

Do not claim formal WCAG AA certification unless actually tested to that standard.

---

# 16. Technical Architecture

Recommended stack:

- Python 3.12.8 if compatible with selected dependencies;
- Pandas;
- NumPy;
- Streamlit;
- Plotly Express / Plotly Graph Objects;
- Jupyter / ipykernel;
- optional Matplotlib/Seaborn for notebook exploration.

Architecture:

`Source data`
→ `01 collection`
→ `02 cleaning/versioning`
→ `data/processed/v1`
→ `03 analysis/hypothesis evidence`
→ `Streamlit app`
→ `deployed dashboard`

Keep analytical functions reusable.

Suggested structure:

```text
responsible-employee-attrition-insights/
│
├── app.py
├── pages/
│   ├── 1_Executive_Overview.py
│   ├── 2_Workforce_Patterns.py
│   ├── 3_Hypothesis_Lab.py
│   ├── 4_Fairness_and_Governance.py
│   └── 5_Methodology_and_Project_Plan.py
│
├── src/
│   ├── data_loader.py
│   ├── analytics.py
│   ├── charts.py
│   └── ui.py
│
├── data/
│   ├── raw/
│   └── processed/
│       └── v1/
│           ├── employee_attrition_v1.csv
│           └── data_dictionary_v1.csv
│
├── jupyter_notebooks/
│   ├── 01_data_collection.ipynb
│   ├── 02_data_cleaning.ipynb
│   └── 03_analysis_and_hypotheses.ipynb
│
├── docs/
│   ├── user_testing.md
│   └── CHANGELOG.md
│
├── .streamlit/
│   └── config.toml
├── requirements.txt
├── .python-version
├── .gitignore
└── README.md
```

Do not create unnecessary architecture just to look sophisticated.

---

# 17. Code Quality Requirements

Custom code must:

- use clear names;
- use functions where repeated logic exists;
- include concise docstrings/comments where they aid understanding;
- avoid unnecessary abstraction;
- avoid hard-coded machine-specific paths;
- use `pathlib` where appropriate;
- cache Streamlit data loading appropriately;
- handle empty filtered datasets safely;
- avoid division-by-zero errors;
- handle filter combinations gracefully;
- use deterministic calculations;
- avoid secrets in source control.

The dashboard must never crash because a filter returns no rows.

---

# 18. User Testing

User testing is a high-value piece of evidence and should be performed before submission.

Create:

`docs/user_testing.md`

Test from three perspectives.

## Non-technical HR user

Tasks:

- find overall attrition rate;
- identify one workplace characteristic associated with higher attrition;
- explain one limitation.

## Technical analyst

Tasks:

- find sample sizes behind a hypothesis;
- locate methodology;
- verify how a processed field was derived.

## Governance user

Tasks:

- identify whether real personal data is used;
- identify prohibited uses;
- find the fairness/legal discussion.

For each test record:

- task;
- expected result;
- actual result;
- issue found;
- change made;
- retest result.

Do not fabricate user feedback.

If only self-testing is possible, label it accurately as scenario-based usability testing rather than pretending external users participated.

---

# 19. Project Management / MoSCoW

Create a new GitHub Project specifically for Unit 3.

Fields:

**Status**
- Todo
- In Progress
- Done
- Not Planned

**Priority**
- Must Have
- Should Have
- Could Have
- Won't Have

Must Have items should include:

- business requirements;
- hypotheses;
- source/licensing;
- data notebooks;
- versioned processed data;
- executive dashboard;
- pattern explorer;
- hypothesis page;
- ethics/governance;
- project lifecycle;
- accessibility;
- user testing;
- README;
- deployment;
- QA.

Won't Have should explicitly include:

- individual employee risk scoring;
- automated employment decisions;
- deep learning;
- unnecessary predictive modelling;
- real employee data ingestion.

The board must reflect actual work.

Do not manufacture historical statuses or dates.

---

# 20. Git Strategy

Use genuine incremental development.

Recommended commit subjects as the work actually happens:

`Set up Unit 3 project`

`Document employee attrition dataset`

`Add data collection notebook`

`Add data cleaning and versioning`

`Add hypothesis analysis`

`Add Streamlit app foundation`

`Add executive overview`

`Add workforce pattern explorer`

`Add hypothesis dashboard`

`Add ethics and governance page`

`Add methodology and project plan`

`Add accessibility and user testing`

`Complete project README`

`Fix final QA issues`

Do not force this exact number of commits.

Commit when a genuine unit of work is complete.

Never:

- backdate;
- artificially split completed work;
- rewrite history to appear more human;
- fake development activity.

---

# 21. README Requirements

The README is mandatory and should be assessment-grade.

Required structure:

## Project title

RetainWise — Responsible Employee Attrition Insights

## Live application

Prominent deployed Streamlit link.

## Repository

GitHub repository reference.

## Project overview

Problem, purpose and audience.

## Business case

Why responsible attrition analysis matters.

## Target users

HR Director, People Analyst, Governance stakeholder.

## Business requirements

BR1–BR5.

## Project hypotheses

H1–H4 with final outcomes.

## Dataset

- source;
- fictional nature;
- licence;
- shape;
- relevant fields;
- limitations.

## Data preparation

Explain source → clean → versioned output.

## Dashboard design

Explain information architecture and audience strategy.

## Findings

Evidence only.

## Recommendations

Evidence-based and non-causal.

## Ethics, privacy and governance

Substantial section.

## Legal and social implications

Explain real-world implications without pretending fictional records are real personal data.

## Accessibility and UX

Explain design choices and testing.

## Project lifecycle

Implementation, maintenance, update and evaluation.

## Testing

- notebooks;
- dashboard;
- filters;
- links;
- responsive testing;
- user testing;
- data consistency.

## Challenges and retrospective

Real challenges and responses.

## Technologies

## Repository structure

## How to run locally

## Deployment

## Credits

## Licence / source attribution

---

# 22. Deployment

Deploy the final Streamlit application publicly if feasible.

The deployed application must:

- load successfully from a clean environment;
- contain no local filesystem assumptions;
- contain no secrets;
- use pinned requirements;
- have working navigation;
- load the processed versioned dataset;
- have no visible traceback;
- have no placeholder text.

The live-app link must appear near the top of the README.

If deployment exposes a genuine blocker, document it transparently rather than faking deployment.

---

# 23. Analytical Writing Rules

These are non-negotiable.

Use:

- “associated with”
- “observed in this dataset”
- “higher/lower observed rate”
- “the data suggests”
- “requires further investigation”

Avoid:

- “causes”
- “drives” unless causal evidence exists
- “proves”
- “will leave”
- “high-risk employee”
- “bad employee”
- “loyal employee”
- “this intervention will reduce attrition”

Every numerical claim shown in the dashboard/README must be traceable to notebook or app calculations.

---

# 24. Legal and Governance Position

This is an educational prototype, not legal advice.

The project should demonstrate awareness that, with real employees, workforce analytics could involve personal data and potentially significant employment consequences.

Current ICO guidance emphasises that worker monitoring/analytics must be lawful and fair, transparent, purpose-specific and proportionate, with appropriate accountability. It also notes DPIAs for high-risk processing and meaningful human involvement where automated recommendations feed significant worker decisions.

The Equality Act 2010 includes protected characteristics such as age, sex, and marriage/civil partnership.

This project must therefore intentionally avoid turning demographic characteristics into individual employment recommendations.

---

# 25. Success Metrics

The project is submission-ready only when:

| Measure | Required outcome |
|---|---|
| Unit 3 criteria | 7/7 have explicit evidence |
| Dashboard | All pages load with no errors |
| Hypotheses | H1–H4 evaluated and evidenced |
| Plot types | ≥3 distinct useful types |
| Narratives | Every core visual has explanation |
| Technical/non-technical communication | Both clearly evidenced |
| Ethics/governance | Dedicated page + README |
| Project plan | Implementation through evaluation documented |
| Versioning | Processed `v1` folder created programmatically |
| Accessibility | Explicitly reviewed and documented |
| User testing | Recorded honestly |
| README | Complete, English, no placeholders |
| Git | Genuine incremental history |
| Deployment | Live if technically feasible |
| Reproducibility | Notebooks run from clean kernel |
| Links | All checked |
| Filters | No crash/empty-state failure |
| Sensitive data | No individual risk targeting |
| Causal claims | None unless justified |

---

# 26. Final QA Gate

Before submission:

1. Run every notebook from a fresh kernel in order.
2. Recreate `data/processed/v1`.
3. Launch Streamlit from a clean environment.
4. Exercise every filter combination likely to produce edge cases.
5. Test empty-state behaviour.
6. Test all navigation.
7. Test all external links.
8. Inspect mobile/tablet/desktop layouts.
9. Check chart labels and tooltips.
10. Check colour/contrast and textual chart alternatives.
11. Search entire repository for:
   - TODO
   - placeholder
   - lorem ipsum
   - unsupported currency symbols
   - causal wording
   - local machine paths
   - credentials/secrets
12. Confirm README matches actual functionality.
13. Confirm project board reflects actual state.
14. Confirm deployed app matches repository.
15. Confirm Git working tree clean and local/remote synced.

---

# 27. Assessment Evidence Matrix

Before submission, create a final evidence table.

For each criterion:

**1.1**
- exact README section;
- exact dashboard page;
- relevant notebook evidence.

**1.2**
- exact legal/social/governance evidence.

**2.1**
- executive narrative;
- technical expanders;
- audience-specific design.

**2.2**
- chart types;
- filters;
- narrative;
- UX testing.

**2.3**
- code documentation;
- labels;
- tooltips;
- README structure.

**3.1**
- GitHub Project;
- lifecycle;
- implementation;
- maintenance;
- updating;
- evaluation.

**3.2**
- retrospective;
- real challenges;
- decisions/change log.

Do not mark a criterion complete because it “feels covered”.

Point to the exact evidence.

---

# 28. Originality Guardrail

The supplied previous-student projects are inspiration only.

Do not:

- copy their README prose;
- copy their dashboard layout;
- copy their hypotheses;
- reproduce their code;
- reuse their branding;
- mimic a previous submission feature-for-feature.

RetainWise’s differentiator is:

> Responsible workforce attrition decision support that deliberately separates executive insight, analytical evidence and governance constraints.

That is the project's own narrative.

---

# 29. Review and Verification

- outputs must be checked;
- interpretations must follow executed evidence;
- unsupported statements must be rejected;
- the student must understand the finished work;
- test results, user feedback and project history must reflect actual work.

The objective is to produce a well-understood, properly attributed, critically reviewed submission.

---

# 30. Build Priority

If scope pressure occurs, prioritise in this order:

**First:** all seven assessment criteria.

**Second:** functioning professional dashboard.

**Third:** ethics/governance quality.

**Fourth:** hypothesis evidence.

**Fifth:** README/project lifecycle/testing.

**Sixth:** visual polish.

Do not sacrifice required evidence to add optional technical complexity.

A simple, explainable and fully evidenced feature is worth more than an advanced feature the student cannot defend.

---

# 31. Definition of Done

RetainWise is complete only when a new assessor can:

- open the README and immediately understand the problem and audience;
- open the live dashboard and use it without instructions;
- understand the main workforce findings;
- distinguish correlation from causation;
- find the project hypotheses and their results;
- see why demographic analysis requires caution;
- understand the privacy/governance position;
- see a complete project lifecycle;
- identify how the project would be maintained and updated;
- inspect technical evidence if desired;
- reproduce the data preparation;
- see a genuine development history;
- find no obvious broken functionality or unsupported claims.

The final product should feel like a small professional analytics product built for responsible HR decision support, not a collection of assessment boxes.
