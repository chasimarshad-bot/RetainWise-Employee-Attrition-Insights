"""Audience-specific pages sharing reviewed analytics and filter behaviour."""
import json
import re
import pandas as pd
import streamlit as st
from .data import ROOT, PROCESSED, load_data, AGE_ORDER, TENURE_ORDER, ORDINALS
from .analysis import rate_table, distribution, hypothesis_evidence, HYPOTHESES, filter_data, MIN_GROUP
from . import charts

FILTERS = {'Department': 'Department', 'JobRole': 'Job role', 'BusinessTravel': 'Business travel', 'OverTime': 'Overtime'}
LABELS = {'OverTime': 'Overtime', 'JobSatisfaction': 'Job satisfaction', 'EnvironmentSatisfaction': 'Environment satisfaction',
    'Department': 'Department', 'JobRole': 'Job role', 'AgeBand': 'Age band', 'TenureBand': 'Company tenure band',
    'Gender': 'Gender (source label)', 'MaritalStatus': 'Marital status',
    'JobInvolvement': 'Job involvement', 'WorkLifeBalance': 'Work–life balance', 'BusinessTravel': 'Business travel',
    'MonthlyIncome': 'Monthly income (source units)', 'YearsAtCompany': 'Company tenure (years)',
    'YearsInCurrentRole': 'Time in current role (years)', 'TotalWorkingYears': 'Total working years',
    'YearsWithCurrManager': 'Time with current manager (years)'}


@st.cache_data
def data():
    return load_data()


def document_text(name):
    """Resolve document links against the repository, rather than app routes."""
    text = (ROOT / 'docs' / name).read_text(encoding='utf-8')
    base = 'https://github.com/chasimarshad-bot/RetainWise-Employee-Attrition-Insights/'
    def replace(match):
        label, target = match.groups()
        if target.startswith(('https://', 'http://', '#', 'mailto:')):
            return match.group(0)
        location = 'tree/main/docs/' if target.endswith('/') else 'blob/main/docs/'
        return f'[{label}]({base}{location}{target})'
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', replace, text)


def reset():
    for col in FILTERS:
        st.session_state[f'filter_{col}'] = sorted(data()[col].unique())


def sidebar():
    with st.sidebar:
        st.markdown('### ◈ RetainWise')
        st.caption('Responsible workforce analytics')
        st.divider()
        st.markdown('**Explore a workforce group**')
        st.caption('Filters apply to Overview, Patterns and Fairness. The Lab always uses the full dataset.')
        st.button('Reset filters', on_click=reset, width='stretch')
        for col, label in FILTERS.items():
            values = sorted(data()[col].unique())
            st.multiselect(label, values, default=values, key=f'filter_{col}', help='Clear all selections to show an empty cohort. Reset restores all groups.')
        st.divider()
        st.caption('Fictional IBM practice dataset · v1\n\nNo individual predictions or employment decisions.')


def cohort():
    source = data()
    selected = {col: st.session_state.get(f'filter_{col}', sorted(source[col].unique())) for col in FILTERS}
    df = filter_data(source, selected)
    active = [f"{FILTERS[col]}: {', '.join(values) if values else 'none'}" for col, values in selected.items() if len(values) != source[col].nunique()]
    st.caption('ACTIVE FILTERS · ' + (' | '.join(active) if active else 'All departments, roles, travel and overtime categories'))
    st.caption(f'{len(df):,} of {len(source):,} fictional records in this view. Rates describe this cohort, not a yearly turnover measure.')
    if len(df) == 0:
        st.info('No records match these filters. Reset filters or broaden your selections to continue.')
        return None
    if len(df) < MIN_GROUP:
        st.warning(f'This selection contains fewer than {MIN_GROUP} records. Outcome metrics are withheld. Broaden the filters.')
        return None
    if len(df) < 30:
        st.warning('Small cohort: fewer than 30 records. Differences may be unstable.')
    return df


