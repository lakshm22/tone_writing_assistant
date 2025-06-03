import streamlit as st
from textblob import TextBlob
from transformers import pipeline

# Set Streamlit page configuration
st.set_page_config(page_title="Smart Writing Assistant", layout="centered")

# Title and subtitle
st.title("Smart Writing Assistant")
st.markdown("Analyze the tone of your writing and rewrite it to match your desired tone.")

# Load transformer model
@st.cache_resource
def load_model():
    return pipeline("text2text-generation", model="google/flan-t5-small")

generator = load_model()

# Function to detect tone using TextBlob
def detect_tone(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    if polarity > 0.5:
        tone = "Joyful / Positive"
    elif polarity < -0.3:
        tone = "Angry / Negative"
    else:
        tone = "Neutral / Informative"
    
    return tone, polarity, subjectivity

# Function to rewrite text using a given tone
def rewrite_text(input_text, target_tone):
    prompt = f"Rewrite the following in a {target_tone} tone: {input_text}"
    result = generator(prompt, max_length=128, do_sample=True)
    return result[0]['generated_text']

# UI components
input_text = st.text_area("✍️ Enter your text here:")
target_tone = st.selectbox("🎭 Choose your desired tone:", 
                           ["Formal", "Friendly", "Professional", "Persuasive", "Informative"])

if st.button("Analyze & Rewrite"):
    if input_text.strip():
        # Detect tone
        tone, polarity, subjectivity = detect_tone(input_text)
        st.markdown("### 🔍 Detected Tone:")
        st.write(f"**Tone**: {tone}")
        st.write(f"**Polarity**: {polarity:.2f}")
        st.write(f"**Subjectivity**: {subjectivity:.2f}")

        # Rewrite text
        st.markdown("### ✨ Rewritten Text:")
        rewritten = rewrite_text(input_text, target_tone)
        st.success(rewritten)
    else:
        st.warning("Please enter some text to analyze.")
