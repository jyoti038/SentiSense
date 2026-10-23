
import streamlit as st
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download("vader_lexicon", quiet=True)
analyzer = SentimentIntensityAnalyzer()

st.set_page_config(
    page_title="SentiSense | AI Sentiment Analyzer",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
.stApp {
    background: #0b1020;
    color: #edf2ff;
}
header[data-testid="stHeader"] {
    background: transparent;
}
.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
section[data-testid="stSidebar"] {
    background: #10172a;
    border-right: 1px solid #27314a;
}
.hero {
    background: linear-gradient(120deg, #172554, #312e81 60%, #581c87);
    padding: 36px;
    border-radius: 24px;
    border: 1px solid #4338ca;
    margin-bottom: 26px;
}
.eyebrow {
    color: #c4b5fd;
    font-size: 12px;
    letter-spacing: 2px;
    font-weight: 700;
}
.hero h1 {
    color: white;
    font-size: clamp(30px, 4vw, 46px);
    font-weight: 800;
    margin: 12px 0;
}
.hero p {
    color: #dbeafe;
    font-size: 15px;
    line-height: 1.8;
}
.panel {
    background: #121a2d;
    border: 1px solid #293650;
    padding: 24px;
    border-radius: 20px;
    margin-bottom: 18px;
}
.result {
    padding: 26px;
    border-radius: 20px;
    border: 1px solid #34415c;
    background: linear-gradient(145deg, #172238, #111827);
    margin: 16px 0;
}
.result h2 {
    color: white;
    font-size: 30px;
    margin: 8px 0;
}
.muted {
    color: #a5b4cf;
    font-size: 13px;
}
.score-card {
    background: #121a2d;
    border: 1px solid #293650;
    padding: 20px;
    border-radius: 16px;
    min-height: 110px;
}
.score-number {
    color: white;
    font-size: 28px;
    font-weight: 800;
    margin-top: 8px;
}
div[data-testid="stTextArea"] textarea {
    background: #0f172a;
    color: #f8fafc;
    border: 1px solid #3a4968;
    border-radius: 14px;
    font-size: 16px;
    line-height: 1.7;
}
div.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 22px;
    font-weight: 700;
    min-height: 48px;
}
div.stButton > button {
    border-radius: 10px;
}
h1, h2, h3, p, label {
    color: #edf2ff;
}
hr {
    border-color: #293650;
}
</style>
""", unsafe_allow_html=True)

# ---------- SESSION STATE ----------
if "user_text" not in st.session_state:
    st.session_state.user_text = ""

if "history" not in st.session_state:
    st.session_state.history = []

samples = {
    "Write my own text": "",
    "Positive review": "I absolutely love this product! It is amazing, useful and wonderful.",
    "Negative review": "This product is terrible. I hate it and I am very disappointed.",
    "Neutral statement": "The book is lying on the table."
}

def load_sample():
    st.session_state.user_text = samples[
        st.session_state.sample_choice
    ]

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("## ◉ SentiSense")
    st.caption("AI-powered text insights")
    st.divider()

    st.markdown("### Navigation")
    st.markdown("📝  Sentiment Analyzer")
    st.markdown("📊  Score Analysis")
    st.markdown("🕘  Recent History")

    st.divider()
    st.markdown("### About this project")
    st.write(
        "SentiSense uses Natural Language Processing "
        "and the NLTK VADER sentiment analyzer."
    )
    st.caption("Python • NLTK • Streamlit")

    if st.button("Clear history", use_container_width=True):
        st.session_state.history = []
        st.rerun()

# ---------- HERO ----------
st.markdown("""
<div class="hero">
    <div class="eyebrow">NATURAL LANGUAGE PROCESSING · NLP</div>
    <h1>Understand the feeling<br>behind every sentence.</h1>
    <p>
        Analyze text in seconds. Discover positive, negative and
        neutral signals with an intuitive sentiment dashboard.
    </p>
</div>
""", unsafe_allow_html=True)

# ---------- INPUT PANEL ----------
st.markdown("### 📝 Analyze your text")
st.markdown(
    '<p class="muted">Enter a sentence, review or short paragraph below.</p>',
    unsafe_allow_html=True
)

st.selectbox(
    "Try an example",
    list(samples.keys()),
    key="sample_choice",
    on_change=load_sample
)

text = st.text_area(
    "Your text",
    key="user_text",
    height=160,
    max_chars=5000,
    placeholder="Example: The service was excellent and the staff were very helpful..."
)

st.caption(f"Characters: {len(text)} / 5000")

analyze = st.button(
    "✦  Analyze Sentiment",
    type="primary",
    use_container_width=True
)

# ---------- ANALYSIS ----------
if analyze:
    if not text.strip():
        st.warning("Please enter some text before analyzing.")
    else:
        scores = analyzer.polarity_scores(text)
        compound = scores["compound"]

        if compound >= 0.05:
            sentiment = "Positive"
            emoji = "😊"
            description = "Your text expresses an overall positive tone."
            color = "#34d399"
        elif compound <= -0.05:
            sentiment = "Negative"
            emoji = "😟"
            description = "Your text expresses an overall negative tone."
            color = "#fb7185"
        else:
            sentiment = "Neutral"
            emoji = "😐"
            description = "Your text is neutral or has a balanced tone."
            color = "#60a5fa"

        st.session_state.current_result = {
            "text": text,
            "sentiment": sentiment,
            "emoji": emoji,
            "description": description,
            "color": color,
            "scores": scores
        }

        st.session_state.history.insert(0, {
            "text": text,
            "sentiment": sentiment,
            "compound": compound
        })
        st.session_state.history = st.session_state.history[:5]

# Keep the latest result visible after Streamlit reruns
if "current_result" in st.session_state:
    result = st.session_state.current_result
    scores = result["scores"]

    st.markdown("### ✨ Analysis Results")

    st.markdown(f"""
    <div class="result" style="border-left: 5px solid {result['color']};">
        <div class="muted">DETECTED SENTIMENT</div>
        <h2>{result['emoji']} {result['sentiment']}</h2>
        <p>{result['description']}</p>
        <div class="muted">Compound score</div>
        <h2>{scores['compound']:+.3f}</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 📊 Sentiment breakdown")

    c1, c2, c3 = st.columns(3)

    for col, label, key, color in [
        (c1, "Positive", "pos", "#34d399"),
        (c2, "Negative", "neg", "#fb7185"),
        (c3, "Neutral", "neu", "#60a5fa")
    ]:
        with col:
            st.markdown(f"""
            <div class="score-card">
                <div style="color:{color};font-weight:700;">{label}</div>
                <div class="score-number">{scores[key] * 100:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(float(scores[key]))

    st.markdown("#### 🎯 Score interpretation")
    st.markdown(
        '<div class="panel">'
        '<p class="muted">Compound score ranges from -1 (most negative) '
        'to +1 (most positive).</p></div>',
        unsafe_allow_html=True
    )

    st.markdown("#### 🕘 Recent analyses")
    for item in st.session_state.history:
        st.markdown(
            f"**{item['sentiment']}** · "
            f"Score: {item['compound']:+.3f}  \n"
            f"{item['text'][:120]}"
        )
        st.divider()

else:
    st.markdown("""
    <div class="panel">
        <h3>🚀 Ready to analyze</h3>
        <p class="muted">
            Enter your text above and click Analyze Sentiment.
            Your result and sentiment scores will appear here.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown(
    '<p style="text-align:center;color:#64748b;font-size:12px;">'
    'SentiSense.'
    '</p>',
    unsafe_allow_html=True
)
