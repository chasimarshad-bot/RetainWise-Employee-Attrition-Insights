"""RetainWise Streamlit entry point. Run: python -m streamlit run app.py."""
import streamlit as st
from retainwise.ui import executive, patterns, hypotheses, governance, methodology, sidebar

st.set_page_config(page_title='RetainWise | Workforce insights', page_icon='◈', layout='wide')
st.html('''<style>
.block-container {max-width:1280px; padding-top:4.5rem; padding-bottom:3rem;}
h1 {letter-spacing:-.045em; font-weight:700 !important;}
h2 {letter-spacing:-.025em;}
[data-testid="stMetric"] {background:white; border:1px solid #dce5e9; border-radius:12px; padding:18px;}
[data-testid="stMetricLabel"] {color:#415967;}
[data-testid="stMetricValue"] {font-size:1.9rem;}
[data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] p {color:#465D6B !important; opacity:1 !important;}
[data-testid="stMarkdownContainer"] code {color:#136B42 !important;}
[data-testid="stSidebar"] {border-right:1px solid #dce5e9;}
.eyebrow {color:#137C72; font-size:.78rem; letter-spacing:.16em; font-weight:700; margin-bottom:.5rem;}
.intro {color:#415967; max-width:750px; font-size:1.08rem; line-height:1.6;}
.note {border-left:3px solid #137C72; padding:12px 18px; background:#edf5f3; border-radius:0 8px 8px 0; margin:10px 0 20px;}
@media(max-width:700px) {.block-container {padding:4rem 1rem 1rem;} [data-testid="stMetricValue"] {font-size:1.5rem;}}
</style>''')

pages = [st.Page(executive, title='Executive Overview', icon=':material/dashboard:', default=True, url_path='overview'),
    st.Page(patterns, title='Workforce Patterns', icon=':material/bar_chart:', url_path='patterns'),
    st.Page(hypotheses, title='Hypothesis Lab', icon=':material/science:', url_path='hypotheses'),
    st.Page(governance, title='Fairness & Governance', icon=':material/balance:', url_path='governance'),
    st.Page(methodology, title='Methodology & Project Plan', icon=':material/menu_book:', url_path='methodology')]
page = st.navigation(pages)
sidebar()
page.run()
st.divider()
st.caption('RetainWise · Unit 3 capstone · Ch Asim Arshad | Fictional data. Aggregate evidence. Human judgement.')
