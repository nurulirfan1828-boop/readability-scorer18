import streamlit as st
import textstat
import re

st.set_page_config(page_title="AI Readability Scorer", page_icon="📚")

st.title("📚 AI Reading Level & Complexity Scorer")
st.write("Paste an educational passage below to analyze its reading grade level and spot complex sentences.")

# User inputs
target_grade = st.selectbox("Select Target Grade Level:", [5, 6, 7, 8, 9, 10, 11, 12], index=3)
text_input = st.text_area("Paste your text here:", height=200, placeholder="Enter a paragraph from a textbook, article, or essay...")

if st.button("Analyze Text"):
    if len(text_input.strip()) < 20:
        st.warning("Please enter at least a couple of sentences to analyze.")
    else:
        # Calculate readability metrics
        fk_grade = textstat.flesch_kincaid_grade(text_input)
        reading_ease = textstat.flesch_reading_ease(text_input)
        difficult_words = textstat.difficult_words(text_input)
        word_count = textstat.lexicon_count(text_input, removepunct=True)

        # Display Metrics
        st.subheader("📊 Readability Breakdown")
        col1, col2, col3 = st.columns(3)
        col1.metric("Predicted Grade Level", f"Grade {round(fk_grade, 1)}")
        col2.metric("Reading Ease (0-100)", f"{round(reading_ease, 1)}")
        col3.metric("Complex Words", f"{difficult_words} / {word_count}")

        # Target Grade Comparison
        diff = fk_grade - target_grade
        if diff > 1.5:
            st.error(f"⚠️ This text is about **{round(diff, 1)} grade levels harder** than your Grade {target_grade} target.")
        elif diff < -1.5:
            st.info(f"ℹ️ This text is about **{round(abs(diff), 1)} grade levels easier** than your Grade {target_grade} target.")
        else:
            st.success(f"✅ Great match! This text aligns well with a **Grade {target_grade}** reading level.")

        # Highlight long/complex sentences
        st.subheader("🔍 Sentence-by-Sentence Complexity")
        sentences = re.split(r'(?<=[.!?]) +', text_input.strip())
        for s in sentences:
            s_words = textstat.lexicon_count(s, removepunct=True)
            if s_words > 22:
                st.markdown(f"🔴 **Long/Complex ({s_words} words):** {s}")
            else:
                st.markdown(f"🟢 **Clear ({s_words} words):** {s}")