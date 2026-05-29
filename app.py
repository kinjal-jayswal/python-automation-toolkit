"""
NLP Text Classifier — JK Data Lab
Multi-class text classification with sentiment analysis using Streamlit
Author: Kinjal Jayswal | JK Data Lab
Website: https://www.jkdatalab.com
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re
from collections import Counter

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NLP Text Classifier | JK Data Lab",
    page_icon="🗣️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #0A2A2A; color: #ffffff; }
    h1, h2, h3 { color: #00FFD4; }
    .result-box {
        background: linear-gradient(135deg, #0d3333, #1a4a4a);
        border: 2px solid #00FFD4;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        text-align: center;
    }
    .positive { border-color: #00FFD4; }
    .negative { border-color: #ff6b6b; }
    .neutral  { border-color: #ffd93d; }
    .stButton>button {
        background-color: #00FFD4;
        color: #0A2A2A;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 2rem;
    }
    .stTextArea textarea { background-color: #0d2020; color: white; }
</style>
""", unsafe_allow_html=True)

# ─── Simple NLP Engine (no external API needed) ──────────────────────────────

POSITIVE_WORDS = set([
    "good", "great", "excellent", "amazing", "wonderful", "fantastic",
    "love", "perfect", "best", "awesome", "outstanding", "brilliant",
    "happy", "satisfied", "pleased", "recommend", "helpful", "fast",
    "easy", "reliable", "professional", "quality", "superb", "nice"
])

NEGATIVE_WORDS = set([
    "bad", "terrible", "awful", "horrible", "worst", "hate", "poor",
    "disappointed", "slow", "broken", "useless", "frustrating", "annoying",
    "waste", "expensive", "difficult", "problem", "issue", "error", "fail",
    "ugly", "boring", "confusing", "unclear", "unhelpful", "rude"
])

CATEGORIES = {
    "Technology": ["software", "app", "code", "python", "ai", "data", "machine",
                   "learning", "computer", "tech", "digital", "api", "cloud", "model"],
    "Business":   ["revenue", "profit", "sales", "market", "client", "customer",
                   "business", "company", "service", "price", "cost", "budget", "deal"],
    "Support":    ["help", "support", "issue", "problem", "fix", "error", "bug",
                   "broken", "need", "please", "urgent", "question", "how"],
    "Feedback":   ["review", "feedback", "experience", "recommend", "rating", "opinion",
                   "suggest", "improve", "better", "worse", "compare", "think"],
    "General":    []
}


def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    words = text.split()
    return words


def analyze_sentiment(words):
    pos = sum(1 for w in words if w in POSITIVE_WORDS)
    neg = sum(1 for w in words if w in NEGATIVE_WORDS)
    total = pos + neg
    if total == 0:
        score = 0.5
        label = "Neutral"
        emoji = "😐"
        color = "#ffd93d"
    elif pos / total >= 0.6:
        score = 0.5 + (pos / total) * 0.5
        label = "Positive"
        emoji = "😊"
        color = "#00FFD4"
    elif neg / total >= 0.6:
        score = (1 - neg / total) * 0.5
        label = "Negative"
        emoji = "😞"
        color = "#ff6b6b"
    else:
        score = 0.5
        label = "Neutral"
        emoji = "😐"
        color = "#ffd93d"
    return label, score, emoji, color, pos, neg


def classify_category(words):
    scores = {}
    for cat, keywords in CATEGORIES.items():
        scores[cat] = sum(1 for w in words if w in keywords)
    best = max(scores, key=scores.get)
    if scores[best] == 0:
        best = "General"
    total = sum(scores.values()) or 1
    probs = {k: round(v / total * 100, 1) for k, v in scores.items()}
    return best, probs


def get_key_phrases(words):
    stopwords = {"the", "a", "an", "is", "it", "this", "that", "was",
                 "are", "be", "been", "has", "had", "have", "i", "my",
                 "we", "you", "your", "they", "their", "and", "or", "but",
                 "in", "on", "at", "to", "for", "of", "with", "by"}
    filtered = [w for w in words if w not in stopwords and len(w) > 2]
    freq = Counter(filtered)
    return freq.most_common(10)


