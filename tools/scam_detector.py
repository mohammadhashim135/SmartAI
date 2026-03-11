import streamlit as st
import json
from tools.ai_client import call_ai

def scam_detector():
    st.markdown("""
    <div class="tool-header">
        <span class="tool-icon">🔐</span>
        <div>
            <h2>Scam Message Detector</h2>
            <p>Paste any suspicious message — SMS, email, WhatsApp, or DM — and AI will analyze it for scam signals.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if "scam_input" not in st.session_state:
        st.session_state.scam_input = ""

    col1, col2 = st.columns([3, 1])

    with col1:
        message = st.text_area(
            "Paste your message here",
            value=st.session_state.scam_input,
            height=160,
            placeholder="e.g. 'Congratulations! You've won ₹50,000. Click here to claim: bit.ly/win50k. OTP: 847291'"
        )

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**Examples to try:**")

        if st.button("📧 Try Phishing Email", use_container_width=True):
            st.session_state.scam_input = "Dear customer, your bank account has been suspended. Click this link immediately to verify: http://secure-bank-verify.xyz. Enter your OTP to restore access."
            st.rerun()

        if st.button("💬 Try Safe Message", use_container_width=True):
            st.session_state.scam_input = "Hi! Just wanted to check if you're free for lunch tomorrow at 1pm? Let me know!"
            st.rerun()

        if st.button("🎁 Try Lottery Scam", use_container_width=True):
            st.session_state.scam_input = "Congratulations! You've won ₹5,00,000 in our lucky draw. Click this link to claim your prize now: bit.ly/win500k"
            st.rerun()

        if st.button("📦 Try Delivery Scam", use_container_width=True):
            st.session_state.scam_input = "Your package delivery failed. Please update your address immediately: http://delivery-update.xyz"
            st.rerun()

    if st.button("🔍 Analyze Message", type="primary", use_container_width=True):

        if not message.strip():
            st.warning("Please paste a message to analyze.")
            return

        with st.spinner("Analyzing message for scam signals..."):

            system = """
            You are a cybersecurity expert specializing in scam and phishing detection.

            Return ONLY valid JSON in this format:

            {
            "risk_level": "HIGH | MEDIUM | LOW",
            "risk_score": 0-100,
            "verdict": "one sentence explanation",
            "red_flags": ["flag1","flag2","flag3"],
            "safe_signals": ["signal1","signal2"],
            "recommendation": "what the user should do",
            "scam_type": "phishing | lottery scam | OTP fraud | fake link | not a scam"
            }
            """

            prompt = f"Analyze this message for scam/phishing indicators:\n\n{message}"

            try:
                result_text = call_ai(prompt, system)

                start = result_text.find("{")
                end = result_text.rfind("}") + 1
                clean_json = result_text[start:end]

                result = json.loads(clean_json)

                risk = result.get("risk_level", "UNKNOWN")
                score = result.get("risk_score", 0)

                if risk == "HIGH":
                    st.markdown(f"""
                    <div class="result-card result-danger">
                        <h3>⛔ HIGH RISK — Likely Scam</h3>
                        <p><strong>Type:</strong> {result.get('scam_type', 'Unknown')}</p>
                        <p>{result.get('verdict', '')}</p>
                    </div>
                    """, unsafe_allow_html=True)

                elif risk == "MEDIUM":
                    st.markdown(f"""
                    <div class="result-card result-warning">
                        <h3>⚠️ MEDIUM RISK — Suspicious</h3>
                        <p><strong>Type:</strong> {result.get('scam_type', 'Unknown')}</p>
                        <p>{result.get('verdict', '')}</p>
                    </div>
                    """, unsafe_allow_html=True)

                else:
                    st.markdown(f"""
                    <div class="result-card result-safe">
                        <h3>✅ LOW RISK — Looks Safe</h3>
                        <p><strong>Type:</strong> {result.get('scam_type', 'Not a scam')}</p>
                        <p>{result.get('verdict', '')}</p>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown(f"**Risk Score: {score}/100**")
                st.progress(score / 100)

                c1, c2 = st.columns(2)

                with c1:
                    flags = result.get("red_flags", [])
                    if flags:
                        st.markdown("**🚩 Red Flags Detected:**")
                        for f in flags:
                            st.markdown(f"- {f}")

                with c2:
                    safe = result.get("safe_signals", [])
                    if safe:
                        st.markdown("**✅ Safe Signals:**")
                        for s in safe:
                            st.markdown(f"- {s}")

                st.info(f"💡 **Recommendation:** {result.get('recommendation', '')}")

            except Exception as e:
                st.error(f"Analysis error: {e}")