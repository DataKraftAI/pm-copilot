import streamlit as st

# ============================== Page & style ===============================
st.set_page_config(page_title="Project Manager Risk Copilot", layout="wide")
st.markdown("""
<style>
/* Match button style from other apps */
.stButton > button[kind="primary"]{
  padding: 12px 18px;
  font-size: 16px;
  font-weight: 700;
  border-radius: 10px;
}
/* Right-aligned header language select */
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
        "stub_h": "App is set up ✔",
        "stub_p": "Great—deployment works. Next step: wire the OpenAI risk engine and output a RAG table with owners, probability, impact, and mitigations in the selected language.",
        "info_h": "About",
        "info_p": "Step 1 scaffold only. No AI calls yet.",
    },
    "de": {
        "title": "📋 Project Manager Risk Copilot",
        "caption": "Wöchentliche Projekt-Updates oder Notizen einfügen → strukturierte Risiken (RAG), Verantwortliche, Eintrittswahrscheinlichkeit/Auswirkung und Maßnahmen.",
        "lang_label": "Sprache",
        "input_label": "Projektstatus-Updates oder Notizen einfügen",
        "input_ph": "Beispiel: Backend-API-Rate-Limits stiegen am Montag; Mobile-Release wartet auf QA-Freigabe; SSO-Zertifikat des Anbieters läuft nächste Woche ab…",
        "analyze_btn": "Risiken analysieren",
        "stub_h": "App ist eingerichtet ✔",
        "stub_p": "Super—Deployment funktioniert. Nächster Schritt: Risiko-Engine (OpenAI) anbinden und eine RAG-Tabelle mit Verantwortlichen, Wahrscheinlichkeit, Auswirkung und Maßnahmen in der gewählten Sprache erzeugen.",
        "info_h": "Info",
        "info_p": "Nur Schritt-1-Gerüst. Noch keine KI-Aufrufe.",
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

if st.button(TXT[LANG]["analyze_btn"], type="primary"):
    st.success(TXT[LANG]["stub_h"])
    st.info(TXT[LANG]["stub_p"])
    if text.strip():
        with st.expander("Your pasted text (for testing) / Ihr eingefügter Text (zum Testen)"):
            st.write(text.strip())
    else:
        st.write("—")

st.markdown("<hr/>", unsafe_allow_html=True)
st.subheader(TXT[LANG]["info_h"])
st.caption(TXT[LANG]["info_p"])
