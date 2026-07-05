"""Enterprise market intelligence theme for Shocktail.ai."""

import streamlit as st


def inject_theme():
    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --st-bg: #0B1426;
    --st-surface: #131D33;
    --st-surface-2: #1A2744;
    --st-border: #2A3A5C;
    --st-text: #E8ECF4;
    --st-muted: #8B9BB8;
    --st-accent: #D4A853;
    --st-accent-2: #4A9EFF;
    --st-danger: #E85D5D;
    --st-success: #3DD68C;
}

.stApp {
    background: linear-gradient(180deg, #0B1426 0%, #0E1830 100%);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.block-container { padding-top: 1.2rem; max-width: 1280px; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0A1120;
    border-right: 1px solid var(--st-border);
}
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 { color: var(--st-text); }

/* Headers */
h1, h2, h3 { color: var(--st-text) !important; font-weight: 600 !important; }
p, label, .stMarkdown { color: var(--st-muted); }

/* Metrics */
[data-testid="stMetric"] {
    background: var(--st-surface);
    border: 1px solid var(--st-border);
    border-radius: 10px;
    padding: 12px 16px;
}
[data-testid="stMetricLabel"] { color: var(--st-muted) !important; font-size: 0.8rem !important; }
[data-testid="stMetricValue"] { color: var(--st-text) !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: transparent;
    border-bottom: 1px solid var(--st-border);
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: var(--st-muted);
    border-radius: 8px 8px 0 0;
    padding: 10px 20px;
    font-weight: 500;
}
.stTabs [aria-selected="true"] {
    background: var(--st-surface) !important;
    color: var(--st-accent) !important;
    border-bottom: 2px solid var(--st-accent);
}

/* Buttons */
.stButton > button {
    background: var(--st-surface-2);
    color: var(--st-text);
    border: 1px solid var(--st-border);
    border-radius: 8px;
    font-weight: 500;
}
.stButton > button:hover {
    border-color: var(--st-accent);
    color: var(--st-accent);
}

/* Primary feel for first button in row */
div[data-testid="column"]:first-child .stButton > button[kind="primary"],
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #C9983E 0%, #D4A853 100%);
    color: #0B1426;
    border: none;
    font-weight: 600;
}

/* Inputs */
.stSelectbox, .stTextInput, .stNumberInput, .stSlider {
    color: var(--st-text);
}

/* Info/success boxes */
.stAlert {
    border-radius: 10px;
    border: 1px solid var(--st-border);
}

/* Custom Shocktail components */
.st-hero {
    background: linear-gradient(135deg, #131D33 0%, #1A2744 100%);
    border: 1px solid var(--st-border);
    border-radius: 14px;
    padding: 28px 32px;
    margin-bottom: 24px;
}
.st-hero h1 {
    font-size: 2rem !important;
    margin: 0 0 4px 0 !important;
    background: linear-gradient(90deg, #E8ECF4, #D4A853);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.st-hero .tagline { color: var(--st-muted); font-size: 1.05rem; margin: 0 0 16px 0; }
.st-hero .positioning {
    color: var(--st-accent-2);
    font-size: 0.9rem;
    font-weight: 500;
    letter-spacing: 0.02em;
}

.st-stat-row {
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
    margin: 16px 0 8px 0;
}
.st-stat-pill {
    background: var(--st-surface);
    border: 1px solid var(--st-border);
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 0.82rem;
    color: var(--st-muted);
}
.st-stat-pill strong { color: var(--st-accent); }

.st-compare-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-top: 16px;
}
.st-compare-card {
    background: var(--st-surface);
    border: 1px solid var(--st-border);
    border-radius: 12px;
    padding: 20px;
}
.st-compare-card h4 {
    color: var(--st-text) !important;
    margin: 0 0 12px 0 !important;
    font-size: 1rem !important;
}
.st-compare-card ul { margin: 0; padding-left: 18px; color: var(--st-muted); font-size: 0.9rem; }
.st-compare-card li { margin-bottom: 6px; }
.st-compare-card.shocktail { border-color: var(--st-accent); }
.st-compare-card.shocktail h4 { color: var(--st-accent) !important; }

.st-section-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--st-accent);
    margin-bottom: 8px;
}

.st-footer {
    text-align: center;
    color: var(--st-muted);
    font-size: 0.78rem;
    padding: 24px 0 8px 0;
    border-top: 1px solid var(--st-border);
    margin-top: 32px;
}

/* Hide Streamlit branding */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
</style>
        """,
        unsafe_allow_html=True,
    )