def hero(kicker, title, description):
    st.markdown(f'<div class="eyebrow">{kicker}</div>', unsafe_allow_html=True)
    st.title(title)
    st.markdown(f'<div class="intro">{description}</div>', unsafe_allow_html=True)
    st.write('')


def explain(shows, matters, caution='These are observed associations in fictional data. They do not explain why people left.'):
    st.markdown(f'**What this shows**  \n{shows}\n\n**Why it matters**  \n{matters}\n\n**Caution**  \n{caution}')


def table_detail(table, title='View figures and calculation'):
    with st.expander(title):
        st.caption('Rate = attrited ÷ group n × 100. Percentage-point differences subtract rates. Groups below n=10 are withheld; groups below n=30 are flagged. This rule does not guarantee privacy in a real deployment.')
        st.dataframe(table.rename(columns={**LABELS, 'n': 'Employees (n)', 'attrited': 'Attrited', 'rate_pct': 'Attrition (%)', 'caution': 'Interpretation'}), hide_index=True, width='stretch')


def rate_chart(df, field, title, order=None):
    table = rate_table(df, field, order)
    label = LABELS.get(field, field)
    display = table.copy()
    if field in ORDINALS:
        display[field] = display[field].map(lambda value: f'{value} · {ORDINALS[field][value]}').astype(str)
    if table.rate_pct.notna().sum() == 0:
        st.info('No group rates can be shown: every group has fewer than 10 records. Broaden the filters to compare rates.')
        table_detail(display)
        return table
    fig = charts.rates(display, field, title)
    fig.update_xaxes(title_text=label)
    st.plotly_chart(fig, width='stretch', alt=f'{title}. The figures table provides group sizes, attrited counts and observed percentages.')
    if table.rate_pct.isna().any():
        st.caption('Some groups are withheld (n < 10). Their attrition counts and rates are omitted from the chart and table.')
    table_detail(display)
    return table


def executive():
    hero('WORKFORCE BRIEF', 'RetainWise', 'Responsible Employee Attrition Insights. Explore workforce patterns while keeping fairness, privacy and responsible interpretation visible.')
    st.info('This is a fictional employee dataset created for analytics practice. It does not represent IBM’s real workforce.')
    df = cohort()
    if df is None:
        return
    total, left = len(df), int(df.Attrition_Flag.sum())
    cols = st.columns(5)
    for col, label, value in zip(cols, ['Employees', 'Attrited', 'Attrition rate', 'Retained', 'Median tenure'],
        [f'{total:,}', f'{left:,}', f'{100*left/total:.1f}%', f'{total-left:,}', f'{df.YearsAtCompany.median():g} years']):
        col.metric(label, value)
    st.write('')
    st.subheader('The workforce at a glance')
    st.markdown(f'In the current selection, **{left:,} of {total:,} records** show attrition. The remaining **{100*(total-left)/total:.1f}%** show retention. There is no observation period, so this is a dataset proportion rather than an annual attrition rate.')
    left_col, right_col = st.columns(2)
    with left_col:
        st.plotly_chart(charts.outcomes(df), width='stretch', alt=f'Employee outcomes: {total-left:,} retained and {left:,} attrited in the selected cohort.')
        explain('Counts for each outcome in the selected group.', 'The number of records behind each outcome helps put rate and distribution comparisons in context.')
        table_detail(df.Status.value_counts().rename_axis('Outcome').reset_index(name='Employees'))
    with right_col:
        rate_chart(df, 'OverTime', 'How observed attrition differs by overtime', ['No', 'Yes'])
        explain('Attrition rates for the two recorded overtime categories. Hover or open the figures to check each denominator.', 'Workload and scheduling are reasonable topics for a wider staff conversation.')
    rate_chart(df, 'TenureBand', 'Attrition across company tenure bands', TENURE_ORDER)
    explain('Company tenure grouped into four transparent bands.', 'Different points in the employee journey may warrant different research questions.', 'Tenure was measured in the source snapshot. Shorter tenure among leavers can partly reflect less time to accumulate service; the data cannot separate that effect.')
    st.subheader('Questions for the next HR discussion')
    for title, text in [
        ('Review workload and scheduling', 'Use the overtime comparison to frame voluntary staff research. Hours, workload intensity and reasons for leaving are absent, so the dashboard cannot tell HR which scheduling change would help.'),
        ('Look more closely at the early employee experience', 'Review onboarding and role expectations alongside tenure patterns. Do not assume a tenure band explains a departure or identifies an individual who needs an intervention.'),
        ('Add context before making decisions', 'Bring in staff feedback, role mix and a reviewed governance plan. Demographic differences belong in an aggregate audit, never in individual targeting.')]:
        with st.container(border=True):
            st.markdown(f'**{title}**')
            st.write(text)
    st.subheader('Workforce composition')
    rate_chart(df, 'Department', 'Department sizes and observed attrition')
    explain('Department rates with the corresponding workforce sizes in the figures table.', 'Department composition gives context to comparisons elsewhere; role and pay mix can differ between departments.')


