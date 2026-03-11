import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tools.scam_detector import scam_detector
from tools.medicine_checker import medicine_checker
from tools.fake_news import fake_news
from tools.summarizer import summarizer, text_classifier

st.set_page_config(
    page_title="SmartAI Hub",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

:root {
    --bg-primary:#0a0e1a;
    --bg-secondary:#111827;
    --bg-card:#161d2e;
    --accent-cyan:#00d4ff;
    --accent-purple:#7c3aed;
    --accent-green:#10b981;
    --accent-orange:#f59e0b;
    --accent-red:#ef4444;
    --text-primary:#f1f5f9;
    --text-secondary:#94a3b8;
    --border:rgba(255,255,255,0.08);
}

html, body, .stApp {
    background-color:var(--bg-primary)!important;
    font-family:'Space Grotesk',sans-serif!important;
    color:var(--text-primary)!important;
}

.stApp::before {
    content:'';
    position:fixed;
    top:0;left:0;right:0;bottom:0;
    background-image:
    linear-gradient(rgba(0,212,255,0.03)1px,transparent 1px),
    linear-gradient(90deg,rgba(0,212,255,0.03)1px,transparent 1px);
    background-size:40px 40px;
    pointer-events:none;
}

[data-testid="stSidebar"]{
background:linear-gradient(180deg,#0d1321 0%,#111827 100%)!important;
border-right:1px solid var(--border)!important;
}

.main-title{
font-size:2.6rem;
font-weight:700;
background:linear-gradient(135deg,var(--accent-cyan),var(--accent-purple));
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
margin-bottom:0.3rem;
}

.main-subtitle{
color:var(--text-secondary);
font-size:1.05rem;
margin-bottom:2rem;
}

.tool-header{
display:flex;
gap:1rem;
padding:1.5rem;
background:linear-gradient(135deg,rgba(0,212,255,0.05),rgba(124,58,237,0.05));
border:1px solid rgba(0,212,255,0.15);
border-radius:16px;
margin-bottom:1.5rem;
}

.tool-icon{
font-size:2.4rem;
}

.sidebar-logo{
text-align:center;
padding:1.5rem 1rem 1rem;
border-bottom:1px solid var(--border);
margin-bottom:1rem;
}

.logo-text{
font-size:1.6rem;
font-weight:700;
background:linear-gradient(135deg,var(--accent-cyan),var(--accent-purple));
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
}

.logo-sub{
font-size:0.75rem;
color:var(--text-secondary);
letter-spacing:2px;
text-transform:uppercase;
}

.result-card{
padding:1.2rem 1.5rem;
border-radius:12px;
margin:1rem 0;
border-left:4px solid;
}

.result-safe{
background:rgba(16,185,129,0.08);
border-left-color:var(--accent-green);
}

.result-warning{
background:rgba(245,158,11,0.08);
border-left-color:var(--accent-orange);
}

.result-danger{
background:rgba(239,68,68,0.08);
border-left-color:var(--accent-red);
}

#MainMenu,footer,header{visibility:hidden;}
.block-container{padding-top:1.5rem!important;}
</style>
""", unsafe_allow_html=True)

with st.sidebar:

    st.markdown("""
    <div class="sidebar-logo">
        <div class="logo-text">🤖 SmartAI</div>
        <div class="logo-sub">AI Toolkit</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🛠️ Choose Tool")

    tools={
        "🔐 Scam Detector":"Detect phishing or fraud messages",
        "💊 Medicine Checker":"Drug safety and side effects",
        "📰 Fake News Analyzer":"Verify news claims",
        "📚 Study Assistant":"Summaries and learning help",
        "🏷️ Text Classifier":"Sentiment and intent detection"
    }

    selected_tool=st.radio(
        "tool_selector",
        list(tools.keys()),
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.markdown("""
<div style="color:#64748b;font-size:0.8rem;padding:0.5rem 0;">
<strong style="color:#94a3b8;">AI Engine</strong><br>
Llama 3.1 via Groq<br><br>
<span style="color:#475569;">
Smart tools for everyday problems.<br>
Cybersecurity • Health • Learning
</span>
</div>
""", unsafe_allow_html=True)

col_title,col_stats=st.columns([2,1])

with col_title:
    st.markdown('<div class="main-title">SmartAI Hub</div>',unsafe_allow_html=True)
    st.markdown(
        '<div class="main-subtitle">AI powered tools for everyday problem solving like security, health, learning and media awareness.</div>',
        unsafe_allow_html=True
    )

with col_stats:
    st.markdown("""
<div style="display:flex;gap:0.6rem;padding-top:0.5rem;">
<div style="background:#161d2e;border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:0.8rem;text-align:center;flex:1;">
<div style="font-size:1.5rem;font-weight:700;color:#00d4ff;">5</div>
<div style="font-size:0.7rem;color:#64748b;text-transform:uppercase;">AI Tools</div>
</div>
<div style="background:#161d2e;border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:0.8rem;text-align:center;flex:1;">
<div style="font-size:1.5rem;font-weight:700;color:#7c3aed;">∞</div>
<div style="font-size:0.7rem;color:#64748b;text-transform:uppercase;">Analyses</div>
</div>
<div style="background:#161d2e;border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:0.8rem;text-align:center;flex:1;">
<div style="font-size:1.5rem;font-weight:700;color:#10b981;">AI</div>
<div style="font-size:0.7rem;color:#64748b;text-transform:uppercase;">Powered</div>
</div>
</div>
""",unsafe_allow_html=True)

st.markdown("---")

if selected_tool=="🔐 Scam Detector":
    scam_detector()

elif selected_tool=="💊 Medicine Checker":
    medicine_checker()

elif selected_tool=="📰 Fake News Analyzer":
    fake_news()

elif selected_tool=="📚 Study Assistant":
    summarizer()

elif selected_tool=="🏷️ Text Classifier":
    text_classifier()