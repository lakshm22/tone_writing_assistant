from textblob import TextBlob
from transformers import T5ForConditionalGeneration
from transformers import T5Tokenizer
from transformers import pipeline
import streamlit as st

# Loading paraphrasing model using Hugging Face Transformer
model_name = "google/flan-t5-base"
tokenizer = T5Tokenizer.from_pretrained(model_name)

# Loading model and tokeniser separately
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# Pipeline creation
paraphraser = pipeline("text2text-generation", model=model, tokenizer=tokenizer)

def detect_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    return polarity, subjectivity

def rewrite_text(text, tone):
    prompt = (
        f"Rewrite the following sentence in a {tone.lower()} tone.\n\n"
        f"Original: {text}\n"
        f"{tone} Tone:"
    )
    output = paraphraser(
        prompt,
        max_length=100,
        do_sample=True,
        top_k=50,
        top_p=0.95
    )[0]['generated_text']
    return output


# Streamlit app interactive dashboard
st.set_page_config(page_title="Text Enhancer", layout="centered")
st.title("Tone-Aware Text Enhancer")
st.write("Improve and rewrite your text to match your preferred tone!")
user_input = st.text_area("Enter your text here:", height=200)
    
if user_input:
    if st.button("Analyze Tone"):
        polarity, subjectivity = detect_sentiment(user_input)
        st.markdown(f"**Polarity:** {polarity:.2f} (negative to positive)")
        st.markdown(f"**Subjectivity:** {subjectivity:.2f} (objective to subjective)")
    tone = st.selectbox("Choose the tone you want:", ["Formal", "Casual", "Friendly", "Assertive", "Professional"])
    
    if st.button("Rewrite in Selected Tone"):
        with st.spinner("Rewriting your text..."):
            result = rewrite_text(user_input, tone)
        st.markdown("### ✨ Rewritten Text")
        st.success(result)
