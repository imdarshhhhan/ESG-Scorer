"""
ESG Trust Score Predictor  — Streamlit Frontend
Run: python -m streamlit run App.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="ESG Trust Score",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600&display=swap');

/* ── Reset Streamlit defaults ── */
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
#root > div:first-child { background: #070C1A; }
.main  { background: #070C1A !important; }

/* Remove ALL default padding/margin */
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}
section[data-testid="stSidebar"] { display: none; }
div[data-testid="collapsedControl"] { display: none; }
header[data-testid="stHeader"] { background: transparent !important; height: 0 !important; }
footer { display: none !important; }

/* ── HEADER ── */
.site-header {
    background: linear-gradient(180deg, #0D1526 0%, #070C1A 100%);
    border-bottom: 1px solid #1A2845;
    padding: 0 4rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 64px;
    position: sticky;
    top: 0;
    z-index: 999;
}
.header-logo {
    display: flex;
    align-items: center;
    gap: 10px;
}
.logo-dot {
    width: 32px; height: 32px;
    background: linear-gradient(135deg, #4A7DFF, #34D399);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px;
}
.logo-text {
    font-family: 'DM Serif Display', serif;
    font-size: 1.25rem;
    color: #E8F0FE;
    letter-spacing: .01em;
}
.header-nav {
    display: flex; gap: 2rem; align-items: center;
}
.nav-link {
    font-size: .82rem;
    color: #7B93C4;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: .08em;
    text-decoration: none;
}
.header-badge {
    background: #0D2040;
    border: 1px solid #4A7DFF44;
    color: #60A5FA;
    font-size: .72rem;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 20px;
    letter-spacing: .06em;
}

/* ── HERO ── */
.hero-wrap {
    background: radial-gradient(ellipse 80% 60% at 50% -10%, #0D2040 0%, #070C1A 70%);
    padding: 4rem 4rem 3rem;
    text-align: center;
    border-bottom: 1px solid #1A2845;
}
.hero-tag {
    display: inline-block;
    background: #0D2040;
    border: 1px solid #4A7DFF44;
    color: #60A5FA;
    font-size: .72rem;
    font-weight: 600;
    padding: 5px 16px;
    border-radius: 20px;
    letter-spacing: .1em;
    margin-bottom: 1.2rem;
    text-transform: uppercase;
}
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 3.4rem;
    color: #E8F0FE;
    line-height: 1.1;
    margin-bottom: .75rem;
}
.hero-title span { color: #4A7DFF; }
.hero-sub {
    font-size: 1rem;
    color: #7B93C4;
    max-width: 520px;
    margin: 0 auto 2.5rem;
    line-height: 1.6;
}
.hero-stats {
    display: flex;
    justify-content: center;
    gap: 3rem;
    margin-top: 2rem;
    padding-top: 2rem;
    border-top: 1px solid #1A2845;
}
.stat-item { text-align: center; }
.stat-num {
    font-family: 'DM Serif Display', serif;
    font-size: 1.8rem;
    color: #E8F0FE;
}
.stat-lbl { font-size: .75rem; color: #7B93C4; text-transform: uppercase; letter-spacing: .08em; margin-top: 2px; }

/* ── SEARCH SECTION ── */
.search-wrap {
    padding: 2.5rem 4rem;
    background: #070C1A;
}
.search-title {
    font-size: .78rem;
    color: #7B93C4;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: .1em;
    margin-bottom: 1.2rem;
    text-align: center;
}

/* Streamlit selectbox styling */
.stSelectbox > div > div {
    background: #0D1526 !important;
    border: 1.5px solid #1A2845 !important;
    border-radius: 10px !important;
    color: #E8F0FE !important;
}
.stSelectbox > div > div:focus-within {
    border-color: #4A7DFF !important;
    box-shadow: 0 0 0 3px rgba(74,125,255,.12) !important;
}
.stSelectbox label {
    color: #7B93C4 !important;
    font-size: .78rem !important;
    font-weight: 600 !important;
    letter-spacing: .08em !important;
    text-transform: uppercase !important;
}

/* Button */
.stButton > button {
    background: linear-gradient(135deg, #4A7DFF, #2E5BCC) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: .72rem 2rem !important;
    font-size: .95rem !important;
    font-weight: 600 !important;
    font-family: 'DM Sans', sans-serif !important;
    width: 100% !important;
    letter-spacing: .03em;
    transition: all .2s !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px rgba(74,125,255,.35) !important;
}

/* ── RESULTS SECTION ── */
.results-wrap {
    padding: 0 4rem 3rem;
    background: #070C1A;
}

/* Company card */
.company-card {
    background: #0D1526;
    border: 1px solid #1A2845;
    border-radius: 16px;
    padding: 1.6rem;
}
.card-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-bottom: 1.4rem;
    padding-bottom: 1.1rem;
    border-bottom: 1px solid #1A2845;
}
.company-name {
    font-family: 'DM Serif Display', serif;
    font-size: 1.3rem;
    color: #E8F0FE;
    line-height: 1.25;
    max-width: 68%;
}
.trust-badge { text-align: right; }
.trust-label {
    font-size: .65rem; color: #7B93C4;
    text-transform: uppercase; letter-spacing: .1em; margin-bottom: 2px;
}
.trust-value {
    font-family: 'DM Serif Display', serif;
    font-size: 2.1rem; color: #4A7DFF; line-height: 1;
}

/* Metric rows */
.metric-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: .5rem 0; border-bottom: 1px solid #111D33;
}
.metric-row:last-child { border-bottom: none; }
.metric-label {
    font-size: .76rem; color: #5A7099; font-weight: 500;
    text-transform: uppercase; letter-spacing: .06em;
}
.metric-value { font-size: .9rem; color: #C8D8F8; font-weight: 500; text-align: right; }

/* Tags */
.tag { display:inline-block; font-size:.7rem; font-weight:600; padding:3px 10px; border-radius:20px; letter-spacing:.05em; }
.tag-low    { background:#0A2D1A; color:#4ADE80; border:1px solid #1A5530; }
.tag-medium { background:#2A1E00; color:#FBBF24; border:1px solid #4A3800; }
.tag-high   { background:#2A0A0A; color:#F87171; border:1px solid #4A1515; }
.tag-excel  { background:#0A1D3A; color:#60A5FA; border:1px solid #1A3560; }
.tag-good   { background:#0A2A1E; color:#34D399; border:1px solid #1A4A35; }
.tag-avg    { background:#2A2A0A; color:#FCD34D; border:1px solid #4A4A18; }
.tag-poor   { background:#2A1000; color:#FB923C; border:1px solid #4A2000; }
.tag-mkt    { background:#160D3A; color:#A78BFA; border:1px solid #2A1A60; }

/* Score bars */
.score-bar-wrap { margin: .25rem 0 .75rem; }
.score-bar-label { display:flex; justify-content:space-between; font-size:.75rem; color:#5A7099; margin-bottom:5px; }
.score-bar-track { background:#111D33; border-radius:6px; height:7px; overflow:hidden; }
.score-bar-fill  { height:100%; border-radius:6px; }

.diff-pos { color:#4ADE80; font-weight:500; }
.diff-neg { color:#F87171; font-weight:500; }

.section-label {
    font-size:.68rem; color:#4A7DFF; font-weight:700;
    text-transform:uppercase; letter-spacing:.12em; margin:1.1rem 0 .5rem;
}

/* Winner banner */
.winner-banner {
    background: linear-gradient(135deg, #0A1830 0%, #070C1A 100%);
    border: 1px solid #4A7DFF33;
    border-radius: 14px;
    padding: 1.25rem 2rem;
    text-align: center;
    margin: 1.5rem 0;
}
.winner-text {
    font-family: 'DM Serif Display', serif;
    font-size: 1.15rem; color: #E8F0FE;
}
.winner-highlight { color: #4A7DFF; }

/* ── FOOTER ── */
.site-footer {
    background: #0D1526;
    border-top: 1px solid #1A2845;
    padding: 2.5rem 4rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem;
}
.footer-left { }
.footer-logo {
    font-family: 'DM Serif Display', serif;
    font-size: 1.1rem; color: #E8F0FE; margin-bottom: .3rem;
}
.footer-copy { font-size: .78rem; color: #5A7099; }
.footer-right {
    display: flex; gap: 2rem;
}
.footer-col-title {
    font-size: .68rem; color: #4A7DFF; font-weight: 700;
    text-transform: uppercase; letter-spacing: .1em; margin-bottom: .5rem;
}
.footer-col-item { font-size: .78rem; color: #7B93C4; margin-bottom: .2rem; }

/* Streamlit misc overrides */
.stAlert { background:#0D1526 !important; border-color:#1A2845 !important; color:#C8D8F8 !important; border-radius:10px !important; }
div[data-testid="stVerticalBlock"] { gap:0 !important; }
div[data-testid="column"] { padding: 0 0.5rem !important; }
</style>
""", unsafe_allow_html=True)