def patterns():
    hero('EXPLORE / WORKPLACE & EXPERIENCE', 'Workforce Patterns', 'Compare workplace characteristics, tenure and income. Change the cohort in the sidebar, then check the group sizes before interpreting a difference.')
    df = cohort()
    if df is None:
        return
    tab1, tab2 = st.tabs(['Workplace & engagement', 'Tenure & compensation'])
    with tab1:
        factor = st.selectbox('Workplace characteristic', ['OverTime', 'JobSatisfaction', 'EnvironmentSatisfaction', 'JobInvolvement', 'WorkLifeBalance', 'BusinessTravel', 'JobRole'], format_func=lambda x: LABELS.get(x, 'Job role'))
        order = list(ORDINALS[factor]) if factor in ORDINALS else (['No', 'Yes'] if factor == 'OverTime' else None)
        rate_chart(df, factor, f'Observed attrition by {LABELS.get(factor, "job role").lower()}', order)
        explain('Each bar is the share of its group recorded as attrited, not the number of employees in that group.', 'Comparing rates helps distinguish a large workforce group from a group with a larger attrition share.', 'Group composition can explain part of a difference. Ordinal scales follow the source order; the categories are not measured distances.')
    with tab2:
        factor = st.selectbox('Tenure or compensation measure', ['YearsAtCompany', 'YearsInCurrentRole', 'TotalWorkingYears', 'YearsWithCurrManager', 'MonthlyIncome'], format_func=lambda x: LABELS[x])
        st.plotly_chart(charts.boxes(df, factor, LABELS[factor]), width='stretch', alt=f'{LABELS[factor]} by employee outcome. The accompanying table gives sample sizes, medians and quartiles.')
        explain('The line marks the median; the box spans the middle half of the group. Whiskers end at the most distant values within 1.5 interquartile ranges.', 'The median and spread show more than a single average can.', 'Outlier points are omitted. Outcome groups below n=10 are withheld. Income is in source units; currency is undocumented. No individual records are shown.')
        summary = distribution(df, factor)
        table_detail(summary.loc[summary.n >= MIN_GROUP], 'View sample sizes, means, medians and quartiles')
        st.plotly_chart(charts.histogram(df, factor, LABELS[factor]), width='stretch', alt=f'Binned distribution of {LABELS[factor].lower()}, using percentages within each employee outcome.')
        explain('A binned distribution with a separate percentage denominator for each outcome.', 'Normalising each outcome helps compare shapes despite the unequal number of retained and attrited records.', 'The bins are shared across outcomes, include their left boundary, and exclude their right boundary except the final bin. Binning can hide detail; no causal comparison is implied.')


