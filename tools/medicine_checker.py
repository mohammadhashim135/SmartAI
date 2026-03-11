import streamlit as st
import json
from tools.ai_client import call_ai


def medicine_checker():
    st.markdown("""
    <div class="tool-header">
        <span class="tool-icon">💊</span>
        <div>
            <h2>Medicine Safety Checker</h2>
            <p>Check medicine information, interactions, side effects, and safety precautions instantly.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""<div class="disclaimer-box">
        ⚕️ <strong>Medical Disclaimer:</strong> This tool provides general information only. 
        Always consult a licensed doctor or pharmacist before taking any medication.
    </div>""", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["💊 Single Medicine Info", "⚠️ Drug Interaction Check"])

    with tab1:
        medicine_name = st.text_input(
            "Enter medicine name",
            placeholder="e.g. Paracetamol, Ibuprofen, Metformin, Amoxicillin...",
            key="med_single"
        )

        col1, col2 = st.columns(2)

        with col1:
            age_group = st.selectbox(
                "Age group",
                ["Adult (18-60)", "Child (under 18)", "Elderly (60+)", "Pregnant"]
            )

        with col2:
            purpose = st.text_input(
                "Why are you taking it? (optional)",
                placeholder="e.g. headache, fever..."
            )

        if st.button("🔍 Check Medicine", type="primary", use_container_width=True, key="check_single"):

            if not medicine_name.strip():
                st.warning("Please enter a medicine name.")
                return

            with st.spinner(f"Looking up {medicine_name}..."):
                system = """
                You are a professional clinical pharmacist AI.

                Return ONLY JSON:

                {
                "name":"",
                "generic_name":"",
                "drug_class":"",
                "common_uses":["","",""],
                "how_it_works":"",
                "typical_dosage":"",
                "common_side_effects":["","",""],
                "serious_warnings":["",""],
                "contraindications":["",""],
                "foods_to_avoid":[""],
                "storage":"",
                "otc_or_prescription":"OTC | Prescription",
                "safety_rating":"SAFE | USE WITH CAUTION | HIGH RISK"
                }

                Rules:
                - Always fill all fields.
                - common_uses must contain at least 3 items.
                - common_side_effects must contain at least 3 items.
                """

                prompt = f"Provide complete safety information for: {medicine_name}. Patient is: {age_group}. Reason for use: {purpose or 'not specified'}."

                try:
                    result_text = call_ai(prompt, system)
                    result = json.loads(result_text)

                    safety = result.get("safety_rating", "USE WITH CAUTION")

                    if safety == "SAFE":
                        badge = "🟢"
                        card_class = "result-safe"
                    elif safety == "HIGH RISK":
                        badge = "🔴"
                        card_class = "result-danger"
                    else:
                        badge = "🟡"
                        card_class = "result-warning"

                    st.markdown(f"""
                    <div class="result-card {card_class}">
                        <h3>{badge} {result.get('name', medicine_name)} — {safety}</h3>
                        <p>
                        <strong>Generic:</strong> {result.get('generic_name', 'N/A')} &nbsp;|&nbsp;
                        <strong>Class:</strong> {result.get('drug_class', 'N/A')} &nbsp;|&nbsp;
                        <strong>Type:</strong> {result.get('otc_or_prescription', 'N/A')}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                    c1, c2 = st.columns(2)

                    with c1:
                        st.markdown("**✅ Common Uses:**")
                        for u in result.get("common_uses", []):
                            st.markdown(f"- {u}")

                        st.markdown(f"\n**💉 How it Works:**\n{result.get('how_it_works', '')}")

                        st.markdown(f"\n**📏 Typical Dosage ({age_group}):**\n{result.get('typical_dosage', 'Consult doctor')}")

                    with c2:
                        st.markdown("**⚠️ Common Side Effects:**")
                        for s in result.get("common_side_effects", []):
                            st.markdown(f"- {s}")

                        warnings = result.get("serious_warnings", [])

                        if warnings:
                            st.markdown("**🚨 Serious Warnings:**")
                            for w in warnings:
                                st.markdown(f"- {w}")

                    col3, col4 = st.columns(2)

                    with col3:
                        contra = result.get("contraindications", [])

                        if contra:
                            st.markdown("**🚫 Do NOT take if you have:**")
                            for c in contra:
                                st.markdown(f"- {c}")

                    with col4:
                        foods = result.get("foods_to_avoid", [])

                        if foods:
                            st.markdown("**🍽️ Foods/Drinks to Avoid:**")
                            for f in foods:
                                st.markdown(f"- {f}")

                    st.info(f"📦 **Storage:** {result.get('storage', 'Store in cool, dry place')}")

                except Exception as e:
                    st.error(f"Error: {e}")

    with tab2:

        st.markdown("**Enter two or more medicines to check for interactions:**")

        med1 = st.text_input("Medicine 1", placeholder="e.g. Aspirin", key="int_med1")
        med2 = st.text_input("Medicine 2", placeholder="e.g. Warfarin", key="int_med2")
        med3 = st.text_input("Medicine 3 (optional)", placeholder="e.g. Ibuprofen", key="int_med3")

        if st.button("⚠️ Check Interactions", type="primary", use_container_width=True, key="check_interaction"):

            meds = [m for m in [med1, med2, med3] if m.strip()]

            if len(meds) < 2:
                st.warning("Please enter at least 2 medicines.")
                return

            with st.spinner("Checking drug interactions..."):

                system = """You are a clinical pharmacist. Respond ONLY with valid JSON:
                {
                    "interaction_found": true | false,
                    "severity": "NONE" | "MINOR" | "MODERATE" | "MAJOR",
                    "summary": "<brief summary>",
                    "interactions": [
                        {"drugs": ["drug1", "drug2"], "effect": "<effect>", "severity": "MINOR|MODERATE|MAJOR"}
                    ],
                    "recommendation": "<what to do>"
                }"""

                prompt = f"Check drug interactions between: {', '.join(meds)}"

                try:
                    result_text = call_ai(prompt, system)
                    result = json.loads(result_text)

                    severity = result.get("severity", "NONE")

                    if severity == "MAJOR":
                        st.markdown(f"""
                        <div class="result-card result-danger">
                            <h3>🚨 MAJOR Interaction Found!</h3>
                            <p>{result.get('summary', '')}</p>
                        </div>
                        """, unsafe_allow_html=True)

                    elif severity == "MODERATE":
                        st.markdown(f"""
                        <div class="result-card result-warning">
                            <h3>⚠️ Moderate Interaction</h3>
                            <p>{result.get('summary', '')}</p>
                        </div>
                        """, unsafe_allow_html=True)

                    else:
                        st.markdown(f"""
                        <div class="result-card result-safe">
                            <h3>✅ No Significant Interaction</h3>
                            <p>{result.get('summary', '')}</p>
                        </div>
                        """, unsafe_allow_html=True)

                    for ix in result.get("interactions", []):
                        st.markdown(f"**{' + '.join(ix.get('drugs', []))}:** {ix.get('effect', '')}")

                    st.info(f"💡 **Recommendation:** {result.get('recommendation', '')}")

                except Exception as e:
                    st.error(f"Error: {e}")