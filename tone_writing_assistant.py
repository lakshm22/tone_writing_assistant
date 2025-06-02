import streamlit as st
import language_tool_python

# Initialize LanguageTool
tool = language_tool_python.LanguageTool('en-US')

def correct_text(text):
    matches = tool.check(text)
    corrected_text = language_tool_python.utils.correct(text, matches)
    return matches, corrected_text

# Streamlit App
st.set_page_config(page_title="Mini Grammarly", layout="wide")

st.title("📝 Mini Grammarly - Grammar & Spell Checker")

text_input = st.text_area("Enter your text here:", height=200)

if st.button("Check Grammar"):
    if text_input.strip():
        with st.spinner("Analyzing..."):
            matches, corrected_text = correct_text(text_input)

        st.subheader("✅ Corrected Text:")
        st.write(corrected_text)

        if matches:
            st.subheader("🛠 Suggestions:")
            for match in matches:
                st.markdown(f"- **{match.ruleIssueType.title()}**: {match.message}")
                st.markdown(f"  - Suggestion: `{', '.join(match.replacements)}`")
                st.markdown(f"  - Context: `{match.context}`")
        else:
            st.success("Your text is already perfect! 🎉")
    else:
        st.warning("Please enter some text to analyze.")
