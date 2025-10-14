# Project Manager Risk Copilot — Step 1 (UI scaffold)

This is a minimal Streamlit app scaffold. It does **not** call any AI yet.
Purpose: get the page live on Streamlit Cloud, then add features step-by-step.

## Files
- `app.py` — Streamlit UI (language toggle EN/DE, textarea, stub button).
- `requirements.txt` — minimal dependency.

## Deploy (Streamlit Cloud)
1) Push these files to a new GitHub repo named `project-manager-risk-copilot`.
2) In Streamlit Community Cloud → **New app** → pick the repo → `app.py`.
3) (Optional) Set Python to 3.11 in app settings.
4) Deploy. You should see the title and the button; clicking shows a stub message.

Next step: we'll add the OpenAI-based risk engine with PII masking and a clean risk table (RAG).
