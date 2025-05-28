import streamlit as st
from textblob import TextBlob
import spacy
from spacy.cli import download

# this section is to load spaCy model and download it if missing
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# this section is for configuration like emoji or logo
st.set_page_config(
    page_title="VoxPopuli: Speech Analyzer",
    page_icon="🇮🇳",
    layout="wide"
)

# this is for indian flag colour theme 
def get_flag_style():
    st.markdown(
        """
        <style>
        .main {
            background-color: #ffffff;
        }
        .st-bx { background: #ff9933 !important; }
        .st-bv { background: #ffffff !important; }
        .st-bw { background: #138808 !important; }
        .big-title { font-size: 2.5em; color: #138808; font-weight: bold;}
        .tagline { color: #ff9933; font-size: 1.2em;}
        .section-header { color: #054187; font-weight: bold; margin-top: 24px;}
        .stButton>button { background-color: #ff9933; color: #ffffff; font-weight: bold; }
        .analysis-box { border: 2px solid #054187; border-radius: 8px; padding: 18px; margin-bottom: 18px;}
        </style>
        """,
        unsafe_allow_html=True,
    )

get_flag_style()

# header
st.markdown(f"<div class='big-title'>🇮🇳 VoxPopuli: Speech Analyzer</div>", unsafe_allow_html=True)
st.markdown(f"<div class='tagline'>Clarity in action: Transparency for a better future.</div>", unsafe_allow_html=True)
st.write("")

# this section is about - about, info etc
with st.sidebar:
    st.markdown("### About VoxPopuli")
    st.info("""
    Welcome to our website where we make things — or you can say speeches — transparent for the people, in the form of subjectivity, tone, and more. This project was created with a mission to unveil the true meaning behind speeches given in parliament.

    **My name is Harsh Bhati.**

    This project was initiated to solve the problem of understanding parliament or any other speech by famous figures.
    """)
    st.markdown("### How to Use")
    st.success("""
    1. Paste a parliamentary or public speech in the text box.
    2. Click 'Analyze Speech'.
    3. View the analysis of tone, subjectivity, and named entities.
    """)
    st.markdown("### Contact")
    st.write("📧 harshbhati5252@gmail.com")
    st.write("[LinkedIn](https://www.linkedin.com/in/harsh-bhati-7a5952313)")

# main app 
st.markdown("<hr style='border:2px solid #054187;'>", unsafe_allow_html=True)

st.header("🔎 Speech Analyzer")
example_speech = (
    "Honorable members of the parliament, today we gather to discuss critical reforms that will shape the future of our nation. "
    "Our focus must be on improving education, healthcare, and infrastructure to ensure prosperity for all citizens. I firmly believe that by working together, we can create a more inclusive and equitable society. "
    "We must also invest in renewable energy and sustainable development to protect our environment for future generations. "
    "Let us commit to transparency, accountability, and the welfare of every citizen. Together, we will overcome challenges and build a stronger nation."
)

with st.expander("Need an example? Click here to fill with a sample speech!"):
    if st.button("Use Sample Speech"):
        st.session_state['speech_input'] = example_speech

speech_input = st.text_area(
    "Paste a parliamentary speech here:",
    value=st.session_state.get('speech_input', ''),
    height=200,
    key="speech_input"
)

analyze = st.button("Analyze Speech")

if analyze and speech_input.strip():
    blob = TextBlob(speech_input)
    sentiment = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    if sentiment > 0.1:
        sentiment_label = "🔵 Positive"
        sentiment_color = "#054187"
    elif sentiment < -0.1:
        sentiment_label = "🔴 Negative"
        sentiment_color = "#E03A3E"
    else:
        sentiment_label = "⚪️ Neutral"
        sentiment_color = "#ffffff"

    doc = nlp(speech_input)
    entities = [ent.text for ent in doc.ents]

    st.markdown(f"<div class='analysis-box'>"
                f"<b>Sentiment Score:</b> <span style='color:{sentiment_color}; font-weight:bold'>{sentiment:.2f} {sentiment_label}</span><br>"
                f"<b>Subjectivity:</b> {subjectivity:.2f} "
                f"({'Opinionated' if subjectivity > 0.5 else 'Factual'})<br>"
                f"<b>Named Entities:</b> {', '.join(entities) if entities else 'No named entities found.'}"
                f"</div>", unsafe_allow_html=True)
elif analyze and not speech_input.strip():
    st.warning("Please enter a speech to analyze.")

st.markdown("<hr style='border:2px solid #138808;'>", unsafe_allow_html=True)

st.caption("Made by Harsh Bhati • VoxPopuli 2025 🇮🇳")
