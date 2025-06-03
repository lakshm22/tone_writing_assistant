import streamlit as st
from transformers import T5ForConditionalGeneration, T5Tokenizer
from textblob import TextBlob
import torch

st.set_page_config(page_title="Smart Writing Assistant", layout="centered")

st.title("Smart Writing Assistant")
st.markdown(
    "Refine your writing tone with the help of AI. Just enter your text, choose a target tone, and let the assistant rewrite it!"
)

# Load model and tokenizer once (cached)
def load_model():
    model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-small")
    tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-small")
    return model, tokenizer

model, tokenizer = load_model()

# Tone rewriting function
def rewrite_text(input_text, target_tone):
    prompt = f"Rewrite the following in a {target_tone} tone: {input_text}"
    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=512
    )
    try:
        with torch.no_grad():
            outputs = model.generate(**inputs, max_new_tokens=128)
        return tokenizer.decode(outputs[0], skip_special_tokens=True)
    except Exception as e:
        return f"Error in rewriting text: {e}"

# UI inputs
input_text = st.text_area("Enter your original text:")
target_tone = st.selectbox(
    "Select desired tone:",
    ["Formal", "Informal", "Polite", "Professional", "Persuasive", "Empathetic"]
)

if st.button("Rewrite"):
    if input_text.strip() == "":
        st.warning("Please enter some text first.")
    else:
        rewritten = rewrite_text(input_text, target_tone)
        st.subheader("🎯 Rewritten Text")
        st.success(rewritten)

        # Optional: show sentiment analysis
        st.subheader("🧠 Sentiment Analysis")
        blob = TextBlob(rewritten)
        sentiment = blob.sentiment
        st.write(f"**Polarity:** {sentiment.polarity:.2f} (−1 to +1)")
        st.write(f"**Subjectivity:** {sentiment.subjectivity:.2f} (0 to 1)")