# ── Load data & model ────────────────────────────────────────
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


# ── Helpers ──────────────────────────────────────────────────
def predict_trust(env, soc, gov):
    pred  = model.predict([[env, soc, gov]])[0]
    trust = round((pred - 600) / (1536 - 600) * 100, 1)
    return max(0.0, min(100.0, trust))

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
    </div>"""


# ════════════════════════════════════════════════════════════
#  HEADER
# ════════════════════════════════════════════════════════════
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


# ════════════════════════════════════════════════════════════
#  HERO
# ════════════════════════════════════════════════════════════
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
    <div class="stat-item"><div class="stat-num">99.5%</div><div class="stat-lbl">Model Accuracy</div></div>
  </div>
</div>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
#  SEARCH  —  selectbox with live type-to-filter
# ════════════════════════════════════════════════════════════
st.markdown('<div class="search-wrap">', unsafe_allow_html=True)
st.markdown('<div class="search-title">Select two companies to compare</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([5, 5, 2])
with c1:
    company1 = st.selectbox("COMPANY ONE", options=[""] + company_list,
                            format_func=lambda x: "Search company name..." if x == "" else x,
                            index=0)
with c2:
    company2 = st.selectbox("COMPANY TWO", options=[""] + company_list,
                            format_func=lambda x: "Search company name..." if x == "" else x,
                            index=0)
with c3:
    st.markdown("<br><br>", unsafe_allow_html=True)
    compare_btn = st.button("Compare →")

st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
#  RESULTS
# ════════════════════════════════════════════════════════════
st.markdown('<div class="results-wrap">', unsafe_allow_html=True)

if compare_btn:
    if not company1 or not company2:
        st.warning("Please select both companies before comparing.")
    elif company1 == company2:
        st.warning("Please select two different companies.")
    else:
        r1 = get_company(company1)
        r2 = get_company(company2)

        if r1 is not None and r2 is not None:
            t1 = predict_trust(r1["environment_score"], r1["social_score"], r1["governance_score"])
            t2 = predict_trust(r2["environment_score"], r2["social_score"], r2["governance_score"])

            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2 = st.columns(2, gap="large")
            with col1:
                st.markdown(render_card(r1, t1), unsafe_allow_html=True)
            with col2:
                st.markdown(render_card(r2, t2), unsafe_allow_html=True)

            # Winner banner
            if t1 != t2:
                winner = r1["name"] if t1 > t2 else r2["name"]
                loser  = r2["name"] if t1 > t2 else r1["name"]
                wt, lt = max(t1,t2), min(t1,t2)
                st.markdown(f"""
                <div class="winner-banner">
                  <div class="winner-text">
                    <span class="winner-highlight">{winner}</span> leads with a Trust Score of
                    <span class="winner-highlight">{wt}</span> —
                    {round(wt-lt,1)} points ahead of {loser} ({lt})
                  </div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="winner-banner">
                  <div class="winner-text">Both companies are <span class="winner-highlight">tied</span> on Trust Score!</div>
                </div>""", unsafe_allow_html=True)

            # Radar chart
            st.markdown("<br>", unsafe_allow_html=True)
            cats = ["Environment", "Social", "Governance", "Trust Score", "Total ESG"]

            def norm(v, mn, mx): return round((v - mn) / (mx - mn) * 100, 1)

            v1 = [norm(r1["environment_score"],200,719), norm(r1["social_score"],160,667),
                  norm(r1["governance_score"],75,475),   t1,
                  norm(r1["total_esg_score"],600,1536)]
            v2 = [norm(r2["environment_score"],200,719), norm(r2["social_score"],160,667),
                  norm(r2["governance_score"],75,475),   t2,
                  norm(r2["total_esg_score"],600,1536)]

            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=v1+[v1[0]], theta=cats+[cats[0]], fill='toself',
                fillcolor='rgba(74,125,255,0.15)',
                line=dict(color='#4A7DFF', width=2), name=r1["name"]))
            fig.add_trace(go.Scatterpolar(
                r=v2+[v2[0]], theta=cats+[cats[0]], fill='toself',
                fillcolor='rgba(52,211,153,0.12)',
                line=dict(color='#34D399', width=2), name=r2["name"]))
            fig.update_layout(
                polar=dict(
                    bgcolor='#0D1526',
                    radialaxis=dict(visible=True, range=[0,100], color='#3A5080',
                                   gridcolor='#1A2845', tickfont=dict(color='#7B93C4', size=10)),
                    angularaxis=dict(color='#7B93C4', gridcolor='#1A2845',
                                    tickfont=dict(color='#C8D8F8', size=12))),
                paper_bgcolor='#070C1A', plot_bgcolor='#070C1A',
                font=dict(family='DM Sans', color='#C8D8F8'),
                legend=dict(bgcolor='#0D1526', bordercolor='#1A2845', borderwidth=1,
                           font=dict(color='#C8D8F8', size=12)),
                margin=dict(t=30, b=20), height=440)
            st.plotly_chart(fig, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
#  FOOTER
# ════════════════════════════════════════════════════════════
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
      <div class="footer-col-item">R² Accuracy: 99.5%</div>
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