def hypotheses():
    hero('EVIDENCE / FULL DATASET', 'Hypothesis Lab', 'Four questions defined in the PRD, evaluated using descriptive evidence. “Supported” describes this dataset; it is not a significance test or a causal finding.')
    df = data()
    st.info(f'Fixed baseline: all {len(df):,} fictional records. Sidebar filters do not change these results.')
    evidence = hypothesis_evidence(df)
    rules = {
        'H1': 'Supported if the overtime Yes rate exceeds the No rate; otherwise Not Supported.',
        'H2': 'Supported if both mean and median company tenure are lower among attrited records; Mixed if only one is lower; otherwise Not Supported.',
        'H3': 'Supported if rates never increase from satisfaction 1 to 4. Mixed if the lowest category exceeds the highest but the sequence is not monotonic; otherwise Not Supported.',
        'H4': 'Supported if the attrited median monthly income is lower than the retained median; otherwise Not Supported.'}
    interpretations = {
        'H1': f"The observed rate gap is {evidence['H1']['difference_pp']:.2f} percentage points. The source has no overtime hours or reasons for departure.",
        'H2': 'Both the mean and median are compared, rather than selecting whichever summary favours the statement. This snapshot cannot establish whether shorter tenure contributes to leaving.',
        'H3': 'The lowest and highest satisfaction categories differ, but the middle categories do not form a steady decline. Calling the pattern simply monotonic would overstate the evidence.',
        'H4': 'The medians differ in source income units. Job level, occupation and tenure may also differ between outcome groups; no adjusted or causal effect has been estimated.'}
    for key, statement in HYPOTHESES.items():
        with st.container(border=True):
            st.subheader(f"{key} · {evidence[key]['outcome']}")
            st.write(statement)
            if key == 'H1':
                st.metric('Overtime rate gap', f"{evidence[key]['difference_pp']:.2f} pp")
                rate_chart(df, 'OverTime', 'H1 · Overtime comparison', ['No', 'Yes'])
            elif key == 'H3':
                rate_chart(df, 'JobSatisfaction', 'H3 · Satisfaction in source order', [1, 2, 3, 4])
            else:
                field = 'YearsAtCompany' if key == 'H2' else 'MonthlyIncome'
                st.plotly_chart(charts.boxes(df, field, LABELS[field]), width='stretch', alt=f'{LABELS[field]} for attrited and retained records. Exact summaries are in the technical evidence table.')
            st.write(interpretations[key])
            with st.expander('Technical detail · decision rule and exact evidence'):
                st.write(rules[key])
                st.caption('Rate = attrited / n × 100. Median = 50th percentile. Quartiles use linear interpolation. No confidence interval or population inference is claimed; records are fictional, not a probability sample.')
                st.dataframe(pd.DataFrame(evidence[key]['table']), hide_index=True, width='stretch')
            st.caption('Association is not causation. The dataset cannot predict an intervention’s effect.')


