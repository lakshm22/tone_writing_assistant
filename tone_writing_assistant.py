import streamlit as st
from textblob import TextBlob
import language_tool_python
import textstat

# Setup language tool
tool = language_tool_python.LanguageTool('en-US')

# Functions
def correct_grammar(text):
    matches = tool.check(text)
    return language_tool_python.utils.correct(text, matches)

def get_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment

def simplify_text(text):
    blob = TextBlob(text)
    simplified = ". ".join([str(sentence.correct()) for sentence in blob.sentences])
    return simplified

def get_readability_scores(text):
    return {
        "Flesch Reading Ease": textstat.flesch_reading_ease(text),
        "Flesch-Kincaid Grade": textstat.flesch_kincaid_grade(text),
        "Gunning Fog Index": textstat.gunning_fog(text),
        "SMOG Index": textstat.smog_index(text),
        "Automated Readability Index": textstat.automated_readability_index(text),
        "Dale-Chall Score": textstat.dale_chall_readability_score(text),
    }

# Streamlit UI
st.set_page_config(page_title="SmartText Enhancer", layout="wide")
st.title("📝 SmartText Enhancer")
st.markdown("Enhance your writing with grammar correction, simplification, and readability analysis!")

text = st.text_area("✍️ Enter your text here:", height=250)

if st.button("🚀 Enhance Text"):
    if not text.strip():
        st.warning("Please enter some text to enhance.")
    else:
        st.subheader("✅ Corrected Grammar")
        corrected = correct_grammar(text)
        st.write(corrected)

        st.subheader("🪄 Simplified Text")
        simplified = simplify_text(corrected)
        st.write(simplified)

        st.subheader("📊 Readability Scores")
        scores = get_readability_scores(simplified)
        for name, score in scores.items():
            st.markdown(f"**{name}:** {score:.2f}")

        st.subheader("🔍 Sentiment Analysis")
        sentiment = get_sentiment(text)
        st.markdown(f"**Polarity:** {sentiment.polarity:.2f}")
        st.markdown(f"**Subjectivity:** {sentiment.subjectivity:.2f}")

        st.success("Enhancement Complete!")
