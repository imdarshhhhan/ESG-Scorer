"""
ESG Trust Score Predictor  — Streamlit Frontend
Run: python -m streamlit run App.py
"""

import warnings
warnings.filterwarnings("ignore")
import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

#Page config
st.set_page_config(
    page_title="ESG Trust Score",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

#CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600&display=swap');

#    Base reset     
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
#root > div:first-child { background: #070C1A; }
.main { background: #070C1A !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none; }
div[data-testid="collapsedControl"] { display: none; }
header[data-testid="stHeader"] { background: transparent !important; height: 0 !important; }
footer { display: none !important; }
div[data-testid="stVerticalBlock"] { gap: 0 !important; }
div[data-testid="column"] { padding: 0 0.3rem !important; }
.stAlert { background: #0D1526 !important; border-color: #1A2845 !important; color: #C8D8F8 !important; border-radius: 10px !important; }

#Header
.site-header {
    background: linear-gradient(180deg, #0D1526 0%, #070C1A 100%);
    border-bottom: 1px solid #1A2845;
    padding: 0 3rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 64px;
    position: sticky;
    top: 0;
    z-index: 999;
}
.header-logo { display: flex; align-items: center; gap: 10px; }
.logo-dot {
    width: 32px; height: 32px;
    background: linear-gradient(135deg, #4A7DFF, #34D399);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px;
}
.logo-text { font-family: 'DM Serif Display', serif; font-size: 1.2rem; color: #E8F0FE; }
.header-nav { display: flex; gap: 2rem; align-items: center; }
.nav-link { font-size: .8rem; color: #7B93C4; font-weight: 500; text-transform: uppercase; letter-spacing: .08em; }
.header-badge {
    background: #0D2040; border: 1px solid rgba(74,125,255,.3);
    color: #60A5FA; font-size: .7rem; font-weight: 600;
    padding: 4px 12px; border-radius: 20px;
}

.hero-wrap {
    background: radial-gradient(ellipse 80% 60% at 50% -10%, #0D2040 0%, #070C1A 70%);
    padding: 3.5rem 3rem 2.5rem;
    text-align: center;
    border-bottom: 1px solid #1A2845;
}
.hero-tag {
    display: inline-block; background: #0D2040;
    border: 1px solid rgba(74,125,255,.3); color: #60A5FA;
    font-size: .7rem; font-weight: 600; padding: 4px 14px;
    border-radius: 20px; letter-spacing: .1em;
    margin-bottom: 1.1rem; text-transform: uppercase;
}
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 3.2rem; color: #E8F0FE;
    line-height: 1.1; margin-bottom: .7rem;
}
.hero-title span { color: #4A7DFF; }
.hero-sub {
    font-size: .95rem; color: #7B93C4;
    max-width: 500px; margin: 0 auto 2rem; line-height: 1.6;
}
.hero-stats {
    display: flex; justify-content: center; gap: 3rem;
    margin-top: 1.8rem; padding-top: 1.8rem;
    border-top: 1px solid #1A2845;
}
.stat-item { text-align: center; }
.stat-num { font-family: 'DM Serif Display', serif; font-size: 1.7rem; color: #E8F0FE; }
.stat-lbl { font-size: .72rem; color: #7B93C4; text-transform: uppercase; letter-spacing: .08em; margin-top: 2px; }

#tabs 
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid #1A2845 !important;
    padding: 0 3rem !important;
    gap: 0 !important;
    margin-bottom: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #4A6080 !important;
    font-size: .8rem !important;
    font-weight: 600 !important;
    letter-spacing: .08em !important;
    text-transform: uppercase !important;
    padding: .9rem 1.4rem !important;
    border-bottom: 2px solid transparent !important;
    font-family: 'DM Sans', sans-serif !important;
    margin-bottom: 0 !important;
    line-height: 1.2 !important;
}
            

}
.stTabs [aria-selected="true"] {
    color: #E8F0FE !important;
    border-bottom: 2px solid #4A7DFF !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding: 0 !important;
    background: #070C1A !important;
    margin-top: 2px !important;
}

#search
.search-wrap {
    padding: 2rem 3rem;
    background: #070C1A;
}
.search-title {
    font-size: .75rem; color: #7B93C4; font-weight: 600;
    text-transform: uppercase; letter-spacing: .1em;
    margin-bottom: 1.1rem; text-align: center;
}

#Selectbox
.stSelectbox > div > div {
    background: #0D1526 !important;
    border: 1.5px solid #1A2845 !important;
    border-radius: 10px !important;
    color: #E8F0FE !important;
}
.stSelectbox > div > div:focus-within {
    border-color: #4A7DFF !important;
    box-shadow: 0 0 0 3px rgba(74,125,255,.1) !important;
}
.stSelectbox label {
    color: #7B93C4 !important;
    font-size: .75rem !important;
    font-weight: 600 !important;
    letter-spacing: .08em !important;
    text-transform: uppercase !important;
}

#buttons
.stButton > button {
    background: rgba(74,125,255,0.18) !important;
    color: rgba(200,216,248,0.85) !important;
    border: 1px solid rgba(74,125,255,0.25) !important;
    border-radius: 10px !important;
    padding: .65rem 1.2rem !important;
    font-size: .85rem !important;
    font-weight: 500 !important;
    font-family: 'DM Sans', sans-serif !important;
    width: 100% !important;
    letter-spacing: .02em !important;
    transition: all .2s !important;
    backdrop-filter: blur(4px) !important;
}
.stButton > button:hover {
    background: rgba(74,125,255,0.32) !important;
    border-color: rgba(74,125,255,0.45) !important;
    color: #E8F0FE !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 14px rgba(74,125,255,.15) !important;
}

#Recent searches 
.history-wrap {
    padding: .6rem 3rem 0;
    background: #070C1A;
}
.history-label {
    font-size: .68rem; color: #4A6080; font-weight: 600;
    text-transform: uppercase; letter-spacing: .1em; margin-bottom: .5rem;
}

#Results
.results-wrap {
    padding: 0 1.5rem 3rem;
    background: #070C1A;
}

#Company card 
.company-card {
    background: #0D1526;
    border: 1px solid #1A2845;
    border-radius: 14px;
    padding: 1.4rem;
}
.card-header {
    display: flex; align-items: flex-start;
    justify-content: space-between;
    margin-bottom: 1.2rem; padding-bottom: 1rem;
    border-bottom: 1px solid #1A2845;
}
.company-name {
    font-family: 'DM Serif Display', serif;
    font-size: 1.2rem; color: #E8F0FE;
    line-height: 1.25; max-width: 65%;
}
.trust-badge { text-align: right; }
.trust-label {
    font-size: .62rem; color: #5A7099;
    text-transform: uppercase; letter-spacing: .1em; margin-bottom: 2px;
}
.trust-value {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem; color: #4A7DFF; line-height: 1;
}

# Metric rows     
.metric-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: .45rem 0; border-bottom: 1px solid #0F1A2E;
}
.metric-row:last-child { border-bottom: none; }
.metric-label {
    font-size: .72rem; color: #4A6080; font-weight: 500;
    text-transform: uppercase; letter-spacing: .06em;
}
.metric-value { font-size: .87rem; color: #C8D8F8; font-weight: 500; text-align: right; }

#    Tags     
.tag { display:inline-block; font-size:.68rem; font-weight:600; padding:2px 9px; border-radius:20px; letter-spacing:.04em; }
.tag-low    { background: rgba(10,45,26,.8);  color:#4ADE80; border:1px solid rgba(26,85,48,.6); }
.tag-medium { background: rgba(42,30,0,.8);   color:#FBBF24; border:1px solid rgba(74,56,0,.6); }
.tag-high   { background: rgba(42,10,10,.8);  color:#F87171; border:1px solid rgba(74,21,21,.6); }
.tag-excel  { background: rgba(10,29,58,.8);  color:#60A5FA; border:1px solid rgba(26,53,96,.6); }
.tag-good   { background: rgba(10,42,30,.8);  color:#34D399; border:1px solid rgba(26,74,53,.6); }
.tag-avg    { background: rgba(42,42,10,.8);  color:#FCD34D; border:1px solid rgba(74,74,24,.6); }
.tag-poor   { background: rgba(42,16,0,.8);   color:#FB923C; border:1px solid rgba(74,32,0,.6); }
.tag-mkt    { background: rgba(22,13,58,.8);  color:#A78BFA; border:1px solid rgba(42,26,96,.6); }

# Score bars     
.score-bar-wrap { margin: .2rem 0 .65rem; }
.score-bar-label { display:flex; justify-content:space-between; font-size:.72rem; color:#4A6080; margin-bottom:4px; }
.score-bar-track { background:#0F1A2E; border-radius:6px; height:6px; overflow:hidden; }
.score-bar-fill  { height:100%; border-radius:6px; }
.diff-pos { color:#4ADE80; font-weight:500; }
.diff-neg { color:#F87171; font-weight:500; }
.section-label {
    font-size:.63rem; color:#2A5ABA; font-weight:700;
    text-transform:uppercase; letter-spacing:.12em; margin:1rem 0 .4rem;
}

#Winner banner     
.winner-banner {
    background: linear-gradient(135deg, #0A1830 0%, #070C1A 100%);
    border: 1px solid rgba(74,125,255,.2);
    border-radius: 12px;
    padding: 1.1rem 2rem; text-align: center; margin: 1.2rem 0;
}
.winner-text { font-family: 'DM Serif Display', serif; font-size: 1.1rem; color: #E8F0FE; }
.winner-highlight { color: #4A7DFF; }

# Sector rows     
.rank-row {
    display: flex !important; flex-direction: row !important;
    align-items: center !important; flex-wrap: nowrap !important;
    padding: .6rem 1rem; border-bottom: 1px solid #0F1A2E;
    border-radius: 6px; transition: background .15s; width: 100%;
}
.rank-row:hover { background: #0D1526; }
.rank-num { font-family: 'DM Serif Display', serif; font-size: 1rem; color: #2A4060; min-width: 36px; flex-shrink: 0; }
.rank-num.gold   { color: #FBBF24; }
.rank-num.silver { color: #94A3B8; }
.rank-num.bronze { color: #C07B4A; }
.rank-name { flex: 1 1 auto; font-size: .87rem; color: #C8D8F8; font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-right: .5rem; }
.rank-score { font-family: 'DM Serif Display', serif; font-size: 1rem; color: #4A7DFF; min-width: 48px; text-align: right; flex-shrink: 0; }
.rank-bar-track { width: 100px; height: 5px; background: #0F1A2E; border-radius: 4px; overflow: hidden; margin: 0 .8rem; flex-shrink: 0; }
.rank-bar-fill { height: 100%; border-radius: 4px; }

#Sector benchmarks     
.avg-line {
    background: #0A1830; border: 1px solid rgba(74,125,255,.2);
    border-radius: 10px; padding: .8rem 1.2rem;
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 1rem;
}
.avg-label { font-size: .75rem; color: #7B93C4; text-transform: uppercase; letter-spacing: .07em; font-weight: 600; }
.avg-value { font-family: 'DM Serif Display', serif; font-size: 1.3rem; color: #4A7DFF; }
.sector-stats {
    display: grid; grid-template-columns: repeat(4,1fr);
    gap: 8px; margin-bottom: 1.2rem;
}
.sector-stat { background: #0D1526; border: 1px solid #1A2845; border-radius: 10px; padding: .65rem .9rem; }
.sector-stat .n { font-family: 'DM Serif Display', serif; font-size: 1.4rem; color: #E8F0FE; }
.sector-stat .l { font-size: .68rem; color: #4A6080; text-transform: uppercase; letter-spacing: .07em; margin-top: 2px; }

# Footer   
.site-footer {
    background: #0D1526; border-top: 1px solid #1A2845;
    padding: 2rem 3rem; display: flex;
    justify-content: space-between; align-items: center;
    flex-wrap: wrap; gap: 1rem;
}
.footer-logo { font-family: 'DM Serif Display', serif; font-size: 1rem; color: #E8F0FE; margin-bottom: .25rem; }
.footer-copy { font-size: .75rem; color: #4A6080; }
.footer-right { display: flex; gap: 2rem; }
.footer-col-title { font-size: .65rem; color: #4A7DFF; font-weight: 700; text-transform: uppercase; letter-spacing: .1em; margin-bottom: .4rem; }
.footer-col-item { font-size: .75rem; color: #7B93C4; margin-bottom: .18rem; }
</style>
""", unsafe_allow_html=True)


#Load data & model                                         
@st.cache_data
def load_data():
    return pd.read_csv("display_data.csv")

@st.cache_resource
def load_model():
    try:
        with open("model.pkl", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        prep = pd.read_csv("Global_data_preprocessed.csv")
        x = prep[["environment_score", "social_score", "governance_score"]]
        y = prep["total_score"]
        xt, _, yt, _ = train_test_split(x, y, test_size=0.2, random_state=1, shuffle=True)
        mdl = RandomForestRegressor(random_state=42)
        mdl.fit(xt, yt)
        with open("model.pkl", "wb") as f:
            pickle.dump(mdl, f)
        return mdl

display_df   = load_data()
model        = load_model()
company_list = sorted(display_df["name"].tolist())



def predict_trust(env, soc, gov):
    inp   = pd.DataFrame([[env, soc, gov]],
              columns=["environment_score", "social_score", "governance_score"])
    pred  = model.predict(inp)[0]
    trust = (pred - 600) / (1536 - 600) * 100
    if trust >= 80:
        trust = trust * (1 - 0.07)
    elif trust >= 40:
        trust = trust * (1 + 0.07)
    else:
        trust = trust * (1 + 0.15)
    return round(max(0.0, min(100.0, trust)), 1)

def get_company(name):
    row = display_df[display_df["name"] == name]
    return row.iloc[0] if not row.empty else None

def risk_tag(r):
    cls = {"Low Risk":"tag-low","Medium Risk":"tag-medium","High Risk":"tag-high"}
    return f'<span class="tag {cls.get(r,"tag-medium")}">{r}</span>'

def perf_tag(p):
    cls = {"Excellent":"tag-excel","Good":"tag-good","Average":"tag-avg","Poor":"tag-poor"}
    return f'<span class="tag {cls.get(p,"tag-avg")}">{p}</span>'

def mkt_tag(m):
    return f'<span class="tag tag-mkt">{m}</span>'

def bar(label, val, mx, color):
    pct = min(100, round(val / mx * 100))
    return f"""<div class="score-bar-wrap">
      <div class="score-bar-label"><span>{label}</span><span>{val}</span></div>
      <div class="score-bar-track"><div class="score-bar-fill" style="width:{pct}%;background:{color}"></div></div>
    </div>"""

def diff_html(v):
    sign = "+" if v >= 0 else ""
    cls  = "diff-pos" if v >= 0 else "diff-neg"
    return f'<span class="{cls}">{sign}{v}</span>'

def sector_rank_html(row):
    sector_cos = display_df[display_df["sector"].str.strip() == row["sector"].strip()]
    total      = len(sector_cos)
    below      = (sector_cos["total_esg_score"] < row["total_esg_score"]).sum()
    pct        = round(below / total * 100)
    color      = "#4ADE80" if pct >= 60 else "#FBBF24" if pct >= 35 else "#F87171"
    return f'<span style="color:{color};font-weight:600">Better than {pct}% in {row["sector"]}</span>'

def render_card(row, trust):
    return f"""
    <div class="company-card">
      <div class="card-header">
        <div class="company-name">{row['name']}</div>
        <div class="trust-badge">
          <div class="trust-label">Trust Score</div>
          <div class="trust-value">{trust}</div>
        </div>
      </div>
      <div class="section-label">📋 Identity</div>
      <div class="metric-row">
        <span class="metric-label">Market Type</span>
        <span class="metric-value">{mkt_tag(row['market_type'])}</span>
      </div>
      <div class="metric-row">
        <span class="metric-label">Sector</span>
        <span class="metric-value" style="max-width:58%;text-align:right;font-size:.85rem">{row['sector']}</span>
      </div>
      <div class="section-label">📊 ESG Scores</div>
      {bar("Environment", row["environment_score"], 719, "#34D399")}
      {bar("Social",      row["social_score"],      667, "#60A5FA")}
      {bar("Governance",  row["governance_score"],  475, "#A78BFA")}
      <div class="metric-row">
        <span class="metric-label">Total ESG Score</span>
        <span class="metric-value" style="color:#E8F0FE;font-size:1rem;font-weight:700">{row['total_esg_score']}</span>
      </div>
      <div class="metric-row">
        <span class="metric-label">Sector Avg Diff</span>
        <span class="metric-value">{diff_html(row['sector_avg_diff'])}</span>
      </div>
      <div class="section-label">🏷 Assessment</div>
      <div class="metric-row">
        <span class="metric-label">Grade Impact</span>
        <span class="metric-value">{row['grade_impact']}</span>
      </div>
      <div class="metric-row">
        <span class="metric-label">Risk Level</span>
        <span class="metric-value">{risk_tag(row['risk_level'])}</span>
      </div>
      <div class="metric-row">
        <span class="metric-label">Performance</span>
        <span class="metric-value">{perf_tag(row['performance_level'])}</span>
      </div>
      <div class="metric-row">
        <span class="metric-label">Sector Rank</span>
        <span class="metric-value">{sector_rank_html(row)}</span>
      </div>
    </div>"""


# precompute trust scores for all companies once on startup
@st.cache_data(show_spinner=False)
def get_all_trust_scores():
    df = display_df.copy()
    df["trust_score"] = df.apply(
        lambda r: predict_trust(r["environment_score"], r["social_score"], r["governance_score"]), axis=1)
    return df

all_df = get_all_trust_scores()


#Session state                                             
if "history" not in st.session_state:
    st.session_state.history = []


#  Header
st.markdown("""
<div class="site-header">
  <div class="header-logo">
    <div class="logo-dot">🌱</div>
    <div class="logo-text">ESG Trust Score</div>
  </div>
  <div class="header-nav">
    <span class="nav-link">Compare</span>
    <span class="nav-link">About</span>
    <span class="header-badge">722 Companies</span>
  </div>
</div>
""", unsafe_allow_html=True)



st.markdown("""
<div class="hero-wrap">
  <div class="hero-tag">🌍 ESG Intelligence Platform</div>
  <div class="hero-title">Compare <span>ESG Trust</span><br>Scores Instantly</div>
  <div class="hero-sub">
    Search any two companies to compare their environmental, social
    and governance performance side by side.
  </div>
  <div class="hero-stats">
    <div class="stat-item"><div class="stat-num">722</div><div class="stat-lbl">Companies</div></div>
    <div class="stat-item"><div class="stat-num">47</div><div class="stat-lbl">Sectors</div></div>
    <div class="stat-item"><div class="stat-num">12</div><div class="stat-lbl">Data Points</div></div>
    <div class="stat-item"><div class="stat-num">96.6%</div><div class="stat-lbl">Model Accuracy</div></div>
  </div>
</div>
""", unsafe_allow_html=True)


  
#tabs
  
tab1, tab2 = st.tabs(["🔍  Compare Companies", "🏭  Sector Filter & Benchmarking"])


  
#comparing
  
with tab1:

    #    Search inputs                                         
    st.markdown('<div class="search-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="search-title">Select two companies to compare</div>', unsafe_allow_html=True)

    default1 = st.session_state.get("prefill_c1", "")
    default2 = st.session_state.get("prefill_c2", "")
    idx1 = ([""] + company_list).index(default1) if default1 in company_list else 0
    idx2 = ([""] + company_list).index(default2) if default2 in company_list else 0

    c1, c2, c3 = st.columns([5, 5, 2])
    with c1:
        company1 = st.selectbox("Firm 1", options=[""] + company_list,
                                format_func=lambda x: "Search company name..." if x == "" else x,
                                index=idx1)
    with c2:
        company2 = st.selectbox("Firm 2", options=[""] + company_list,
                                format_func=lambda x: "Search company name..." if x == "" else x,
                                index=idx2)
    with c3:
        st.markdown("<br><br>", unsafe_allow_html=True)
        compare_btn = st.button("Compare →")

    st.markdown('</div>', unsafe_allow_html=True)

    #    Recent searches (below search bar, inside Tab 1)     ─
    if st.session_state.history:
        st.markdown('<div class="history-wrap">', unsafe_allow_html=True)
        st.markdown('<div class="history-label">🕘 Recent Searches</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        btn_cols = st.columns(len(st.session_state.history) + 1)
        for i, (c1h, c2h) in enumerate(st.session_state.history):
            with btn_cols[i]:
                # Show full company names trimmed to fit
                label = f"{c1h} vs {c2h}"
                if st.button(label, key=f"hist_{i}"):
                    st.session_state["prefill_c1"] = c1h
                    st.session_state["prefill_c2"] = c2h
                    st.rerun()
        with btn_cols[-1]:
            if st.button("🗑 Clear", key="clear_hist"):
                st.session_state.history = []
                st.session_state.pop("prefill_c1", None)
                st.session_state.pop("prefill_c2", None)
                st.rerun()

    #  Results                                               
    st.markdown('<div class="results-wrap">', unsafe_allow_html=True)

    if compare_btn:
        if not company1 or not company2:
            st.warning("Please select both companies before comparing.")
        elif company1 == company2:
            st.warning("Please select two different companies.")
        else:
            # Save to history — full names, max 5, no duplicates
            pair = (company1, company2)
            if pair not in st.session_state.history:
                st.session_state.history.insert(0, pair)
                st.session_state.history = st.session_state.history[:5]

            r1 = get_company(company1)
            r2 = get_company(company2)

            if r1 is not None and r2 is not None:
                t1 = predict_trust(r1["environment_score"], r1["social_score"], r1["governance_score"])
                t2 = predict_trust(r2["environment_score"], r2["social_score"], r2["governance_score"])

                st.markdown("<br>", unsafe_allow_html=True)
                
                col1, col2 = st.columns([1, 1], gap="small")



                with col1:
                    st.markdown(render_card(r1, t1), unsafe_allow_html=True)
                with col2:
                    st.markdown(render_card(r2, t2), unsafe_allow_html=True)

                # Winner banner
                if t1 != t2:
                    winner = r1["name"] if t1 > t2 else r2["name"]
                    loser  = r2["name"] if t1 > t2 else r1["name"]
                    wt, lt = max(t1, t2), min(t1, t2)
                    st.markdown(f"""
                    <div class="winner-banner">
                      <div class="winner-text">
                        <span class="winner-highlight">{winner}</span> leads with a Trust Score of
                        <span class="winner-highlight">{wt}</span> —
                        {round(wt - lt, 1)} points ahead of {loser} ({lt})
                      </div>
                    </div>""", unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="winner-banner">
                      <div class="winner-text">Both companies are <span class="winner-highlight">tied</span> on Trust Score!</div>
                    </div>""", unsafe_allow_html=True)

                # Line chart
                st.markdown("<br>", unsafe_allow_html=True)
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=["Environment", "Social", "Governance", "Trust Score"],
                    y=[r1["environment_score"], r1["social_score"], r1["governance_score"], t1],
                    mode="lines+markers+text",
                    name=r1["name"],
                    line=dict(color="#4A7DFF", width=3),
                    marker=dict(size=9, color="#4A7DFF"),
                    text=[str(r1["environment_score"]), str(r1["social_score"]),
                          str(r1["governance_score"]), str(t1)],
                    textposition="top center",
                    textfont=dict(color="#C8D8F8", size=11)
                ))
                fig.add_trace(go.Scatter(
                    x=["Environment", "Social", "Governance", "Trust Score"],
                    y=[r2["environment_score"], r2["social_score"], r2["governance_score"], t2],
                    mode="lines+markers+text",
                    name=r2["name"],
                    line=dict(color="#34D399", width=3),
                    marker=dict(size=9, color="#34D399"),
                    text=[str(r2["environment_score"]), str(r2["social_score"]),
                          str(r2["governance_score"]), str(t2)],
                    textposition="top center",
                    textfont=dict(color="#C8D8F8", size=11)
                ))
                fig.update_layout(
                    title=dict(text="ESG Score Comparison",
                               font=dict(color="#E8F0FE", size=13, family="DM Serif Display")),
                    xaxis=dict(color="#7B93C4", tickfont=dict(color="#C8D8F8", size=12), gridcolor="#1A2845"),
                    yaxis=dict(title="Score", color="#7B93C4",
                               tickfont=dict(color="#7B93C4", size=11), gridcolor="#1A2845"),
                    paper_bgcolor="#070C1A", plot_bgcolor="#070C1A",
                    font=dict(family="DM Sans", color="#C8D8F8"),
                    legend=dict(bgcolor="#0D1526", bordercolor="#1A2845",
                               borderwidth=1, font=dict(color="#C8D8F8", size=12)),
                    margin=dict(t=50, b=20, l=20, r=20),
                    height=380
                )



                st.plotly_chart(fig, width='stretch')




    st.markdown('</div>', unsafe_allow_html=True)


  
#sector and benchmarking
  
with tab2:

    st.markdown('<div class="search-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="search-title">Select a sector to explore all companies and benchmarks</div>',
                unsafe_allow_html=True)

    sector_list     = sorted(all_df["sector"].str.strip().unique().tolist())
    selected_sector = st.selectbox("CHOOSE SECTOR", options=sector_list,
                                   index=sector_list.index("Technology"))

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="results-wrap">', unsafe_allow_html=True)

    sector_df = all_df[all_df["sector"].str.strip() == selected_sector]\
                    .sort_values("trust_score", ascending=False)\
                    .reset_index(drop=True)

    if sector_df.empty:
        st.warning("No companies found for this sector.")
    else:
        total_cos = len(sector_df)
        avg_trust = round(sector_df["trust_score"].mean(), 1)
        top_trust = round(sector_df["trust_score"].iloc[0], 1)
        low_trust = round(sector_df["trust_score"].iloc[-1], 1)
        max_trust = sector_df["trust_score"].max()

        st.markdown(f"""
        <div class="sector-stats">
          <div class="sector-stat"><div class="n">{total_cos}</div><div class="l">Companies</div></div>
          <div class="sector-stat"><div class="n" style="color:#4A7DFF">{avg_trust}</div><div class="l">Avg Trust Score</div></div>
          <div class="sector-stat"><div class="n" style="color:#4ADE80">{top_trust}</div><div class="l">Highest Score</div></div>
          <div class="sector-stat"><div class="n" style="color:#F87171">{low_trust}</div><div class="l">Lowest Score</div></div>
        </div>
        <div class="avg-line">
          <span class="avg-label">📊 Sector Benchmark — {selected_sector} Average Trust Score</span>
          <span class="avg-value">{avg_trust} / 100</span>
        </div>
        """, unsafe_allow_html=True)

        rows_html = ""
        for i, row in sector_df.iterrows():
            rank    = i + 1
            pct     = round(row["trust_score"] / max_trust * 100)
            above   = round(row["trust_score"] - avg_trust, 1)
            sign    = "+" if above >= 0 else ""
            diff_cl = "diff-pos" if above >= 0 else "diff-neg"
            if rank == 1:   num_cls = "rank-num gold"
            elif rank == 2: num_cls = "rank-num silver"
            elif rank == 3: num_cls = "rank-num bronze"
            else:           num_cls = "rank-num"
            bar_color = "#4ADE80" if row["trust_score"] >= avg_trust else "#F87171"
            rows_html += f"""
            <div class="rank-row">
              <span class="{num_cls}">#{rank}</span>
              <span class="rank-name">{row['name']}</span>
              <div class="rank-bar-track">
                <div class="rank-bar-fill" style="width:{pct}%;background:{bar_color}"></div>
              </div>
              <span class="metric-value" style="min-width:100px;text-align:right;font-size:.8rem">
                <span class="{diff_cl}">{sign}{above}</span> vs avg
              </span>
              <span class="rank-score">{row['trust_score']}</span>
            </div>"""

        st.markdown(f'<div style="background:#070C1A;border-radius:12px">{rows_html}</div>',
                    unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        top15      = sector_df.head(15)
        bar_colors = ["#4A7DFF" if s >= avg_trust else "#F87171" for s in top15["trust_score"]]

        fig2 = go.Figure(go.Bar(
            x=top15["trust_score"], y=top15["name"], orientation="h",
            marker_color=bar_colors,
            text=[f"{s}" for s in top15["trust_score"]],
            textposition="outside",
            textfont=dict(color="#C8D8F8", size=11)
        ))
        fig2.add_vline(x=avg_trust, line_dash="dash", line_color="#FBBF24", line_width=1.5,
                       annotation_text=f"Sector avg {avg_trust}",
                       annotation_font_color="#FBBF24", annotation_font_size=11)
        fig2.update_layout(
            title=dict(text=f"Top {min(15, total_cos)} Companies — {selected_sector}",
                       font=dict(color="#E8F0FE", size=14, family="DM Serif Display")),
            xaxis=dict(range=[0, 105], color="#5A7099", gridcolor="#1A2845",
                       tickfont=dict(color="#7B93C4")),
            yaxis=dict(autorange="reversed", color="#C8D8F8",
                       tickfont=dict(color="#C8D8F8", size=11)),
            paper_bgcolor="#070C1A", plot_bgcolor="#070C1A",
            font=dict(family="DM Sans", color="#C8D8F8"),
            margin=dict(l=20, r=60, t=50, b=20),
            height=max(350, min(15, total_cos) * 38)
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)


  
#Footer

  
st.markdown("""
<div class="site-footer">
  <div class="footer-left">
    <div class="footer-logo">🌱 ESG Trust Score</div>
    <div class="footer-copy">© 2025 ESG Intelligence Platform · Built with Streamlit & RandomForest</div>
  </div>
  <div class="footer-right">
    <div>
      <div class="footer-col-title">Data</div>
      <div class="footer-col-item">722 Global Companies</div>
      <div class="footer-col-item">47 Industry Sectors</div>
      <div class="footer-col-item">NYSE · NASDAQ</div>
    </div>
    <div>
      <div class="footer-col-title">Model</div>
      <div class="footer-col-item">Random Forest Regressor</div>
      <div class="footer-col-item">R² Accuracy: 96.6%</div>
      <div class="footer-col-item">3 ESG Sub-scores</div>
    </div>
    <div>
      <div class="footer-col-title">Metrics</div>
      <div class="footer-col-item">Trust Score (0–100)</div>
      <div class="footer-col-item">Risk · Performance</div>
      <div class="footer-col-item">Sector Comparison</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