def governance():
    hero('AUDIT / FAIRNESS & RESPONSIBLE USE', 'Fairness & Governance', 'Demographic comparisons can reveal questions worth asking. They cannot justify treating an employee differently.')
    st.info('These records are fictional. This prototype does not process actual employee personal data and must not be presented as IBM workforce research.')
    st.subheader('An aggregate audit lens')
    df = cohort()
    if df is not None:
        field = st.selectbox('Audit characteristic', ['AgeBand', 'Gender', 'MaritalStatus'], format_func=lambda x: {'AgeBand': 'Age band', 'Gender': 'Gender (source label)', 'MaritalStatus': 'Marital status'}[x])
        rate_chart(df, field, 'Observed group differences — audit context only', AGE_ORDER if field == 'AgeBand' else None)
        explain('Group-level rates with denominators, within the selected cohort.', 'An audit can prompt questions about workplace experience and data coverage.', 'Small groups are unstable. The source Gender field has only Female/Male labels and is not a legal definition of sex or a complete account of gender. MaritalStatus does not establish civil-partnership status. These are not measures of discrimination or evidence of demographic motivations.')
    st.subheader('Where this dashboard belongs')
    left, right = st.columns(2)
    with left:
        with st.container(border=True):
            st.markdown('**Appropriate uses**')
            st.markdown('- Aggregate workforce planning\n- Questions for voluntary staff research\n- Reviewing organisational patterns\n- Identifying missing context and data limitations')
    with right:
        with st.container(border=True):
            st.markdown('**Prohibited uses**')
            st.markdown('- Individual flight-risk labels or rankings\n- Solely automated employment decisions\n- Targeting protected demographic groups\n- Presenting an association as a cause')
    st.subheader('Before using real employee records')
    st.markdown('''A real deployment would need a defined purpose, a documented lawful basis and a proportionate design. Employment consent is often problematic because of the power imbalance. Tell workers what is processed and why; minimise collected fields; check accuracy; restrict access; set retention and deletion rules; record accountability and offer routes to question results.

Assess whether a data protection impact assessment (DPIA) is required, especially for high-risk monitoring or profiling. Removing an identifier does not anonymise a workforce dataset: combinations of age, role and department can still identify people. The n=10 display rule here is an educational safeguard, not a complete disclosure-control scheme. Repeated filtering and differencing would need review in production.

This prototype is intended for aggregate decision support. It must not be used to make solely automated employment decisions about individuals. Any future individual recommendation system requires a fresh legal and governance assessment, meaningful human review and an effective challenge process. Reviewers need the authority and competence to reject a recommendation.

The Equality Act 2010 protects characteristics including age, sex, and marriage and civil partnership. Source labels do not establish legal categories. Observed rate differences cannot establish discrimination, justify differential treatment, or determine who receives a retention intervention.

Workforce analytics can also damage trust, stigmatise teams and shift attention away from organisational conditions. Consult workers, review how managers interpret the charts and assess whether the analysis serves a legitimate employee as well as organisational purpose.''')
    st.warning('Legal context reviewed 24 October 2026. ICO worker-monitoring guidance is under review following the Data (Use and Access) Act 2025. Check current commencement provisions and guidance before real use. This educational prototype is not legal advice.')
    st.markdown('Sources: [ICO: worker monitoring](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/employment/monitoring-workers/) · [ICO: automated processes and human oversight](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/employment/monitoring-workers/what-do-we-need-to-do-if-we-use-monitoring-tools-that-use-solely-automated-processes/) · [Equality Act 2010, section 4](https://www.legislation.gov.uk/ukpga/2010/15/section/4)')


def methodology():
    hero('PROJECT RECORD / METHODS & DELIVERY', 'Methodology & Project Plan', 'Follow the path from source records to the dashboard, including the decisions, checks and work still needed before submission.')
    metadata = json.loads((PROCESSED / 'metadata_v1.json').read_text(encoding='utf-8'))
    st.subheader('A small, reproducible pipeline')
    st.markdown('Kaggle source → notebook 01 validation → notebook 02 versioned preparation → notebook 03 descriptive evidence → Streamlit pages. The app reads the reviewed v1 output; it does not clean raw data on a page visit.')
    st.markdown('The original identifier and verified constants are excluded. Outcome labels are retained; the binary flag and fixed age/tenure bands are derived transparently. No records are imputed, modelled, ranked or deleted as outliers.')
    with st.expander('Data quality, transformations and checksums'):
        st.json(metadata)
    with st.expander('Data dictionary'):
        st.dataframe(pd.read_csv(PROCESSED / 'data_dictionary_v1.csv'), hide_index=True, width='stretch')
    st.subheader('Lifecycle, maintenance and evaluation')
    st.markdown(document_text('lifecycle.md'))
    st.subheader('Delivery priorities')
    st.markdown(document_text('plan.md'))
    st.subheader('What changed during the build')
    st.markdown(document_text('retrospective.md'))
    st.subheader('Testing and release status')
    st.markdown(document_text('testing.md'))
    st.subheader('Dataset source')
    st.markdown('Dataset: [IBM HR Analytics Employee Attrition & Performance](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset), published by Pavan Subhash. Kaggle lists Database: Open Database, Contents: Database Contents. See data/SOURCE.md for the acquisition record and licence links.')
