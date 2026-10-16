import os
import re
from datetime import datetime

import streamlit as st
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_groq import ChatGroq

st.set_page_config(page_title="Groq Agent", page_icon="🤖")
st.title("🤖 Groq LangChain Agent")

SYSTEM_PROMPT = """You are a helpful assistant. Use tools when they help.

Formatting rules (your output is rendered with Streamlit markdown):
- Use Markdown: headings (##), **bold**, bullet lists, and tables where useful.
- For math or chemistry formulas, use LaTeX with $...$ for inline and $$...$$ for display blocks.
- Never use \\( \\), \\[ \\], or the \\ce{} command. Write chemistry like $\\text{Fe}^{2+} + 2e^- \\rightarrow \\text{Fe}$.
- Put code in fenced code blocks with a language tag.
- Reply in the same language as the user."""


def fix_latex(text: str) -> str:
    """Convert \\[ \\] and \\( \\) to the $$ / $ style Streamlit renders."""
    text = re.sub(
        r"\\\[(.+?)\\\]",
        lambda m: f"\n$$\n{m.group(1).strip()}\n$$\n",
        text,
        flags=re.S,
    )
    text = re.sub(
        r"\\\((.+?)\\\)",
        lambda m: f"${m.group(1).strip()}$",
        text,
        flags=re.S,
    )
    return text


def to_text(content) -> str:
    """Some models return a list of content blocks instead of a string."""
    if isinstance(content, list):
        return "".join(
            b.get("text", "") if isinstance(b, dict) else str(b) for b in content
        )
    return str(content)


@tool
def get_current_time() -> str:
    """Return the current date and time."""
    return datetime.now().strftime("%A, %d %B %Y, %H:%M:%S")


@tool
def calculator(expression: str) -> str:
    """Evaluate a math expression, e.g. '23 * (4 + 5)'."""
    allowed = set("0123456789+-*/(). %")
    if not set(expression) <= allowed:
        return "Invalid expression."
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as e:
        return f"Error: {e}"


with st.sidebar:
    st.header("Settings")
    api_key = st.text_input(
        "Groq API key",
        value=os.environ.get("GROQ_API_KEY", ""),
        type="password",
    )
    model = st.selectbox(
        "Model",
        ["openai/gpt-oss-120b", "llama-3.1-8b-instant"],
    )
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()


@st.cache_resource
def build_agent(api_key: str, model: str):
    llm = ChatGroq(model=model, temperature=0, api_key=api_key)
    return create_agent(
        model=llm,
        tools=[get_current_time, calculator],
        system_prompt=SYSTEM_PROMPT,
    )


if "messages" not in st.session_state:
    st.session_state.messages = []

for role, content in st.session_state.messages:
    with st.chat_message(role):
        st.markdown(content)

if prompt := st.chat_input("Ask something..."):
    if not api_key:
        st.error("Enter your Groq API key in the sidebar.")
        st.stop()

    st.session_state.messages.append(("user", prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                agent = build_agent(api_key, model)
                response = agent.invoke({"messages": st.session_state.messages})
                answer = fix_latex(to_text(response["messages"][-1].content))
            except Exception as e:
                answer = f"Error: {e}"
        st.markdown(answer)
        

    st.session_state.messages.append(("assistant", answer))