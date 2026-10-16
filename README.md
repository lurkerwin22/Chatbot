# 🤖 Groq LangChain Agent

A simple AI agent built with [LangChain](https://www.langchain.com/) and the [Groq](https://groq.com/) free API. It can call tools (current time, calculator) and comes with two interfaces: a terminal chat and a Streamlit web UI.

## Features

- Tool-calling agent powered by `openai/gpt-oss-120b` on Groq
- Built-in tools: current date/time and a safe calculator
- Terminal chat (`agent.py`) with optional conversation memory
- Streamlit chat UI (`app.py`) with model selector, API key field, and clear-chat button
- Markdown, tables, code blocks, and LaTeX math rendering in the UI
- Easy to extend with your own tools

## Requirements

- Python 3.10+
- A free Groq API key from [console.groq.com](https://console.groq.com/)

## Installation

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -U langchain langchain-groq streamlit
```

## Configuration

Set your Groq API key as an environment variable.

**Windows (PowerShell):**

```powershell
$env:GROQ_API_KEY="your_key_here"
```

**macOS / Linux:**

```bash
export GROQ_API_KEY="your_key_here"
```

For the Streamlit app you can also paste the key into the sidebar.

> Never commit your API key. If you use a `.env` file, add it to `.gitignore`.

## Usage

### Terminal version

```bash
python agent.py
```

Type a question and press Enter. Type `exit` to quit.

### Web UI (Streamlit)

```bash
python -m streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501).

## Project structure

```
.
├── agent.py     # Terminal chat agent
├── app.py       # Streamlit web UI
└── README.md
```

## Adding your own tools

Define a function with the `@tool` decorator and add it to the `tools` list:

```python
from langchain_core.tools import tool

@tool
def my_tool(text: str) -> str:
    """Describe what this tool does so the model knows when to use it."""
    return text.upper()
```

## Troubleshooting

| Problem | Fix |
|---|---|
| `model_not_found` (404) | Your key can't access that model. List available models with `Groq().models.list()` and use one that supports tool calling. |
| `ImportError` on `create_agent` | Upgrade LangChain: `pip install -U langchain` |
| Rate limit errors | The free tier has per-minute limits. Wait a few seconds and retry. |
| LaTeX shows as raw text | Restart the app. The prompt asks the model for `$...$` math, and `app.py` converts `\( \)` and `\[ \]` automatically. |
| `pip.exe` access denied (Windows) | Use `python -m pip install ...` instead. |

## Tech stack

- [LangChain](https://www.langchain.com/)
- [Groq](https://groq.com/)
- [Streamlit](https://streamlit.io/)

## License

MIT. See `LICENSE` for details.