# ─── Header ─────────────────────────────────────────────────────────────────
st.title("🗣️ NLP Text Classifier")
st.markdown("**Sentiment Analysis + Text Classification** | Powered by NLP")
st.markdown("---")

# ─── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    mode = st.radio("Analysis Mode", ["Single Text", "Batch Analysis"])
    show_details = st.checkbox("Show Detailed Analysis", value=True)
    st.markdown("---")
    st.markdown("### 📝 Sample Texts")
    samples = {
        "Positive Review": "This is an excellent service! The team was very professional and delivered amazing results. Highly recommend!",
        "Negative Review": "Terrible experience. The software was broken and the support was unhelpful. Waste of money.",
        "Tech Query": "I need help with the Python API integration. The machine learning model is giving errors.",
        "Business Inquiry": "We are looking for a data science solution to improve our sales revenue and customer analytics.",
        "Neutral Feedback": "The service was okay. Nothing special but it worked fine for our requirements."
    }
    selected_sample = st.selectbox("Load Sample", [""] + list(samples.keys()))
    st.markdown("---")
    st.markdown("**🌐 [JK Data Lab](https://www.jkdatalab.com)**")

# ─── Single Text Mode ────────────────────────────────────────────────────────
if mode == "Single Text":
    default_text = samples.get(selected_sample, "") if selected_sample else ""

    text_input = st.text_area(
        "Enter text to analyze:",
        value=default_text,
        height=150,
        placeholder="Type or paste any text here — reviews, emails, feedback, queries..."
    )

    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        analyze_btn = st.button("🔍 Analyze", type="primary")
    with col2:
        clear_btn = st.button("🗑️ Clear")

    if clear_btn:
        st.rerun()

    if analyze_btn and text_input.strip():
        words = preprocess(text_input)
        sentiment_label, sentiment_score, emoji, color, pos_count, neg_count = analyze_sentiment(words)
        category, cat_probs = classify_category(words)
        key_phrases = get_key_phrases(words)
        word_count = len(words)
        char_count = len(text_input)
        sentence_count = len(re.split(r'[.!?]+', text_input))

        st.markdown("---")
        st.subheader("📊 Analysis Results")

        # Main results
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="result-box">
                <div style="font-size:2.5rem">{emoji}</div>
                <div style="color:{color}; font-size:1.4rem; font-weight:bold">{sentiment_label}</div>
                <div style="color:#aaa; font-size:0.8rem">Sentiment</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="result-box">
                <div style="font-size:2.5rem">🏷️</div>
                <div style="color:#00FFD4; font-size:1.4rem; font-weight:bold">{category}</div>
                <div style="color:#aaa; font-size:0.8rem">Category</div>
            </div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="result-box">
                <div style="font-size:2.5rem">📝</div>
                <div style="color:#00FFD4; font-size:1.4rem; font-weight:bold">{word_count}</div>
                <div style="color:#aaa; font-size:0.8rem">Words</div>
            </div>""", unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class="result-box">
                <div style="font-size:2.5rem">📊</div>
                <div style="color:#00FFD4; font-size:1.4rem; font-weight:bold">{sentiment_score:.0%}</div>
                <div style="color:#aaa; font-size:0.8rem">Confidence</div>
            </div>""", unsafe_allow_html=True)

        if show_details:
            st.markdown("---")
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📈 Sentiment Breakdown")
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=sentiment_score * 100,
                    domain={"x": [0, 1], "y": [0, 1]},
                    title={"text": "Sentiment Score", "font": {"color": "white"}},
                    gauge={
                        "axis": {"range": [0, 100], "tickcolor": "white"},
                        "bar": {"color": color},
                        "bgcolor": "#0d2020",
                        "steps": [
                            {"range": [0, 33], "color": "#3d0000"},
                            {"range": [33, 66], "color": "#2d2d00"},
                            {"range": [66, 100], "color": "#003d2d"},
                        ],
                        "threshold": {
                            "line": {"color": "white", "width": 2},
                            "thickness": 0.75,
                            "value": 50
                        }
                    }
                ))
                fig.update_layout(
                    paper_bgcolor="#0A2A2A", font=dict(color="white"),
                    height=250, margin=dict(l=20, r=20, t=40, b=20)
                )
                st.plotly_chart(fig, use_container_width=True)

                # Positive/Negative word counts
                fig2 = go.Figure(go.Bar(
                    x=["Positive Words", "Negative Words"],
                    y=[pos_count, neg_count],
                    marker_color=["#00FFD4", "#ff6b6b"],
                    text=[pos_count, neg_count],
                    textposition="outside"
                ))
                fig2.update_layout(
                    paper_bgcolor="#0A2A2A", plot_bgcolor="#0d2020",
                    font=dict(color="white"), height=200,
                    margin=dict(l=10, r=10, t=10, b=10)
                )
                st.plotly_chart(fig2, use_container_width=True)

            with col2:
                st.subheader("🏷️ Category Probabilities")
                cat_df = pd.DataFrame(
                    list(cat_probs.items()), columns=["Category", "Score"]
                ).sort_values("Score", ascending=True)
                fig3 = px.bar(
                    cat_df, x="Score", y="Category", orientation="h",
                    color="Score", color_continuous_scale="teal", text="Score"
                )
                fig3.update_traces(texttemplate="%{text}%", textposition="outside")
                fig3.update_layout(
                    paper_bgcolor="#0A2A2A", plot_bgcolor="#0d2020",
                    font=dict(color="white"), height=250,
                    margin=dict(l=10, r=10, t=10, b=10),
                    coloraxis_showscale=False
                )
                st.plotly_chart(fig3, use_container_width=True)

                st.subheader("🔑 Key Phrases")
                if key_phrases:
                    kp_df = pd.DataFrame(key_phrases, columns=["Word", "Frequency"])
                    fig4 = px.bar(
                        kp_df, x="Frequency", y="Word", orientation="h",
                        color="Frequency", color_continuous_scale="teal"
                    )
                    fig4.update_layout(
                        paper_bgcolor="#0A2A2A", plot_bgcolor="#0d2020",
                        font=dict(color="white"), height=250,
                        margin=dict(l=10, r=10, t=10, b=10),
                        coloraxis_showscale=False
                    )
                    st.plotly_chart(fig4, use_container_width=True)

    elif analyze_btn:
        st.warning("⚠️ Please enter some text to analyze!")

