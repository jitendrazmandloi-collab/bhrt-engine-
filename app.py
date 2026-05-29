import streamlit as st
import sys
import os
import pandas as pd
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bhrt_engine_v2 import process, to_json, submit_feedback, get_memory_stats

st.set_page_config(
    page_title="BHRT Engine v2.0 | Self-Learning",
    page_icon="🖤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    .main {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #0f0f23 100%);
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #0f0f23 100%);
    }

    h1 { color: #e0e0e0 !important; font-weight: 700 !important; letter-spacing: -1px; }
    h2, h3 { color: #b0b0b0 !important; font-weight: 600 !important; }

    .stTextArea textarea {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 12px !important;
        color: #e0e0e0 !important;
        font-size: 16px !important;
        padding: 16px !important;
    }

    .stButton button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 32px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
    }

    .metric-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 20px;
        margin: 8px 0;
    }

    .output-box {
        background: rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 20px;
        margin: 12px 0;
        font-family: 'Courier New', monospace;
    }

    .tag {
        display: inline-block;
        background: rgba(99,102,241,0.2);
        color: #a5b4fc;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        margin: 4px;
        border: 1px solid rgba(99,102,241,0.3);
    }

    .learned-tag {
        display: inline-block;
        background: rgba(34,197,94,0.2);
        color: #86efac;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        margin: 4px;
        border: 1px solid rgba(34,197,94,0.3);
    }

    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        margin: 24px 0;
    }

    .footer {
        text-align: center;
        color: rgba(255,255,255,0.3);
        font-size: 12px;
        margin-top: 40px;
        padding: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR - Memory Stats
# ============================================================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h2 style="color: #6366f1; font-size: 1.5em;">🖤 BHRT v2.0</h2>
        <p style="color: rgba(255,255,255,0.4); font-size: 12px;">Self-Learning Engine</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Memory stats
    st.markdown("""
    <h4 style="color: #b0b0b0; margin-bottom: 12px;">🧠 Memory Stats</h4>
    """, unsafe_allow_html=True)

    try:
        stats = get_memory_stats()
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Learned Words", stats['learned_words'])
        with col2:
            st.metric("Patterns", stats['learned_patterns'])

        col3, col4 = st.columns(2)
        with col3:
            st.metric("Rules", stats['context_rules'])
        with col4:
            st.metric("Processed", stats['total_processed'])

        st.markdown(f"<p style='color: rgba(255,255,255,0.4); font-size: 12px;'>Version: {stats['version']}</p>", unsafe_allow_html=True)
    except:
        st.info("Memory not initialized yet. Process some text first.")

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Feedback section
    st.markdown("""
    <h4 style="color: #b0b0b0; margin-bottom: 12px;">💡 Feedback</h4>
    <p style="color: rgba(255,255,255,0.4); font-size: 12px; margin-bottom: 12px;">
        System ko sikhao. Word daalo jo identity tha par system ne nahi pakda.
    </p>
    """, unsafe_allow_html=True)

    feedback_word = st.text_input("Word:", placeholder="e.g., gf, bhai, office")
    feedback_category = st.selectbox("Category:", [
        "relationship", "explicit_activity", "trauma_reaction", 
        "violence_marker", "social_identity", "activity_location"
    ])

    if st.button("🎓 Teach System", use_container_width=True) and feedback_word:
        result = submit_feedback(feedback_word, feedback_category)
        st.success(result)
        st.rerun()

# ============================================================
# HEADER
# ============================================================
st.markdown("""
<div style="text-align: center; padding: 20px 0;">
    <h1 style="font-size: 2.5em; margin-bottom: 0;">
        <span style="color: #6366f1;">BHRT</span> Engine <span style="color: #22c55e; font-size: 0.5em;">v2.0</span>
    </h1>
    <p style="color: rgba(255,255,255,0.5); font-size: 1.1em; margin-top: 8px;">
        🖤 Pattern se identity hatao. Structure bachao. System seekho.
    </p>
    <p style="color: rgba(255,255,255,0.3); font-size: 14px; margin-top: 4px;">
        Self-Learning | Context-Aware | User-Trainable
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ============================================================
# TABS
# ============================================================
tab1, tab2, tab3 = st.tabs(["✍️ Single Text", "📁 CSV Bulk", "🧠 Memory"])

# ============================================================
# TAB 1: SINGLE TEXT
# ============================================================
with tab1:
    st.markdown("""
    <h3 style="color: #b0b0b0; margin-bottom: 16px;">📥 Input Text</h3>
    <p style="color: rgba(255,255,255,0.4); font-size: 14px; margin-bottom: 12px;">
        Koi bhi text daalo — system static rules + learned memory dono use karega.
        <br>Feedback do — system seekhta jayega.
    </p>
    """, unsafe_allow_html=True)

    example_texts = {
        "English (Professional)": """My name is Priya Sharma and I am 28 years old. I work as a project manager 
at a tech company in Bangalore. Yesterday, I had a terrible meeting with 
my client Mr. Gupta. I felt frustrated and angry because the deadline was 
moved again. My phone is +919876543210 and email is priya.s@email.com.
We discussed the project timeline for 3 months. The budget was Rs.25,00,000.""",

        "Hinglish (Personal - Test Learning)": """Me or meri gf dono sath me ghum rahe the or or ek bhalu dikh gya 
jo sex kre the vo bhi bhalu hum bhag gye fir""",

        "Hinglish (Emotional)": """Main aaj bahut udaas hoon. Kal mujhe office mein gussa aaya tha.
Mera boss ne mujhe daanta. Maine socha ki shayad meri galti thi.
Mujhe lagta hai main fail ho gaya. Mera phone 9876543210 hai.
Main Mumbai mein rehta hoon. Abhi tak main thak gaya hoon.""",

        "Custom": ""
    }

    selected_example = st.selectbox(
        "Example chuno ya custom likho:",
        list(example_texts.keys()),
        index=1,  # Default to the test case
        key="single_select"
    )

    if selected_example == "Custom":
        user_text = st.text_area(
            "Apna text yahan likho:",
            height=200,
            placeholder="Yahan apna text paste karo...",
            key="single_custom"
        )
    else:
        user_text = st.text_area(
            "Text:",
            value=example_texts[selected_example],
            height=200,
            key="single_example"
        )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        process_single = st.button("⚡ PROCESS KARO", use_container_width=True, key="single_btn")

    if process_single and user_text.strip():
        with st.spinner("Static rules + Learned memory scan ho rahi hai..."):
            result = process(user_text)

        st.markdown("""
        <div style="text-align: center; margin: 20px 0;">
            <h2 style="color: #6366f1;">✅ Output Ready</h2>
        </div>
        """, unsafe_allow_html=True)

        # Structure Text
        st.markdown("""
        <h3 style="color: #b0b0b0; margin-top: 24px;">📝 Structure Text</h3>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class='output-box'>
            {result.structure_text if result.structure_text else '<i style="color: rgba(255,255,255,0.3);">(Sab identity thi, structure mein kuch nahi bacha)</i>'}
        </div>
        """, unsafe_allow_html=True)

        # Identity Evidence
        st.markdown("""
        <h3 style="color: #b0b0b0; margin-top: 24px;">🔒 Identity Removed</h3>
        """, unsafe_allow_html=True)

        col_i1, col_i2, col_i3 = st.columns(3)
        with col_i1:
            st.markdown(f"""
            <div class='metric-card' style='text-align: center;'>
                <div style='font-size: 2em; font-weight: 700; color: #ef4444;'>{result.identity_tokens_found}</div>
                <div style='color: rgba(255,255,255,0.5); font-size: 12px;'>Total Tokens Stripped</div>
            </div>
            """, unsafe_allow_html=True)
        with col_i2:
            st.markdown(f"""
            <div class='metric-card' style='text-align: center;'>
                <div style='font-size: 2em; font-weight: 700; color: #22c55e;'>{result.learned_words_used}</div>
                <div style='color: rgba(255,255,255,0.5); font-size: 12px;'>Learned Words Used</div>
            </div>
            """, unsafe_allow_html=True)
        with col_i3:
            st.markdown(f"""
            <div class='metric-card' style='text-align: center;'>
                <div style='font-size: 2em; font-weight: 700; color: #f59e0b;'>{len(result.context_rules_triggered)}</div>
                <div style='color: rgba(255,255,255,0.5); font-size: 12px;'>Context Rules Triggered</div>
            </div>
            """, unsafe_allow_html=True)

        # Tags
        if result.identity_types_found:
            st.markdown("<p style='color: rgba(255,255,255,0.5); font-size: 12px; margin-bottom: 8px;'>Identity Types Found:</p>", unsafe_allow_html=True)
            for tag in result.identity_types_found:
                st.markdown(f"<span class='tag'>{tag}</span>", unsafe_allow_html=True)

        if result.context_rules_triggered:
            st.markdown("<p style='color: rgba(255,255,255,0.5); font-size: 12px; margin: 12px 0 8px 0;'>Context Rules:</p>", unsafe_allow_html=True)
            for rule in result.context_rules_triggered:
                st.markdown(f"<span class='learned-tag'>{rule}</span>", unsafe_allow_html=True)

        # Metrics
        st.markdown("""
        <h3 style="color: #b0b0b0; margin-top: 24px;">📊 Metrics</h3>
        """, unsafe_allow_html=True)

        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.markdown(f"""
            <div class='metric-card' style='text-align: center;'>
                <div style='font-size: 2em; font-weight: 700; color: #6366f1;'>{result.privacy_score:.0f}</div>
                <div style='color: rgba(255,255,255,0.5); font-size: 14px;'>Privacy Score /100</div>
            </div>
            """, unsafe_allow_html=True)
        with col_m2:
            st.markdown(f"""
            <div class='metric-card' style='text-align: center;'>
                <div style='font-size: 2em; font-weight: 700; color: #8b5cf6;'>{result.utility_score:.0f}</div>
                <div style='color: rgba(255,255,255,0.5); font-size: 14px;'>Utility Score /100</div>
            </div>
            """, unsafe_allow_html=True)
        with col_m3:
            st.markdown(f"""
            <div class='metric-card' style='text-align: center;'>
                <div style='font-size: 2em; font-weight: 700; color: #a78bfa;'>{result.bhrt_score:.0f}</div>
                <div style='color: rgba(255,255,255,0.5); font-size: 14px;'>BHRT Score /100</div>
            </div>
            """, unsafe_allow_html=True)

        # Behavioral Pattern
        st.markdown("""
        <h3 style="color: #b0b0b0; margin-top: 24px;">🎯 Behavioral Pattern</h3>
        """, unsafe_allow_html=True)

        pattern_colors = {
            'CONFLICT_PROFESSIONAL': '#ef4444',
            'GROWTH_LEARNING': '#22c55e',
            'LEADERSHIP_EXECUTION': '#3b82f6',
            'CRISIS_MANAGEMENT': '#f59e0b',
            'STAKEHOLDER_NEGOTIATION': '#8b5cf6',
            'TRAUMA_NARRATIVE': '#dc2626',
            'RELATIONSHIP_INTIMATE': '#ec4899',
            'EXPLICIT_CONTENT': '#7c3aed',
            'GENERAL_UNSTRUCTURED': '#6b7280'
        }

        pattern_color = pattern_colors.get(result.behavioral_pattern, '#6b7280')
        st.markdown(f"""
        <div class='metric-card' style='text-align: center; border-left: 4px solid {pattern_color};'>
            <div style='font-size: 1.5em; font-weight: 700; color: {pattern_color};'>
                {result.behavioral_pattern}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Topic Distribution
        st.markdown("""
        <h3 style="color: #b0b0b0; margin-top: 24px;">📈 Topic Distribution</h3>
        """, unsafe_allow_html=True)

        for topic, score in result.topic_distribution.items():
            bar_width = int(score * 100)
            st.markdown(f"""
            <div style='margin: 8px 0;'>
                <div style='display: flex; justify-content: space-between; margin-bottom: 4px;'>
                    <span style='color: rgba(255,255,255,0.6); font-size: 14px; text-transform: capitalize;'>{topic.replace("_", " ")}</span>
                    <span style='color: #6366f1; font-size: 14px; font-weight: 600;'>{score:.1%}</span>
                </div>
                <div style='background: rgba(255,255,255,0.05); border-radius: 8px; height: 8px; overflow: hidden;'>
                    <div style='background: linear-gradient(90deg, #6366f1, #8b5cf6); width: {bar_width}%; height: 100%; border-radius: 8px;'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Irreversibility
        st.markdown("""
        <h3 style="color: #b0b0b0; margin-top: 24px;">🔐 Irreversibility Proof</h3>
        """, unsafe_allow_html=True)

        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1:
            st.markdown(f"""
            <div class='metric-card' style='text-align: center;'>
                <div style='font-size: 1.5em;'>🔒</div>
                <div style='color: #22c55e; font-weight: 600;'>Salt Destroyed</div>
                <div style='color: rgba(255,255,255,0.4); font-size: 12px;'>{result.salt_destroyed}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_p2:
            st.markdown(f"""
            <div class='metric-card' style='text-align: center;'>
                <div style='font-size: 1.5em;'>🛡️</div>
                <div style='color: #22c55e; font-weight: 600;'>VPS Impossible</div>
                <div style='color: rgba(255,255,255,0.4); font-size: 12px;'>{result.vps_impossible}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_p3:
            st.markdown(f"""
            <div class='metric-card' style='text-align: center;'>
                <div style='font-size: 1.5em;'>🆔</div>
                <div style='color: #6366f1; font-weight: 600;'>Processing ID</div>
                <div style='color: rgba(255,255,255,0.4); font-size: 10px;'>{result.processing_id[:8]}...</div>
            </div>
            """, unsafe_allow_html=True)

        # Feedback prompt
        st.markdown("""
        <div style='background: rgba(245,158,11,0.1); border: 1px solid rgba(245,158,11,0.3); border-radius: 12px; padding: 16px; margin: 24px 0;'>
            <h4 style='color: #f59e0b; margin: 0 0 8px 0;'>💡 Help System Learn</h4>
            <p style='color: rgba(255,255,255,0.6); font-size: 14px; margin: 0;'>
                Koi word miss hua? Sidebar mein jao → Feedback section mein word aur category daalo → System seekh jayega.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Full JSON
        with st.expander("📋 Full JSON Output"):
            st.json({
                "structure_text": result.structure_text,
                "structure_tags": result.structure_tags,
                "semantic_vector": result.semantic_vector,
                "topic_distribution": result.topic_distribution,
                "behavioral_pattern": result.behavioral_pattern,
                "identity_tokens_found": result.identity_tokens_found,
                "learned_words_used": result.learned_words_used,
                "context_rules_triggered": result.context_rules_triggered,
                "identity_types_found": result.identity_types_found,
                "pii_types_removed": result.pii_types_removed,
                "i_identity": result.i_identity,
                "i_pattern": result.i_pattern,
                "i_noise": result.i_noise,
                "privacy_score": result.privacy_score,
                "utility_score": result.utility_score,
                "bhrt_score": result.bhrt_score,
                "identity_hash": result.identity_hash[:16] + "...",
                "salt_destroyed": result.salt_destroyed,
                "vps_impossible": result.vps_impossible,
                "processing_id": result.processing_id,
                "language_detected": result.language_detected,
                "input_length": result.input_length,
                "output_length": result.output_length,
            })

    elif process_single and not user_text.strip():
        st.warning("⚠️ Pehle text daalo, phir process karo.")

# ============================================================
# TAB 2: CSV BULK (Same as v1 with learning stats)
# ============================================================
with tab2:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h2 style="color: #6366f1;">📁 B2B Bulk Processing</h2>
        <p style="color: rgba(255,255,255,0.5); font-size: 14px;">
            CSV upload karo — system har row se seekhega
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Sample CSV
    sample_data = {
        'text': [
            'My name is Rajesh and I am very sad today. My phone is 9876543210.',
            'Main aaj bahut khush hoon. Mera email rajesh@test.com hai.',
            'We had a meeting with the client in Mumbai. The budget was Rs.50000.',
            'Mujhe lagta hai main fail ho gaya. Mera boss ne mujhe daanta.',
            'Yesterday I felt angry and frustrated at work. My location is Delhi.',
            'Me or meri gf dono sath me ghum rahe the or or ek bhalu dikh gya.',
            'Dr. Sharma told me I need to take rest. My age is 45 years old.',
            'Hamare team mein 5 log hain. Project deadline next week hai.',
            'I think this is a horrible mistake. Probably we can fix it tomorrow.',
            'Mera PAN number ABCDE1234F hai. Main Bangalore mein job karta hoon.',
        ]
    }
    sample_df = pd.DataFrame(sample_data)
    sample_csv = sample_df.to_csv(index=False).encode('utf-8')

    col_dl1, col_dl2, col_dl3 = st.columns([1, 2, 1])
    with col_dl2:
        st.download_button(
            label="📥 Sample CSV Download",
            data=sample_csv,
            file_name='bhrt_sample.csv',
            mime='text/csv',
            use_container_width=True
        )

    uploaded_file = st.file_uploader(
        "Apna CSV file yahan upload karo:",
        type=['csv'],
        help="CSV file jisme text data ho. Max 10MB."
    )

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"✅ CSV loaded! {len(df)} rows, {len(df.columns)} columns.")

            text_columns = df.select_dtypes(include=['object']).columns.tolist()

            if not text_columns:
                st.error("❌ CSV mein koi text column nahi mila.")
            else:
                selected_column = st.selectbox(
                    "Kaunsa column process karna hai?",
                    text_columns,
                    index=0
                )

                preview_df = df[[selected_column]].head()
                st.dataframe(preview_df, use_container_width=True)

                col_p1, col_p2, col_p3 = st.columns([1, 2, 1])
                with col_p2:
                    process_bulk = st.button(
                        f"⚡ PROCESS ALL {len(df)} ROWS",
                        use_container_width=True,
                        key="bulk_btn"
                    )

                if process_bulk:
                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    results = []

                    for idx, row in df.iterrows():
                        text = str(row[selected_column])

                        if text and text != 'nan':
                            result = process(text)
                            results.append({
                                'original_text': text,
                                'structure_text': result.structure_text,
                                'behavioral_pattern': result.behavioral_pattern,
                                'privacy_score': result.privacy_score,
                                'utility_score': result.utility_score,
                                'bhrt_score': result.bhrt_score,
                                'learned_words_used': result.learned_words_used,
                                'context_rules_triggered': ', '.join(result.context_rules_triggered) if result.context_rules_triggered else 'None',
                                'identity_tokens_found': result.identity_tokens_found,
                                'identity_types_found': ', '.join(result.identity_types_found),
                                'pii_types_removed': ', '.join(result.pii_types_removed) if result.pii_types_removed else 'None',
                                'language_detected': result.language_detected,
                                'processing_id': result.processing_id,
                            })
                        else:
                            results.append({
                                'original_text': text,
                                'structure_text': '',
                                'behavioral_pattern': 'EMPTY',
                                'privacy_score': 0,
                                'utility_score': 0,
                                'bhrt_score': 0,
                                'learned_words_used': 0,
                                'context_rules_triggered': 'None',
                                'identity_tokens_found': 0,
                                'identity_types_found': '',
                                'pii_types_removed': '',
                                'language_detected': 'unknown',
                                'processing_id': '',
                            })

                        progress = (idx + 1) / len(df)
                        progress_bar.progress(min(progress, 1.0))
                        status_text.text(f"Processing row {idx + 1} of {len(df)}... Learning...")

                    progress_bar.empty()
                    status_text.empty()

                    results_df = pd.DataFrame(results)

                    # Summary
                    st.markdown("""
                    <div style="text-align: center; margin: 20px 0;">
                        <h2 style="color: #22c55e;">✅ All Rows Processed & Learned!</h2>
                    </div>
                    """, unsafe_allow_html=True)

                    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
                    with col_s1:
                        avg_privacy = results_df['privacy_score'].mean()
                        st.metric("Avg Privacy", f"{avg_privacy:.0f}/100")
                    with col_s2:
                        avg_utility = results_df['utility_score'].mean()
                        st.metric("Avg Utility", f"{avg_utility:.0f}/100")
                    with col_s3:
                        total_learned = results_df['learned_words_used'].sum()
                        st.metric("Learned Used", total_learned)
                    with col_s4:
                        top_pattern = results_df['behavioral_pattern'].value_counts().index[0]
                        st.metric("Top Pattern", top_pattern)

                    st.dataframe(results_df, use_container_width=True)

                    # Downloads
                    output_csv = results_df.to_csv(index=False).encode('utf-8')

                    col_d1, col_d2 = st.columns(2)
                    with col_d1:
                        st.download_button(
                            label="📥 Download Full CSV",
                            data=output_csv,
                            file_name='bhrt_v2_processed.csv',
                            mime='text/csv',
                            use_container_width=True
                        )

                    with col_d2:
                        summary_df = results_df[[
                            'structure_text', 'behavioral_pattern', 
                            'privacy_score', 'bhrt_score', 'learned_words_used'
                        ]]
                        summary_csv = summary_df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="📥 Download Summary",
                            data=summary_csv,
                            file_name='bhrt_v2_summary.csv',
                            mime='text/csv',
                            use_container_width=True
                        )

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("💡 Tip: CSV UTF-8 encoding mein honi chahiye.")

# ============================================================
# TAB 3: MEMORY VIEW
# ============================================================
with tab3:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h2 style="color: #6366f1;">🧠 System Memory</h2>
        <p style="color: rgba(255,255,255,0.5); font-size: 14px;">
            Jo system ne abhi tak seekha hai
        </p>
    </div>
    """, unsafe_allow_html=True)

    try:
        memory = json.load(open(os.path.join(os.path.dirname(__file__), 'bhrt_memory.json'), 'r', encoding='utf-8'))

        # Stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Learned Words", len(memory.get('learned_words', {})))
        with col2:
            st.metric("Patterns", len(memory.get('learned_patterns', {})))
        with col3:
            st.metric("Context Rules", len(memory.get('context_rules', {})))
        with col4:
            st.metric("User Corrections", len(memory.get('user_feedback', {}).get('corrections', [])))

        # Learned words table
        st.markdown("""
        <h3 style="color: #b0b0b0; margin-top: 24px;">📚 Learned Words</h3>
        """, unsafe_allow_html=True)

        learned = memory.get('learned_words', {})
        if learned:
            learned_df = pd.DataFrame([
                {'word': k, 'category': v['category'], 'confidence': v['confidence'], 'seen': v['seen'], 'lang': v.get('lang', 'unknown')}
                for k, v in learned.items()
            ])
            st.dataframe(learned_df.sort_values('seen', ascending=False), use_container_width=True)
        else:
            st.info("Abhi koi learned words nahi. System process karte waqt seekhega.")

        # Patterns
        st.markdown("""
        <h3 style="color: #b0b0b0; margin-top: 24px;">🔗 Learned Patterns</h3>
        """, unsafe_allow_html=True)

        patterns = memory.get('learned_patterns', {})
        if patterns:
            patterns_df = pd.DataFrame([
                {'pattern': k, 'category': v['category'], 'confidence': v['confidence'], 'seen': v['seen']}
                for k, v in patterns.items()
            ])
            st.dataframe(patterns_df, use_container_width=True)
        else:
            st.info("Abhi koi patterns nahi.")

        # Context rules
        st.markdown("""
        <h3 style="color: #b0b0b0; margin-top: 24px;">⚡ Context Rules</h3>
        """, unsafe_allow_html=True)

        rules = memory.get('context_rules', {})
        if rules:
            rules_df = pd.DataFrame([
                {'rule': k, 'action': v['action'], 'priority': v['priority'], 'reason': v['reason']}
                for k, v in rules.items()
            ])
            st.dataframe(rules_df, use_container_width=True)
        else:
            st.info("Abhi koi context rules nahi.")

        # User feedback
        st.markdown("""
        <h3 style="color: #b0b0b0; margin-top: 24px;">💡 User Feedback History</h3>
        """, unsafe_allow_html=True)

        corrections = memory.get('user_feedback', {}).get('corrections', [])
        if corrections:
            corrections_df = pd.DataFrame(corrections)
            st.dataframe(corrections_df, use_container_width=True)
        else:
            st.info("Abhi koi user feedback nahi.")

    except Exception as e:
        st.error(f"Memory load error: {e}")
        st.info("Pehle kuch text process karo — memory initialize hogi.")

# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div class='footer'>
    <p>🖤 BHRT Identity Stripping Engine v2.0 | Self-Learning</p>
    <p>Created by J.B.S. Mandloi | Apache 2.0 License</p>
    <p style="margin-top: 8px;">
        <a href="https://github.com/jitendrazmandloi-collab/bhrt-engine" target="_blank" style="color: #6366f1; text-decoration: none;">
            GitHub ↗
        </a>
    </p>
</div>
""", unsafe_allow_html=True)
