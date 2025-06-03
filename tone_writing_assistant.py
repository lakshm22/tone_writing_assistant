import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Load model and tokenizer once
model_name = "t5-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Set device properly
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Function to rewrite text
def rewrite_text(text, tone):
    prompt = f"Rewrite the following text in a {tone} tone:\n{text}"
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, padding=True).to(device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=128,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.7
        )

    rewritten_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return rewritten_text

# Streamlit UI
st.set_page_config(page_title="Smart Writing Assistant", layout="centered")
st.title("Smart Writing Assistant")
st.markdown("Rewrite your text to match a desired tone.")

input_text = st.text_area("Enter your text here:", height=200)
target_tone = st.selectbox("Choose target tone:", ["formal", "informal", "polite", "assertive", "empathetic"])

if st.button("Rewrite"):
    if input_text and target_tone:
        try:
            rewritten = rewrite_text(input_text, target_tone)
            st.subheader("Rewritten Text")
            st.write(rewritten)
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter text and select a tone.")
