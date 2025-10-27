# FinancialHealthAdvisor Crew

A multi-agent financial assistant template built on CrewAI. This project demonstrates how to compose a small crew of agents (data reader, advisor, report writer) with custom tools, including a CSV analyzer and integrations for an LLM backend (Google Gemini). It's intended as a developer-friendly starting point for building automated financial workflows and reports.

Contents

- Overview
- Quickstart (setup & run)
- Configuration and environment variables
- Project layout
- Tools and LLM notes (CSV tool, visualization, Gemini LLM)
- Development: tests, running locally, debugging
- Troubleshooting
- Contributing & License

## Overview

This repository contains a CrewAI project named `financial_health_advisor`. The crew is composed of multiple agents defined in `src/financial_health_advisor/crew.py` and configured via YAML files under `src/financial_health_advisor/config/`.

Key features:

- Read and summarize customer transaction CSVs
- Produce visualizations (pie charts) of spending
- Use a customizable LLM backend (Google Gemini via a small wrapper)
- Simple, extensible tool architecture (CrewAI `@tool` functions)

## Quickstart

Prerequisites

- macOS / Linux / Windows with Python 3.10–3.13 installed
- git
- Optional: Google Gemini API key if you plan to use Gemini as the LLM

Setup

1. Clone the repo and cd into it:

```bash
git clone <your-repo-url> financial_health_advisor
cd financial_health_advisor
```

2. Create and activate the Python virtual environment (project includes `financialenv` example):

```bash
# Create venv (if not present)
python -m venv financialenv
source financialenv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

3. Environment variables

Create a `.env` file in the project root or export the variables directly. Minimum recommended variables:

```bash
export GEMINI_API_KEY="your_gemini_api_key"
export GEMINI_MODEL="models/gemini-pro-latest"  # optional: override default
```

Note: If `GEMINI_API_KEY` is not set, the project will not attempt to call Gemini at import time — the LLM will be left uninitialized and agents that call the LLM will raise at runtime.

4. Run the project

You can run the example entrypoint to assemble and kickoff the crew (this may perform network calls to Gemini if configured):

```bash
python src/financial_health_advisor/main.py
```

Alternatively, if you use the crewAI CLI (optional), from the project root:

```bash
crewai run
```

This will execute the configured tasks and create a report file (depending on `config/tasks.yaml`).

## Configuration & Project Layout

Top-level files and folders:

- `src/financial_health_advisor/` — package with the crew, agents, tools, and LLM wrapper
  - `crew.py` — defines the `FinancialHealthAdvisorCrew` class and registers agents/tasks
  - `main.py` — small runner to kickoff the crew with sample inputs
  - `llm/gemini_llm.py` — wrapper around the Google generative API (Gemini) so it matches CrewAI's LLM interface
  - `tools/` — tools used by agents
    - `simple_csv_tool.py` — decorated `@tool` function that summarizes CSVs
    - `visualize_spending_tool.py` — decorated `@tool` that saves a pie chart image
  - `config/agents.yaml` and `config/tasks.yaml` — agent and task definitions
- `data/` — example CSV data (e.g. `customer_transactions.csv`)
- `requirements.txt`, `pyproject.toml` — dependency manifests

Tips

- When running scripts during development, ensure `src` (or `src/financial_health_advisor`) is on `PYTHONPATH`. Example quick test uses `sys.path.insert(0, 'src/financial_health_advisor')`.

## Tools and LLM notes

CSV tool

- `simple_csv_search_tool` is defined in `src/financial_health_advisor/tools/simple_csv_tool.py` and decorated with `@tool` from CrewAI. The decorator returns a `Tool` object that CrewAI validates and accepts in an agent's `tools` list.
- Programmatic invocation (for debugging) can use the tool's underlying function via `csv_tool.func(file_path)` after importing the Crew module.

Visualization tool

- `visualize_spending_tool` reads a CSV and writes `spending_breakdown.png` into the working directory.

Gemini LLM wrapper

- `src/financial_health_advisor/llm/gemini_llm.py` adapts the Google Generative SDK to CrewAI's `BaseLLM` interface. It includes robust handling for different response shapes coming from the Gemini SDK (for example, `.text`, `.candidates`, and dict-like responses).
- The `safe_gemini_llm()` initializer in `crew.py` avoids making a blocking network call when `GEMINI_API_KEY` is not present; it will return `None` in that case so module import remains safe.

## Development & Tests

Run unit tests (recommended to add tests for tools and LLM wrapper). Example using pytest:

```bash
# from project root
source financialenv/bin/activate
pip install -r requirements.txt
pytest -q
```

Suggested tests to add:

- `tests/test_simple_csv_tool.py`: verify summary content for the provided example CSV and behavior when file is missing.
- `tests/test_gemini_llm.py`: mock the Gemini SDK responses and ensure `GeminiLLM.call()` and `generate_chat_response()` return strings correctly.

## Troubleshooting

Common issues and fixes

- pydantic validation error: "Input should be a valid dictionary or instance of BaseTool"

  - Cause: passing a plain object/class instance instead of a CrewAI `Tool` object. Fix: ensure the tool is decorated with `@tool` (see `simple_csv_tool.py`) or pass a `BaseTool` instance.

- Module import error: "No module named 'tools'"
  - Cause: running code with incorrect PYTHONPATH. Fix: run scripts with `src` or `src/financial_health_advisor` on `PYTHONPATH` or use package imports (e.g. `from financial_health_advisor.tools...`). Example:

```bash
python -c "import sys; sys.path.insert(0, 'src/financial_health_advisor'); import crew"
```

- Gemini-related errors or empty responses
  - Cause: missing or invalid `GEMINI_API_KEY`, or the SDK returning a response shape the wrapper didn't expect.
  - Fix: Ensure `GEMINI_API_KEY` is set. The wrapper includes robust extraction for `.text`, `.candidates`, and dict-like responses. If you still see errors, inspect the raw response or enable logging.

## Run examples

Quick interactive check of the CSV tool (Python REPL):

```bash
source financialenv/bin/activate
python - <<'PY'
import sys
sys.path.insert(0, 'src/financial_health_advisor')
import crew
print(crew.csv_tool.func('data/customer_transactions.csv'))
PY
```

Run the main runner (example):

```bash
python src/financial_health_advisor/main.py
```

If you want to run the crew fully through the CLI (`crewai`), first install the CLI and then run `crewai run` from the project root.

## Contributing

Contributions are welcome. Please follow these steps:

- Fork the repo
- Create a feature branch
- Add tests for new functionality
- Open a pull request with a clear description of changes

## License

This project is provided under the MIT License. Adjust as necessary for your organization.

## Contact & Support

If you need help integrating Google Gemini or debugging CrewAI validation errors, open an issue or reach out on the upstream CrewAI community channels listed in the original template.

---

If you'd like, I can also add unit tests for the CSV tool and a short `CONTRIBUTING.md` next. Tell me which to add and I'll create them.
