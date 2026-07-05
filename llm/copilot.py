"""Streamlit UI for the Risk Copilot."""

from __future__ import annotations

import streamlit as st

from .client import chat_completion, get_configured_providers, get_provider_status
from .context import build_messages
from .prompts import QUICK_PROMPTS, RISK_COPILOT_SYSTEM


def render_sidebar_settings():
    """Provider status and setup hints in the sidebar."""
    st.markdown("**Risk Copilot (LLM)**")
    providers = get_configured_providers()
    if providers:
        st.success(f"Active: {providers[0].name}")
    else:
        st.warning("No API key set")

    with st.expander("LLM setup (free)", expanded=not providers):
        st.markdown(
            """
1. **Groq** (recommended): [console.groq.com](https://console.groq.com) → free API key
2. **Hugging Face**: [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
3. **Ollama** (local): `ollama pull llama3.1` — zero cost

Add to `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "gsk_..."
# HF_TOKEN = "hf_..."  # optional fallback
```
            """
        )
        for row in get_provider_status():
            icon = "✅" if row["status"] == "configured" else "⚪"
            if "local" in row["status"]:
                icon = "🖥️"
            st.caption(f"{icon} **{row['name']}** — {row['status']}")


def _init_chat_state():
    if "copilot_messages" not in st.session_state:
        st.session_state.copilot_messages = []
    if "copilot_provider" not in st.session_state:
        st.session_state.copilot_provider = "auto"


def _append_message(role: str, content: str, meta: str | None = None):
    st.session_state.copilot_messages.append({
        "role": role,
        "content": content,
        "meta": meta,
    })


def _run_prompt(user_text: str):
    messages = build_messages(
        st.session_state,
        user_text,
        RISK_COPILOT_SYSTEM,
    )
    preferred = None if st.session_state.copilot_provider == "auto" else st.session_state.copilot_provider

    with st.spinner("Generating grounded analysis..."):
        result = chat_completion(
            messages,
            temperature=0.4,
            preferred_provider=preferred,
        )

    if result["error"] and not result["content"]:
        _append_message("assistant", f"⚠️ {result['error']}")
        return

    meta = None
    if result["provider"]:
        meta = f"{result['provider']} · {result['model']}"
    _append_message("assistant", result["content"], meta=meta)


def render():
    """Main Risk Copilot tab."""
    _init_chat_state()

    st.header("🤖 Risk Copilot")
    st.markdown(
        """
Ask about your **current cocktail** (scenario mix), portfolio factor exposures,
transition risk, or how context modules compound with market shocks.

Grounded in Shocktail's live numbers — not generic ChatGPT advice.
        """
    )

    providers = get_configured_providers()
    if not providers:
        st.info(
            "Add a free **GROQ_API_KEY** in `.streamlit/secrets.toml` to enable the copilot. "
            "See sidebar for setup instructions."
        )

    provider_names = ["auto"] + [p.name for p in get_configured_providers()]
    st.session_state.copilot_provider = st.selectbox(
        "LLM provider",
        options=provider_names,
        index=0,
        help="Auto tries Groq → Hugging Face → Ollama in order.",
    )

    st.markdown("**Quick actions**")
    qcols = st.columns(4)
    quick_items = list(QUICK_PROMPTS.items())
    for i, (key, prompt_text) in enumerate(quick_items):
        label = key.replace("_", " ").title()
        if qcols[i % 4].button(label, key=f"quick_{key}"):
            _append_message("user", prompt_text)
            _run_prompt(prompt_text)
            st.rerun()

    for msg in st.session_state.copilot_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("meta"):
                st.caption(msg["meta"])

    if prompt := st.chat_input("Ask about scenarios, portfolio risk, or physical hazards..."):
        _append_message("user", prompt)
        _run_prompt(prompt)
        st.rerun()

    if st.session_state.copilot_messages and st.button("Clear chat"):
        st.session_state.copilot_messages = []
        st.rerun()

    with st.expander("Context the copilot sees", expanded=False):
        from .context import build_risk_context
        st.code(build_risk_context(st.session_state), language=None)