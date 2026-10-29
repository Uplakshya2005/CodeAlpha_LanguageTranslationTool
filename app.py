import streamlit as st
import requests
import html
import time

st.set_page_config(
    page_title="LingoAI Translation Studio",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

LANGUAGES = {
    "Auto Detect": "autodetect",
    "English": "en",
    "Hindi": "hi",
    "Bengali": "bn",
    "Gujarati": "gu",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Nepali": "ne",
    "Punjabi": "pa",
    "Tamil": "ta",
    "Telugu": "te",
    "Urdu": "ur",
    "Arabic": "ar",
    "Chinese (Simplified)": "zh",
    "Dutch": "nl",
    "French": "fr",
    "German": "de",
    "Greek": "el",
    "Hebrew": "he",
    "Indonesian": "id",
    "Italian": "it",
    "Japanese": "ja",
    "Korean": "ko",
    "Persian": "fa",
    "Polish": "pl",
    "Portuguese": "pt",
    "Russian": "ru",
    "Spanish": "es",
    "Thai": "th",
    "Turkish": "tr",
    "Ukrainian": "uk",
    "Vietnamese": "vi",
}

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.stApp {
    background: radial-gradient(circle at 15% 5%, #20234c 0, transparent 35%),
                radial-gradient(circle at 90% 20%, #173b56 0, transparent 30%),
                #0b1020;
    color: #f3f5ff;
    font-family: 'Inter', sans-serif;
}
.block-container {max-width: 1120px; padding-top: 2.2rem; padding-bottom: 3rem;}
h1, h2, h3, p, label {color: #f3f5ff;}
.hero {text-align:center; padding: 1.1rem 0 1.6rem;}
.logo {font-size: 2.8rem; margin-bottom: .2rem;}
.hero h1 {font-size: clamp(2.2rem, 5vw, 3.4rem); font-weight: 800; margin:0;}
.hero p {color:#b9c2e4; font-size:1.05rem; margin-top:.65rem;}
.panel {
    background: rgba(20, 28, 53, .92);
    border: 1px solid rgba(145, 160, 220, .22);
    border-radius: 20px; padding: 1.25rem;
}
.small-muted {color:#aab5d8; font-size:.9rem;}
.output {
    background: #111a31; border:1px solid #354366; border-radius:14px;
    min-height:145px; padding:1rem; color:#f7f8ff; white-space:pre-wrap;
    overflow-wrap:anywhere; line-height:1.65;
}
div.stButton > button {
    border-radius: 12px; border: 1px solid #6779ff;
    background: linear-gradient(90deg,#5965f2,#8b5cf6);
    color:white; font-weight:700; min-height: 2.8rem;
}
div.stButton > button:hover {border-color:#aab2ff; color:white;}
div[data-baseweb="select"] > div, .stTextArea textarea {
    background-color:#111a31 !important; color:#f5f6ff !important;
    border-color:#3b486b !important; border-radius:12px !important;
}
.stTextArea textarea {line-height:1.6;}
hr {border-color:#293555;}
footer {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div class="logo">🌐</div>
  <h1>LingoAI <span style="color:#8c9bff">Studio</span></h1>
  <p>Translate your words and connect across languages.</p>
</div>
""", unsafe_allow_html=True)

left, right = st.columns(2, gap="large")

with left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("### 📝 Source text")
    source_names = list(LANGUAGES.keys())
    source_default = source_names.index("Auto Detect")
    source_lang_name = st.selectbox(
        "Translate from",
        source_names,
        index=source_default,
        key="source_language",
    )
    source_text = st.text_area(
        "Enter text",
        placeholder="Type or paste the text you want to translate...",
        height=220,
        max_chars=5000,
        key="source_text",
        label_visibility="collapsed",
    )
    st.caption(f"{len(source_text)} / 5,000 characters")
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("### ✨ Translation")
    target_names = [name for name in source_names if name != "Auto Detect"]
    target_default = target_names.index("Hindi")
    target_lang_name = st.selectbox(
        "Translate to",
        target_names,
        index=target_default,
        key="target_language",
    )
    st.markdown('<div class="small-muted">Your translated text will appear below.</div>', unsafe_allow_html=True)
    translated = st.session_state.get("translated_text", "")
    st.markdown(
        f'<div class="output">{html.escape(translated) if translated else "Translation will appear here..."}</div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

button_col1, button_col2, button_col3 = st.columns([1, 2, 1])
with button_col2:
    translate_clicked = st.button("🌍  Translate Text", use_container_width=True)

def translate_mymemory(text, source_code, target_code):
    """Translate using MyMemory's public API. Requires internet; no API key."""
    endpoint = "https://api.mymemory.translated.net/get"
    # MyMemory accepts a limited amount of text per request; keep requests modest.
    if len(text.encode("utf-8")) > 450:
        raise ValueError(
            "This free API request is too long. Please shorten the text to around 400 characters and try again."
        )
    params = {
        "q": text,
        "langpair": f"{source_code}|{target_code}",
    }
    headers = {"User-Agent": "LingoAI-Student-Translation-Tool/1.0"}
    response = requests.get(endpoint, params=params, headers=headers, timeout=20)
    response.raise_for_status()
    data = response.json()
    if data.get("responseStatus") not in (200, "200"):
        detail = data.get("responseDetails") or "The translation service could not process this request."
        raise RuntimeError(str(detail))
    result = data.get("responseData", {}).get("translatedText", "")
    if not result:
        raise RuntimeError("The translation service returned an empty result.")
    # MyMemory can return HTML entities in translated text.
    return html.unescape(result)

if translate_clicked:
    text_to_translate = source_text.strip()
    source_code = LANGUAGES[source_lang_name]
    target_code = LANGUAGES[target_lang_name]

    if not text_to_translate:
        st.warning("Please enter some text to translate.")
    elif source_lang_name != "Auto Detect" and source_code == target_code:
        st.info("Source and target languages are the same. Choose a different target language.")
    else:
        try:
            with st.spinner("Translating..."):
                result = translate_mymemory(text_to_translate, source_code, target_code)
            st.session_state["translated_text"] = result
            st.rerun()
        except requests.Timeout:
            st.error("The translation service took too long to respond. Please try again later.")
        except requests.RequestException:
            st.error("Could not connect to the translation service. Check your internet connection and try again.")
        except Exception as exc:
            st.error(f"Translation failed: {exc}")

translated = st.session_state.get("translated_text", "")
if translated:
    copy_col, clear_col = st.columns([1, 5])
    with copy_col:
        st.download_button(
            "⬇️ Save result",
            data=translated,
            file_name="translation.txt",
            mime="text/plain",
            use_container_width=True,
        )

st.markdown("---")
feature1, feature2, feature3 = st.columns(3)
with feature1:
    st.markdown("#### 🌍 Multiple languages")
    st.markdown('<p class="small-muted">Translate between a selection of commonly used languages.</p>', unsafe_allow_html=True)
with feature2:
    st.markdown("#### 🔑 No API key")
    st.markdown('<p class="small-muted">Uses the public MyMemory endpoint without an API key.</p>', unsafe_allow_html=True)
with feature3:
    st.markdown("#### ⚡ Simple workflow")
    st.markdown('<p class="small-muted">Enter text, select languages, and press Translate.</p>', unsafe_allow_html=True)

st.markdown(
    '<p style="text-align:center;color:#7f8bb2;font-size:.82rem;margin-top:2rem;">'
    'LingoAI Translation Studio · Student project · Free service limits apply</p>',
    unsafe_allow_html=True,
)
