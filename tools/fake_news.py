import streamlit as st
import json
from tools.ai_client import call_ai

def fake_news():
    st.markdown("""
    <div class="tool-header">
        <span class="tool-icon">📰</span>
        <div>
            <h2>Fake News Analyzer</h2>
            <p>Detect misinformation, analyze credibility, and understand the bias in news articles or claims.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    input_type = st.radio(
        "What do you want to analyze?",
        ["📝 News Headline / Claim", "📄 Full Article Text", "🔗 Analyze a Topic"],
        horizontal=True
    )

    if input_type == "📝 News Headline / Claim":
        content = st.text_input(
            "Enter headline or claim",
            placeholder="e.g. 'Scientists prove drinking lemon juice cures cancer'",
        )
        analyze_prompt = f"Analyze this news headline/claim for accuracy and misinformation: {content}"

    elif input_type == "📄 Full Article Text":
        content = st.text_area(
            "Paste article text",
            height=200,
            placeholder="Paste the full article or paragraph here..."
        )
        analyze_prompt = f"Analyze this news article for factual accuracy, bias, and misinformation indicators:\n\n{content}"

    else:
        content = st.text_input(
            "Enter a topic to check for common misinformation",
            placeholder="e.g. 'COVID-19 vaccines', '5G towers', 'climate change'"
        )
        analyze_prompt = f"What are common myths and misinformation about this topic, and what is the factual truth: {content}"

    col1, col2 = st.columns([2,1])
    with col1:
        analyze_btn = st.button("🔍 Analyze Now", type="primary", use_container_width=True)
    with col2:
        st.markdown("*AI analysis in seconds*")

    if analyze_btn:
        if not content or not content.strip():
            st.warning("Please enter content to analyze.")
            return

        with st.spinner("Analyzing credibility and checking for misinformation..."):
            system = """
            You are a professional fact-checking expert.

            Return ONLY JSON:

            {
            "credibility_score": 0-100,
            "verdict": "LIKELY TRUE | MISLEADING | PARTLY FALSE | LIKELY FALSE | UNVERIFIABLE",
            "confidence": "HIGH | MEDIUM | LOW",
            "summary": "2 sentence explanation",
            "red_flags": ["flag1","flag2"],
            "factual_elements": ["fact1","fact2"],
            "missing_context": "important missing context",
            "bias_detected": "LEFT | RIGHT | CENTER | SENSATIONALIST | NONE",
            "bias_explanation": "short explanation",
            "fact_check_tips": ["tip1","tip2"],
            "reliable_sources": ["WHO","BBC","Reuters","Scientific journals"]
            }

            Rules:
            - Always provide at least 2 red_flags if misleading.
            - Always give at least 2 fact_check_tips.
            """

            try:
                result_text = call_ai(analyze_prompt, system)
                result = json.loads(result_text)

                score = result.get("credibility_score", 50)
                verdict = result.get("verdict", "UNVERIFIABLE")

                if verdict in ["LIKELY FALSE"] or score < 30:
                    card_class = "result-danger"
                    emoji = "❌"
                elif verdict in ["MISLEADING", "PARTLY FALSE"] or score < 60:
                    card_class = "result-warning"
                    emoji = "⚠️"
                else:
                    card_class = "result-safe"
                    emoji = "✅"

                st.markdown(f"""<div class="result-card {card_class}">
                    <h3>{emoji} {verdict}</h3>
                    <p><strong>Credibility Score: {score}/100</strong> &nbsp;|&nbsp;
                       <strong>Confidence:</strong> {result.get('confidence', 'MEDIUM')}</p>
                    <p>{result.get('summary', '')}</p>
                </div>""", unsafe_allow_html=True)

                st.progress(score / 100)

                c1, c2 = st.columns(2)

                with c1:
                    flags = result.get("red_flags", [])
                    if flags:
                        st.markdown("**🚩 Misleading/False Elements:**")
                        for f in flags:
                            st.markdown(f"- {f}")

                    bias = result.get("bias_detected", "NONE")
                    bias_colors = {
                        "LEFT": "🔵", "RIGHT": "🔴", "CENTER": "⚪",
                        "SENSATIONALIST": "🟠", "NONE": "🟢"
                    }

                    st.markdown(f"\n**{bias_colors.get(bias,'⚪')} Bias Detected: {bias}**")

                    if result.get("bias_explanation"):
                        st.caption(result.get("bias_explanation"))

                with c2:
                    facts = result.get("factual_elements", [])

                    if facts:
                        st.markdown("**✅ Accurate Elements:**")
                        for f in facts:
                            st.markdown(f"- {f}")

                    missing = result.get("missing_context", "")

                    if missing:
                        st.markdown("**🔎 Missing Context:**")
                        st.markdown(missing)

                st.markdown("---")

                st.markdown("**🧠 How to Verify This Yourself:**")

                for tip in result.get("fact_check_tips", []):
                    st.markdown(f"- {tip}")

                sources = result.get("reliable_sources", [])

                if sources:
                    st.info(f"📚 **Check these sources:** {', '.join(sources)}")

            except Exception as e:
                st.error(f"Analysis error: {e}")