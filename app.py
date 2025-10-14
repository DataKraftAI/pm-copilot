import streamlit as st

st.set_page_config(page_title="Project Manager Risk Copilot", layout="wide")

# --- Simple i18n dictionary (Step 1 only: UI scaffold, no AI yet) ---
I18N = {
    "en": {
        "title": "Project Manager Risk Copilot",
        "subtitle": "Paste weekly project updates or notes → get structured risks (RAG), owners, and suggested mitigations.",
        "lang_label": "Language",
        "input_label": "Paste project status updates or notes",
        "input_ph": "Example: Backend API rate limits spiked on Monday; mobile release is waiting for QA sign-off; vendor SSO cert expires next week...",
        "analyze_btn": "Analyze Risks",
        "stub_header": "App is set up ✔",
        "stub_text": "Great! Deployment works. In the next step, we'll connect the risk engine (OpenAI) and produce a RAG risk list with owners, probability, impact, and mitigations — in your selected language.",
        "about": "About",
        "about_text": "This is Step 1 (UI scaffold). No AI calls yet. The goal is just to get the page live on Streamlit Cloud.",
    },
    "de": {
        "title": "Project Manager Risk Copilot",
        "subtitle": "Wöchentliche Projekt-Updates oder Notizen einfügen → strukturierte Risiken (RAG), Verantwortliche und Maßnahmenvorschläge erhalten.",
        "lang_label": "Sprache",
        "input_label": "Projektstatus-Updates oder Notizen einfügen",
        "input_ph": "Beispiel: Backend-API-Rate-Limits stiegen am Montag; Mobile-Release wartet auf QA-Freigabe; SSO-Zertifikat des Anbieters läuft nächste Woche ab...",
        "analyze_btn": "Risiken analysieren",
        "stub_header": "App ist eingerichtet ✔",
        "stub_text": "Super! Das Deployment funktioniert. Im nächsten Schritt verbinden wir die Risiko-Engine (OpenAI) und erzeugen eine RAG-Risikoliste mit Verantwortlichen, Eintrittswahrscheinlichkeit, Auswirkung und Maßnahmen — in der gewählten Sprache.",
        "about": "Info",
        "about_text": "Dies ist Schritt 1 (UI-Gerüst). Noch keine AI-Aufrufe. Ziel: Seite auf Streamlit Cloud live bringen.",
    },
}

# Sidebar language picker
with st.sidebar:
    lang = st.selectbox("Language / Sprache", ["English", "Deutsch"])
    lang_code = "de" if lang == "Deutsch" else "en"
    st.markdown("---")
    st.subheader(I18N[lang_code]["about"])
    st.caption(I18N[lang_code]["about_text"])

st.title("📊 " + I18N[lang_code]["title"])
st.caption(I18N[lang_code]["subtitle"])

text = st.text_area(
    I18N[lang_code]["input_label"],
    height=220,
    placeholder=I18N[lang_code]["input_ph"],
)

if st.button(I18N[lang_code]["analyze_btn"]):
    st.success(I18N[lang_code]["stub_header"])
    st.info(I18N[lang_code]["stub_text"])
    if text.strip():
        with st.expander("Your pasted text (for testing) / Ihr eingefügter Text (zum Testen)"):
            st.write(text.strip())
    else:
        st.write("—")

# Footer
st.markdown("<hr/>", unsafe_allow_html=True)
st.caption("Step 1 • UI scaffold only · Keine AI · Next: connect the risk engine.")