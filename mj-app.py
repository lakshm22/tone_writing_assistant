import streamlit as st
from textblob import TextBlob
import pandas as pd
import random

# Read affirmation dataset from kaggle
try:
    affirmation_df = pd.read_csv("possitive_affirmation.csv")
    affirmation_list = affirmation_df['Affirmation'].dropna().tolist()
except Exception as e:
    affirmation_list = ["I am worthy of love and respect.", "Every day is a new chance to grow."]


# Sentiment Analysis
def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.2:
        return "Positive"
    elif polarity < -0.2:
        return "Negative"
    else:
        return "Neutral"

def rewrite_text(text):
    sentiment = analyze_sentiment(text)
    if sentiment == "Negative":
        return "It's okay to feel this way. Be gentle with yourself—you're doing the best you can. 🌱"
    elif sentiment == "Neutral":
        return "Take a moment to breathe and reflect. You have the strength to move forward. 💫"
    else:
        return "You're radiating good energy! Keep shining and stay grounded. 🌞"

def suggest_prompt_or_affirmation():
    prompts = [
        "What am I proud of today?",
        "What’s something I can do to care for myself?",
        "How did I handle a challenge recently?",
        "What emotion am I feeling right now and why?",
        "What does my inner child need to hear today?"
    ]
    affirmation = random.choice(affirmation_list)
    return random.choice(prompts), affirmation
    
# Streamlit UI Dashboard
st.set_page_config(page_title="AI Mood Journal", page_icon="📝")
st.title("AI Mood Journal")
st.markdown("Type what you’re feeling.")
st.markdown("The app will reflect back a kind rewrite, mood insight, and a helpful prompt. ✨")

user_input = st.text_area("What's on your mind today?", height=200)

if st.button("Analyze & Reflect"):
    if user_input.strip():
        mood = analyze_sentiment(user_input)
        rewrite = rewrite_text(user_input)
        prompt, affirmation = suggest_prompt_or_affirmation()

        st.subheader("💬 Detected Mood")
        st.info(f"**{mood}**")

        st.subheader("🪞 Rewritten Reflection")
        st.success(rewrite)

        st.subheader("🧘 Journal Prompt")
        st.write(f"**{prompt}**")

        st.subheader("🌸 Affirmation")
        st.write(f"_{affirmation}_")
    else:
        st.warning("Please enter some text to reflect on.")

# Sidebar contents
st.sidebar.title("📖 About This Project – AI Mood Journal")
st.sidebar.write(
    "AI Mood Journal is a self-reflection and emotional support tool designed to help users process their thoughts with kindness and clarity. Whether you're overwhelmed, anxious, hopeful, or just need to vent, the app listens without judgment and responds with gentle rewrites, empowering affirmations, and introspective prompts. "
    ""
    "By combining natural language processing, sentiment analysis, and a simple Streamlit interface, this tool turns raw emotions into reflections that support healing, growth, and self-understanding. "
)
st.sidebar.title("🌿 Why It Matters")
st.sidebar.write(
    "We often write in moments of emotional intensity. This app honors that vulnerability—and then offers a shift in tone, helping you rewrite your inner dialogue with self-compassion."
)

st.sidebar.title("🛠 Built With")
st.sidebar.write(
    "Python "
    ""
    "Streamlit (UI Framework) "
    ""
    "TextBlob (Sentiment Detection) "
    ""
    "Pandas (CSV Handling) "
    ""
    "Affirmation CSV Dataset (Customizable & Expandable)"
)
st.sidebar.markdown("---")
st.sidebar.caption("Created with ❤️ by Lakshitha M")
