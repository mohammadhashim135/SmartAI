import streamlit as st
import json
from tools.ai_client import call_ai


def summarizer():

    st.markdown("""
    <div class="tool-header">
        <span class="tool-icon">📚</span>
        <div>
            <h2>Study Assistant & Summarizer</h2>
            <p>Summarize notes, generate flashcards, explain topics, and create practice questions.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    mode = st.selectbox(
        "What do you need?",
        [
            "📝 Summarize Notes",
            "❓ Generate Flashcards",
            "📋 Extract Key Points",
            "📖 Explain Like I'm 10",
            "🧪 Create Practice Questions"
        ]
    )

    subject = st.text_input("Subject (optional)", placeholder="Physics, History, Biology...")

    text = st.text_area(
        "Paste notes or topic",
        height=200,
        placeholder="Paste lecture notes or topic here..."
    )

    if st.button("✨ Process with AI", type="primary", use_container_width=True):

        if not text.strip():
            st.warning("Please enter some text.")
            return

        with st.spinner("Processing with AI..."):

            subject_context = f"Subject: {subject}" if subject else ""

            if mode == "📝 Summarize Notes":

                system = """
                Return ONLY valid JSON.

                {
                "title":"",
                "summary":"",
                "key_concepts":["","",""],
                "study_tips":["",""]
                }
                """

                prompt = f"Summarize these notes.\n{subject_context}\n{text}"

            elif mode == "❓ Generate Flashcards":

                system = """
                Return ONLY valid JSON.

                {
                "topic":"",
                "flashcards":[
                {"question":"","answer":""}
                ]
                }

                Provide at least 3 flashcards.
                """

                prompt = f"Create flashcards from this content:\n{text}"

            elif mode == "📋 Extract Key Points":

                system = """
                Return ONLY valid JSON.

                {
                "title":"",
                "main_idea":"",
                "points":["","",""]
                }
                """

                prompt = f"Extract key points from:\n{text}"

            elif mode == "📖 Explain Like I'm 10":

                system = """
                Return ONLY valid JSON.

                {
                "topic":"",
                "simple_explanation":"",
                "analogy":"",
                "summary":""
                }
                """

                prompt = f"Explain this in a very simple way for a child:\n{text}"

            else:

                system = """
                Return ONLY valid JSON.

                {
                "topic":"",
                "questions":[
                {"question":"","answer":""}
                ]
                }

                Provide at least 3 questions.
                """

                prompt = f"Create practice questions from:\n{text}"

            try:

                result_text = call_ai(prompt, system)

                if not result_text or result_text.strip() == "":
                    st.error("AI returned empty response")
                    return

                start = result_text.find("{")
                end = result_text.rfind("}") + 1

                if start == -1 or end == -1:
                    st.error("AI did not return valid JSON")
                    st.write(result_text)
                    return

                clean_json = result_text[start:end]
                result = json.loads(clean_json)

                st.success("AI Result")

                st.json(result)

            except Exception as e:
                st.error(f"Error: {e}")


def text_classifier():

    st.markdown("""
    <div class="tool-header">
        <span class="tool-icon">🏷️</span>
        <div>
            <h2>Text Classifier</h2>
            <p>Analyze sentiment, topic, intent, and tone of any text.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    text = st.text_area(
        "Enter text",
        height=150,
        placeholder="Paste any text here..."
    )

    if st.button("🏷️ Classify Text", type="primary", use_container_width=True):

        if not text.strip():
            st.warning("Please enter text.")
            return

        with st.spinner("Analyzing text..."):

            system = """
            Return ONLY valid JSON.

            {
            "sentiment":"positive | negative | neutral",
            "topic":"main topic",
            "intent":"inform | request | opinion | complaint | praise",
            "tone":"formal | casual | enthusiastic | angry | neutral",
            "summary":"short explanation"
            }
            """

            prompt = f"Analyze this text:\n{text}"

            try:

                result_text = call_ai(prompt, system)

                if not result_text or result_text.strip() == "":
                    st.error("AI returned empty response")
                    return

                start = result_text.find("{")
                end = result_text.rfind("}") + 1

                if start == -1 or end == -1:
                    st.error("AI did not return valid JSON")
                    st.write(result_text)
                    return

                clean_json = result_text[start:end]
                result = json.loads(clean_json)

                st.success("Analysis Result")

                st.write("Sentiment:", result.get("sentiment"))
                st.write("Topic:", result.get("topic"))
                st.write("Intent:", result.get("intent"))
                st.write("Tone:", result.get("tone"))

                st.info(result.get("summary"))

            except Exception as e:
                st.error(f"Error: {e}")