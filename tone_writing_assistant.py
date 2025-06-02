import streamlit as st
from textblob import TextBlob
import language_tool_python
import textstat
import nltk
nltk.download('punkt')

# Use the public API (no Java needed)
tool = language_tool_python.LanguageToolPublicAPI('en-US')

def correct_grammar(text):
    matches = tool.check(text)
    return language_tool_python.utils.correct(text, matches)

def simple_sentence_split(text):
    import re
    # Split on period, question mark, exclamation mark followed by space or end of string
    sentences = re.split(r'(?<=[.!?]) +', text)
    return [s.strip() for s in sentences if s.strip()]

def simplify_text(text):
    sentences = simple_sentence_split(text)
    simplified_sentences = []
    for sentence in sentences:
        # Using TextBlob just for spelling correction on each sentence
        corrected = str(TextBlob(sentence).correct())
        simplified_sentences.append(corrected)
    return ". ".join(simplified_sentences)

def get_readability_scores(text):
    return {
        "Flesch Reading Ease": textstat.flesch_reading_ease(text),
        "Flesch-Kincaid Grade": textstat.flesch_kincaid_grade(text),
        "Gunning Fog Index": textstat.gunning_fog(text),
        "SMOG Index": textstat.smog_index(text),
        "Automated Readability Index": textstat.automated_readability_index(text),
        "Dale-Chall Score": textstat.dale_chall_readability_score(text),
    }

st.set_page_config(page_title="SmartText Enhancer", layout="wide")
st.title("Smart Text Enhancer")
st.markdown("Enhance your writing with grammar correction, simplification, and readability analysis!")

text = st.text_area("✍️ Enter your text here:", height=250)

if st.button("Enhance Text"):
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
