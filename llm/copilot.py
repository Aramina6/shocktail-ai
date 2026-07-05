"""Research Copilot — grounded AI narratives for market intelligence."""

from __future__ import annotations

import streamlit as st

from .client import chat_completion, get_configured_providers, get_provider_status
from .context import build_messages
from .prompts import QUICK_PROMPTS, RISK_COPILOT_SYSTEM


def render_sidebar_settings():
    providers = get_configured_providers()
    if providers:
        st.success(f"Engine online · {providers[0].name}")
    else:
        st.error("AI engine offline — add API key")

    with st.expander("Configure AI engine", expanded=not providers):
        st.caption("Free hosted providers (Streamlit Cloud compatible)")
        for row in get_provider_status():
            if row["name"] != "ollama":
                st.caption(f"**{row['name']}** — {row['status']}")


def _init_chat_state():
    if "copilot_messages" not in st.session_state:
        st.session_state.copilot_messages = []
    if "copilot_provider" not in st.session_state:
        st.session_state.copilot_provider = "auto"


def _append_message(role: str, content: str, meta: str | None = None):
    st.session_state.copilot_messages.append({
        "role": role, "content": content, "meta": meta,
    })


def _run_prompt(user_text: str):
    messages = build_messages(st.session_state, user_text, RISK_COPILOT_SYSTEM)
    preferred = None if st.session_state.copilot_provider == "auto" else st.session_state.copilot_provider

    with st.spinner("Generating research narrative..."):
        result = chat_completion(messages, temperature=0.35, preferred_provider=preferred)

    if result["error"] and not result["content"]:
        _append_message("assistant", f"⚠️ {result['error']}")
        return

    meta = f"{result['provider']} · {result['model']}" if result["provider"] else None
    _append_message("assistant", result["content"], meta=meta)


def render():
    _init_chat_state()

    st.markdown('<div class="st-section-label">Research Copilot</div>', unsafe_allow_html=True)
    st.markdown(
        """
Ask research questions about your **active scenario**, **factor exposures**, or **alternative data signals**.
Every answer is grounded in Shocktail's live quantitative context.
        """
    )

    if not get_configured_providers():
        st.warning("Configure **GROQ_API_KEY** in Streamlit Secrets to enable Research Copilot.")

    provider_names = ["auto"] + [p.name for p in get_configured_providers()]
    st.session_state.copilot_provider = st.selectbox(
        "Inference provider",
        options=provider_names,
        index=0,
    )

    st.markdown("**Research templates**")
    labels = {
        "executive_summary": "Executive Summary",
        "sector_memo": "Sector Memo",
        "alt_data_brief": "Alt Data Brief",
        "ic_briefing": "IC Briefing",
        "risk_actions": "Risk Actions",
    }
    cols = st.columns(5)
    for i, (key, prompt_text) in enumerate(QUICK_PROMPTS.items()):
        if cols[i].button(labels.get(key, key), key=f"quick_{key}"):
            _append_message("user", prompt_text)
            _run_prompt(prompt_text)
            st.rerun()

    for msg in st.session_state.copilot_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("meta"):
                st.caption(msg["meta"])

    if prompt := st.chat_input("Research question — scenarios, sectors, risk, alt data..."):
        _append_message("user", prompt)
        _run_prompt(prompt)
        st.rerun()

    if st.session_state.copilot_messages and st.button("Clear session"):
        st.session_state.copilot_messages = []
        st.rerun()

    with st.expander("Source context (grounding data)", expanded=False):
        from .context import build_risk_context
        st.code(build_risk_context(st.session_state), language=None)