# ─── Batch Mode ─────────────────────────────────────────────────────────────
else:
    st.subheader("📦 Batch Text Analysis")
    st.markdown("Analyze multiple texts at once — paste one text per line")

    batch_input = st.text_area(
        "Enter texts (one per line):",
        height=200,
        placeholder="Text 1\nText 2\nText 3..."
    )

    if st.button("🔍 Analyze All", type="primary") and batch_input.strip():
        texts = [t.strip() for t in batch_input.split("\n") if t.strip()]
        results = []
        for text in texts:
            words = preprocess(text)
            sentiment, score, emoji, color, pos, neg = analyze_sentiment(words)
            category, _ = classify_category(words)
            results.append({
                "Text": text[:80] + "..." if len(text) > 80 else text,
                "Sentiment": f"{emoji} {sentiment}",
                "Category": category,
                "Score": f"{score:.0%}",
                "Words": len(words)
            })

        df_results = pd.DataFrame(results)
        st.dataframe(df_results, use_container_width=True, height=300)

        col1, col2 = st.columns(2)
        with col1:
            sent_counts = pd.DataFrame(results)["Sentiment"].value_counts().reset_index()
            fig = px.pie(sent_counts, values="count", names="Sentiment",
                         title="Sentiment Distribution",
                         color_discrete_sequence=["#00FFD4", "#ff6b6b", "#ffd93d"])
            fig.update_layout(paper_bgcolor="#0A2A2A", font=dict(color="white"), height=300)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            cat_counts = pd.DataFrame(results)["Category"].value_counts().reset_index()
            fig2 = px.bar(cat_counts, x="Category", y="count",
                          title="Category Distribution",
                          color="count", color_continuous_scale="teal")
            fig2.update_layout(paper_bgcolor="#0A2A2A", plot_bgcolor="#0d2020",
                               font=dict(color="white"), height=300,
                               coloraxis_showscale=False)
            st.plotly_chart(fig2, use_container_width=True)

# ─── Footer ─────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "Built with ❤️ by **[JK Data Lab](https://www.jkdatalab.com)** | "
    "kinjal@jkdatalab.com | Ahmedabad, India"
)
