# AI Account Health Copilot

## What this project is
A portfolio project that shows how a **Strategic Customer Success Manager (CSM)** at an enterprise AI platform could use AI to manage a book of business. It is built to show to hiring managers for Strategic CS roles at AI companies.

**The scenario:** I am a Strategic CSM with about **70 accounts**:
- About half are **AI startups** and half are **banks and asset managers** (financial services).
- Contracts are **seat-based**, **usage-based**, or **mixed** (both).

The app should help me see which accounts are healthy, which are at risk, and what to do next. It uses account data, AI-written summaries (Anthropic API), and recent public news about each account (Exa API).

## Tech stack
- **Python**: the programming language
- **pandas**: reads and works with the account data in tables
- **Streamlit**: turns the Python script into a simple web app
- **Anthropic API (Claude)**: writes account summaries, risk explanations and suggested next steps
- **Exa API**: searches the web for recent news about each account

## Who I am and how to work with me
- **I don't code.** After every change, explain in plain English what you changed, why, and how I can check that it works. Avoid jargon. If you must use a technical term, define it in one short sentence.
- **Keep the code simple.** Choose the most readable option over the cleverest one. Use few files, clear names and short comments that say what each part does. Don't add libraries, frameworks or abstractions unless they're really needed, and tell me first.
- **Work in small steps.** Each step should leave the app working. Tell me how to run it and what I should see.
- **Commit to GitHub after each working step.** Use a short, plain commit message that describes the change. Never commit something that's broken.
- Ask me before making big decisions, such as a new library, a change in data structure or a change in how scoring works.

## Secrets and API keys (very important)
- API keys live **only** in:
  - `.env` locally (the Anthropic and Exa keys, e.g. `ANTHROPIC_API_KEY=...`, `EXA_API_KEY=...`)
  - **Streamlit secrets** when the app is deployed (`.streamlit/secrets.toml` locally or the Streamlit Cloud settings)
- **Never** write a key into code, comments, commit messages, README files or chat output.
- `.env` and `.streamlit/secrets.toml` must stay in `.gitignore`. Before every commit, check that no key is being committed.
- The code should read keys from Streamlit secrets first, then from `.env`, and should show a friendly error message if a key is missing.

## Data
- Use **made-up (synthetic) account data** only. No real customer data. Company names should be invented, or clearly labelled as fictional.
- The account data should reflect the scenario: about 70 accounts, a mix of AI startups and financial services, and seat, usage and mixed contracts. It should include signals a CSM would care about: seat use, usage trends, renewal dates, ARR, support tickets, executive sponsor and so on.
- Real public news from Exa may only be used for real, public companies when that makes sense. Keep it clearly separate from the made-up account data.

## Running the app
- Python **3.14** (installed from python.org at `/usr/local/bin/python3.14`). The Mac's built-in Python 3.9 is too old. Don't use it.
- Add-ons live in a project environment called `.venv`, which is excluded from git. Always run things with `.venv/bin/python`.

First-time setup (or to rebuild):
```
/usr/local/bin/python3.14 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Test the Claude connection:
```
.venv/bin/python test_claude.py
```

Run the app (once it exists):
```
.venv/bin/streamlit run app.py
```
(Update this section if the file names change.)
