"""Streamlit UI for the Risk Copilot."""

from __future__ import annotations

import streamlit as st

from .client import chat_completion, get_configured_providers, get_provider_status
from .context import build_messages
from .prompts import QUICK_PROMPTS, RISK_COPILOT_SYSTEM


def render_sidebar_settings():
    st.markdown("**Risk Copilot (LLM)**")
    providers = get_configured_providers()
    if providers:
        st.success(f"Ready: {', '.join(p.name for p in providers)}")
    else:
        st.error("No API key — copilot disabled")

    with st.expander("Free LLM setup (pick ONE+)", expanded=not providers):
        st.markdown(
            """
**Works on Streamlit Cloud** — no Ollama needed.

| Provider | Free signup | Secret key |
|----------|-------------|------------|
| **Groq** ⭐ | [console.groq.com/keys](https://console.groq.com/keys) | `GROQ_API_KEY` |
| **Gemini** | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) | `GEMINI_API_KEY` |
| Hugging Face | [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) | `HF_TOKEN` |
| Together AI | [api.together.xyz](https://api.together.xyz/settings/api-keys) | `TOGETHER_API_KEY` |

Add to `.streamlit/secrets.toml` or **Streamlit Cloud → Settings → Secrets**:
```toml
GROQ_API_KEY = "gsk_..."
# GEMINI_API_KEY = "..."   # good free backup
```
            """
        )
        for row in get_provider_status():
            st.caption(f"**{row['name']}** — {row['status']}")


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
    messages = build_messages(st.session_state, user_text, RISK_COPILOT_SYSTEM)
    preferred = None if st.session_state.copilot_provider == "auto" else st.session_state.copilot_provider

    with st.spinner("Generating grounded analysis..."):
        result = chat_completion(messages, temperature=0.4, preferred_provider=preferred)

    if result["error"] and not result["content"]:
        _append_message("assistant", f"⚠️ {result['error']}")
        return

    meta = f"{result['provider']} · {result['model']}" if result["provider"] else None
    _append_message("assistant", result["content"], meta=meta)


def render():
    _init_chat_state()

    st.header("🤖 Risk Copilot")
    st.markdown(
        """
Ask about your **cocktail scenario**, **power/grid stress**, portfolio factors, or compound shocks.
Grounded in Shocktail's live numbers — not generic ChatGPT.
        """
    )

    providers = get_configured_providers()
    if not providers:
        st.warning(
            "⚠️ Add a free **GROQ_API_KEY** or **GEMINI_API_KEY** in Streamlit Secrets. "
            "See sidebar → Free LLM setup. Ollama does not work on Streamlit Cloud."
        )

    provider_names = ["auto"] + [p.name for p in get_configured_providers()]
    st.session_state.copilot_provider = st.selectbox(
        "LLM provider",
        options=provider_names,
        index=0,
        help="Auto: Groq → Gemini → Hugging Face → Together (first key that works).",
    )

    st.markdown("**Quick actions**")
    qcols = st.columns(4)
    for i, (key, prompt_text) in enumerate(QUICK_PROMPTS.items()):
        if qcols[i % 4].button(key.replace("_", " ").title(), key=f"quick_{key}"):
            _append_message("user", prompt_text)
            _run_prompt(prompt_text)
            st.rerun()

    for msg in st.session_state.copilot_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("meta"):
                st.caption(msg["meta"])

    if prompt := st.chat_input("Ask about scenarios, power grid, portfolio risk..."):
        _append_message("user", prompt)
        _run_prompt(prompt)
        st.rerun()

    if st.session_state.copilot_messages and st.button("Clear chat"):
        st.session_state.copilot_messages = []
        st.rerun()

    with st.expander("Context the copilot sees", expanded=False):
        from .context import build_risk_context
        st.code(build_risk_context(st.session_state), language=None)