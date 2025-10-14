import os
import streamlit as st
from openai import OpenAI

# ============================== Page & style ===============================
st.set_page_config(page_title="Project Manager Risk Copilot", layout="wide")
st.markdown("""
<style>
.stButton > button[kind="primary"]{
  padding: 12px 18px;
  font-size: 16px;
  font-weight: 700;
  border-radius: 10px;
}
.header-row { display:flex; align-items:center; justify-content:space-between; }
.header-lang { min-width: 220px; }
</style>
""", unsafe_allow_html=True)

# ============================== Language bootstrap =========================
def get_query_lang_default() -> str:
    try:
        lang = (st.query_params.get("lang") or "en").lower()
    except Exception:
        try:
            params = st.experimental_get_query_params()
            lang = (params.get("lang", ["en"])[0] or "en").lower()
        except Exception:
            lang = "en"
    return "de" if lang.startswith("de") else "en"

if "lang" not in st.session_state:
    st.session_state["lang"] = get_query_lang_default()

def set_lang(new_lang: str):
    st.session_state["lang"] = new_lang
    try:
        st.query_params["lang"] = new_lang
    except Exception:
        st.experimental_set_query_params(lang=new_lang)
    st.rerun()

LANG = st.session_state["lang"]

# ============================== i18n strings ===============================
TXT = {
    "en": {
        "title": "📋 Project Manager Risk Copilot",
        "caption": "Paste weekly project updates or notes → get structured risks (RAG), owners, probability/impact, and mitigations.",
        "lang_label": "Language / Sprache",
        "input_label": "Paste project status updates or notes",
        "input_ph": "Example: Backend API rate limits spiked on Monday; mobile release waiting for QA sign-off; vendor SSO cert expires next week…",
        "analyze_btn": "Analyze Risks",
        "no_key": "No API key found. Add OPENAI_API_KEY in Streamlit → Settings → Secrets.",
        "running": "Analyzing risks…",
        "done": "Done.",
        "output_h": "Risk Register",
        "about_h": "About",
        "about_p": "Step 2A: OpenAI connected. Generating a Markdown risk table (RAG) in your selected language. No sidebar yet.",
    },
    "de": {
        "title": "📋 Project Manager Risk Copilot",
        "caption": "Wöchentliche Projekt-Updates oder Notizen einfügen → strukturierte Risiken (RAG), Verantwortliche, Eintrittswahrscheinlichkeit/Auswirkung und Maßnahmen.",
        "lang_label": "Sprache",
        "input_label": "Projektstatus-Updates oder Notizen einfügen",
        "input_ph": "Beispiel: Backend-API-Rate-Limits stiegen am Montag; Mobile-Release wartet auf QA-Freigabe; SSO-Zertifikat des Anbieters läuft nächste Woche ab…",
        "analyze_btn": "Risiken analysieren",
        "no_key": "Kein API-Schlüssel gefunden. OPENAI_API_KEY in Streamlit → Settings → Secrets hinterlegen.",
        "running": "Risiken werden analysiert…",
        "done": "Fertig.",
        "output_h": "Risikoregister",
        "about_h": "Info",
        "about_p": "Schritt 2A: OpenAI angebunden. Erzeugt eine Markdown-Risikoliste (RAG) in der gewählten Sprache. Noch keine Sidebar.",
    },
}

# ============================== Header row =================================
st.markdown('<div class="header-row">', unsafe_allow_html=True)
col_left, col_right = st.columns([1, 0.32])
with col_left:
    st.title(TXT[LANG]["title"])
    st.caption(TXT[LANG]["caption"])
with col_right:
    new_lang = st.selectbox(TXT[LANG]["lang_label"], ["English", "Deutsch"],
                            index=(0 if LANG=="en" else 1), key="hdr_lang")
    picked = "en" if new_lang.startswith("English") else "de"
    if picked != LANG:
        set_lang(picked)
st.markdown('</div>', unsafe_allow_html=True)

# ============================== Main input =================================
text = st.text_area(
    TXT[LANG]["input_label"],
    height=220,
    placeholder=TXT[LANG]["input_ph"],
)

# ============================== OpenAI helper ==============================
def get_client():
    api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY", ""))
    if not api_key:
        st.warning(TXT[LANG]["no_key"])
        return None
    try:
        return OpenAI(api_key=api_key)
    except Exception as e:
        st.error(f"OpenAI init error: {e}")
        return None

def build_prompt_en(user_text: str) -> str:
    return f"""
You are a risk analyst for project managers. Read the notes below and output a concise **risk register**.

Return **ONLY** a Markdown table followed by a short bullet list. No intro/outro text.

**Columns (table):**
| ID | Risk | Owner | Probability | Impact | RAG | Mitigation | Due |

**Rules:**
- Probability & Impact: Low / Medium / High.
- RAG: Red/Amber/Green. Use emojis if helpful (🟥/🟧/🟩).
- Owner: a short name/role (infer if missing).
- Due: optional date or (—) if unknown.
- Keep rows to the 5–10 most important risks.
- Keep each cell short (1–2 lines).

**Then output:**
- **Top 3 Mitigation Actions**: bullet list (short, actionable).

Project notes:
{user_text}
""".strip()

def build_prompt_de(user_text: str) -> str:
    return f"""
Du bist Risikoanalyst:in für Projektmanager. Lies die Notizen und gib ein kurzes **Risikoregister** zurück.

Gib **NUR** eine Markdown-Tabelle gefolgt von einer kurzen Aufzählung aus. Kein Einleitungs-/Schlusstext.

**Spalten (Tabelle):**
| ID | Risiko | Verantwortlich | Wahrscheinlichkeit | Auswirkung | RAG | Maßnahme | Fällig |

**Regeln:**
- Wahrscheinlichkeit & Auswirkung: Niedrig / Mittel / Hoch.
- RAG: Rot/Amber/Grün. Emojis erlaubt (🟥/🟧/🟩).
- Verantwortlich: kurzer Name/Rolle (falls unbekannt: ableiten).
- Fällig: optionales Datum oder (—), wenn unbekannt.
- 5–10 wichtigste Risiken.
- Zellen kurz halten (1–2 Zeilen).

**Danach ausgeben:**
- **Top-3 Maßnahmen**: kurze, umsetzbare Stichpunkte.

Projektnotizen:
{user_text}
""".strip()

# ============================== Action =====================================
if st.button(TXT[LANG]["analyze_btn"], type="primary"):
    if not text.strip():
        st.info("Paste some notes first." if LANG=="en" else "Bitte zunächst Notizen einfügen.")
    else:
        client = get_client()
        if client:
            with st.spinner(TXT[LANG]["running"]):
                prompt = build_prompt_de(text) if LANG == "de" else build_prompt_en(text)
                try:
                    resp = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.2,
                        max_tokens=900,
                    )
                    out = resp.choices[0].message.content.strip()
                    st.success(TXT[LANG]["done"])
                    st.subheader(TXT[LANG]["output_h"])
                    st.markdown(out)
                except Exception as e:
                    st.error(f"OpenAI error: {e}")

st.markdown("<hr/>", unsafe_allow_html=True)
st.subheader(TXT[LANG]["about_h"])
st.caption(TXT[LANG]["about_p"])
