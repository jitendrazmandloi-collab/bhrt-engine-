import streamlit as st
import sys
import os
import pandas as pd
import io

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bhrt_engine import process, to_json

st.set_page_config(
    page_title="BHRT Engine | B2B Bulk Processing",
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
        transition: all 0.3s ease !important;
    }

    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(99,102,241,0.4) !important;
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

    .upload-box {
        background: rgba(99,102,241,0.05);
        border: 2px dashed rgba(99,102,241,0.3);
        border-radius: 16px;
        padding: 40px;
        text-align: center;
        margin: 20px 0;
    }

    .download-btn {
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%) !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.03);
        border-radius: 8px;
        padding: 12px 24px;
        color: rgba(255,255,255,0.6);
    }

    .stTabs [aria-selected="true"] {
        background: rgba(99,102,241,0.2) !important;
        color: #a5b4fc !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h2 style="color: #6366f1; font-size: 1.5em;">🖤 BHRT</h2>
        <p style="color: rgba(255,255,255,0.4); font-size: 12px;">B2B Bulk Processing</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div style="padding: 16px;">
        <h4 style="color: #b0b0b0; margin-bottom: 12px;">📊 Stats</h4>
        <div style="color: rgba(255,255,255,0.5); font-size: 14px; line-height: 2;">
            <div>✅ Identity Stripping</div>
            <div>✅ PII Detection</div>
            <div>✅ Behavioral Patterns</div>
            <div>✅ CSV Bulk Processing</div>
            <div>✅ Multilingual (EN/HI)</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div style="padding: 16px;">
        <h4 style="color: #b0b0b0; margin-bottom: 12px;">🔗 Links</h4>
        <div style="font-size: 14px;">
            <a href="https://github.com/jitendrazmandloi-collab/bhrt-engine" target="_blank" style="color: #6366f1; text-decoration: none;">GitHub ↗</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================
st.markdown("""
<div style="text-align: center; padding: 20px 0;">
    <h1 style="font-size: 2.5em; margin-bottom: 0;">
        <span style="color: #6366f1;">BHRT</span> Engine
    </h1>
    <p style="color: rgba(255,255,255,0.5); font-size: 1.1em; margin-top: 8px;">
        🖤 Pattern se identity hatao. Structure bachao.
    </p>
    <p style="color: rgba(255,255,255,0.3); font-size: 14px; margin-top: 4px;">
        B2B Bulk Processing | Privacy-First | Enterprise Ready
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ============================================================
# TABS: Single vs Bulk
# ============================================================
tab1, tab2 = st.tabs(["✍️ Single Text", "📁 CSV Bulk Upload"])

# ============================================================
# TAB 1: SINGLE TEXT (Original)
# ============================================================
with tab1:
    st.markdown("""
    <h3 style="color: #b0b0b0; margin-bottom: 16px;">📥 Input Text</h3>
    <p style="color: rgba(255,255,255,0.4); font-size: 14px; margin-bottom: 12px;">
        Koi bhi text daalo — naam, phone, email, emotions sab hata ke sirf structure bachega.
    </p>
    """, unsafe_allow_html=True)

    example_texts = {
        "English (Professional)": """My name is Priya Sharma and I am 28 years old. I work as a project manager 
at a tech company in Bangalore. Yesterday, I had a terrible meeting with 
my client Mr. Gupta. I felt frustrated and angry because the deadline was 
moved again. My phone is +919876543210 and email is priya.s@email.com.
We discussed the project timeline for 3 months. The budget was Rs.25,00,000.""",

        "Hinglish (Personal)": """Main aaj bahut udaas hoon. Kal mujhe office mein gussa aaya tha.
Mera boss ne mujhe daanta. Maine socha ki shayad meri galti thi.
Mujhe lagta hai main fail ho gaya. Mera phone 9876543210 hai.
Main Mumbai mein rehta hoon. Abhi tak main thak gaya hoon.""",

        "Hindi": """मेरा नाम राजेश है। मैं 32 साल का हूँ। मुझे कल बहुत दुख हुआ।
मैं दिल्ली में रहता हूँ। मेरा फोन 9876543210 है।""",

        "Custom": ""
    }

    selected_example = st.selectbox(
        "Example chuno ya custom likho:",
        list(example_texts.keys()),
        index=0,
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
        with st.spinner("Identity strip ho rahi hai..."):
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

        # Identity Evidence
        st.markdown("""
        <h3 style="color: #b0b0b0; margin-top: 24px;">🔒 Identity Removed</h3>
        """, unsafe_allow_html=True)

        col_i1, col_i2 = st.columns(2)
        with col_i1:
            st.markdown(f"""
            <div class='metric-card'>
                <div style='color: rgba(255,255,255,0.5); font-size: 12px;'>Tokens Found & Removed</div>
                <div style='font-size: 2em; font-weight: 700; color: #ef4444;'>{result.identity_tokens_found}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_i2:
            st.markdown(f"""
            <div class='metric-card'>
                <div style='color: rgba(255,255,255,0.5); font-size: 12px;'>PII Types Removed</div>
                <div style='font-size: 1.2em; font-weight: 600; color: #f87171;'>
                    {', '.join(result.pii_types_removed) if result.pii_types_removed else 'None'}
                </div>
            </div>
            """, unsafe_allow_html=True)

        if result.identity_types_found:
            st.markdown("<div style='margin: 8px 0;'>", unsafe_allow_html=True)
            for tag in result.identity_types_found:
                st.markdown(f"<span class='tag'>{tag}</span>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

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

    elif process_single and not user_text.strip():
        st.warning("⚠️ Pehle text daalo, phir process karo.")

# ============================================================
# TAB 2: CSV BULK UPLOAD (B2B FEATURE)
# ============================================================
with tab2:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h2 style="color: #6366f1;">📁 B2B Bulk Processing</h2>
        <p style="color: rgba(255,255,255,0.5); font-size: 14px;">
            CSV upload karo — 1000 rows ek saath process hongi
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Upload Section
    st.markdown("""
    <h3 style="color: #b0b0b0; margin-bottom: 16px;">📤 Upload CSV</h3>
    <p style="color: rgba(255,255,255,0.4); font-size: 14px; margin-bottom: 12px;">
        CSV mein ek column hona chahiye jisme text hai. Column ka koi bhi naam ho sakta hai.
    </p>
    """, unsafe_allow_html=True)

    # Sample CSV download
    sample_data = {
        'text': [
            'My name is Rajesh and I am very sad today. My phone is 9876543210.',
            'Main aaj bahut khush hoon. Mera email rajesh@test.com hai.',
            'We had a meeting with the client in Mumbai. The budget was Rs.50000.',
            'Mujhe lagta hai main fail ho gaya. Mera boss ne mujhe daanta.',
            'Yesterday I felt angry and frustrated at work. My location is Delhi.'
        ]
    }
    sample_df = pd.DataFrame(sample_data)
    sample_csv = sample_df.to_csv(index=False).encode('utf-8')

    col_dl1, col_dl2, col_dl3 = st.columns([1, 2, 1])
    with col_dl2:
        st.download_button(
            label="📥 Sample CSV Download (Test ke liye)",
            data=sample_csv,
            file_name='bhrt_sample.csv',
            mime='text/csv',
            use_container_width=True
        )

    st.markdown("<div style='margin: 16px 0;'></div>", unsafe_allow_html=True)

    # File uploader
    uploaded_file = st.file_uploader(
        "Apna CSV file yahan upload karo:",
        type=['csv'],
        help="CSV file jisme text data ho. Max 10MB."
    )

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)

            st.success(f"✅ CSV loaded! {len(df)} rows, {len(df.columns)} columns.")

            # Column selection
            text_columns = df.select_dtypes(include=['object']).columns.tolist()

            if not text_columns:
                st.error("❌ CSV mein koi text column nahi mila. String/text columns hone chahiye.")
            else:
                selected_column = st.selectbox(
                    "Kaunsa column process karna hai?",
                    text_columns,
                    index=0
                )

                # Preview
                st.markdown("""
                <h4 style="color: #b0b0b0; margin-top: 16px;">👁️ Preview (First 5 rows)</h4>
                """, unsafe_allow_html=True)

                preview_df = df[[selected_column]].head()
                st.dataframe(preview_df, use_container_width=True)

                # Process button
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
                                'identity_tokens_found': result.identity_tokens_found,
                                'identity_types_found': ', '.join(result.identity_types_found),
                                'pii_types_removed': ', '.join(result.pii_types_removed) if result.pii_types_removed else 'None',
                                'language_detected': result.language_detected,
                                'processing_id': result.processing_id,
                                'salt_destroyed': result.salt_destroyed,
                                'vps_impossible': result.vps_impossible,
                            })
                        else:
                            results.append({
                                'original_text': text,
                                'structure_text': '',
                                'behavioral_pattern': 'EMPTY',
                                'privacy_score': 0,
                                'utility_score': 0,
                                'bhrt_score': 0,
                                'identity_tokens_found': 0,
                                'identity_types_found': '',
                                'pii_types_removed': '',
                                'language_detected': 'unknown',
                                'processing_id': '',
                                'salt_destroyed': False,
                                'vps_impossible': False,
                            })

                        progress = (idx + 1) / len(df)
                        progress_bar.progress(min(progress, 1.0))
                        status_text.text(f"Processing row {idx + 1} of {len(df)}...")

                    progress_bar.empty()
                    status_text.empty()

                    results_df = pd.DataFrame(results)

                    # Summary metrics
                    st.markdown("""
                    <div style="text-align: center; margin: 20px 0;">
                        <h2 style="color: #22c55e;">✅ All Rows Processed!</h2>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("""
                    <h3 style="color: #b0b0b0; margin-top: 24px;">📊 Bulk Summary</h3>
                    """, unsafe_allow_html=True)

                    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
                    with col_s1:
                        avg_privacy = results_df['privacy_score'].mean()
                        st.markdown(f"""
                        <div class='metric-card' style='text-align: center;'>
                            <div style='font-size: 2em; font-weight: 700; color: #6366f1;'>{avg_privacy:.0f}</div>
                            <div style='color: rgba(255,255,255,0.5); font-size: 12px;'>Avg Privacy Score</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with col_s2:
                        avg_utility = results_df['utility_score'].mean()
                        st.markdown(f"""
                        <div class='metric-card' style='text-align: center;'>
                            <div style='font-size: 2em; font-weight: 700; color: #8b5cf6;'>{avg_utility:.0f}</div>
                            <div style='color: rgba(255,255,255,0.5); font-size: 12px;'>Avg Utility Score</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with col_s3:
                        total_tokens = results_df['identity_tokens_found'].sum()
                        st.markdown(f"""
                        <div class='metric-card' style='text-align: center;'>
                            <div style='font-size: 2em; font-weight: 700; color: #ef4444;'>{total_tokens}</div>
                            <div style='color: rgba(255,255,255,0.5); font-size: 12px;'>Total Tokens Stripped</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with col_s4:
                        pattern_counts = results_df['behavioral_pattern'].value_counts()
                        top_pattern = pattern_counts.index[0] if len(pattern_counts) > 0 else 'N/A'
                        st.markdown(f"""
                        <div class='metric-card' style='text-align: center;'>
                            <div style='font-size: 1.2em; font-weight: 700; color: #f59e0b;'>{top_pattern}</div>
                            <div style='color: rgba(255,255,255,0.5); font-size: 12px;'>Top Pattern</div>
                        </div>
                        """, unsafe_allow_html=True)

                    # Pattern distribution
                    st.markdown("""
                    <h4 style="color: #b0b0b0; margin-top: 16px;">🎯 Pattern Distribution</h4>
                    """, unsafe_allow_html=True)

                    pattern_df = results_df['behavioral_pattern'].value_counts().reset_index()
                    pattern_df.columns = ['Pattern', 'Count']
                    st.bar_chart(pattern_df.set_index('Pattern'))

                    # Results table
                    st.markdown("""
                    <h4 style="color: #b0b0b0; margin-top: 16px;">📋 Full Results</h4>
                    """, unsafe_allow_html=True)

                    st.dataframe(results_df, use_container_width=True)

                    # Download buttons
                    st.markdown("""
                    <h3 style="color: #b0b0b0; margin-top: 24px;">💾 Download Results</h3>
                    """, unsafe_allow_html=True)

                    # CSV download
                    output_csv = results_df.to_csv(index=False).encode('utf-8')

                    col_d1, col_d2 = st.columns(2)
                    with col_d1:
                        st.download_button(
                            label="📥 Download Full CSV",
                            data=output_csv,
                            file_name='bhrt_processed_results.csv',
                            mime='text/csv',
                            use_container_width=True
                        )

                    with col_d2:
                        # Summary only
                        summary_df = results_df[[
                            'structure_text', 'behavioral_pattern', 
                            'privacy_score', 'bhrt_score', 'language_detected'
                        ]]
                        summary_csv = summary_df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="📥 Download Summary Only",
                            data=summary_csv,
                            file_name='bhrt_summary.csv',
                            mime='text/csv',
                            use_container_width=True
                        )

                    # JSON download
                    json_output = results_df.to_json(orient='records', indent=2)
                    st.download_button(
                        label="📥 Download JSON",
                        data=json_output,
                        file_name='bhrt_results.json',
                        mime='application/json',
                        use_container_width=True
                    )

        except Exception as e:
            st.error(f"❌ Error reading CSV: {str(e)}")
            st.info("💡 Tip: CSV file UTF-8 encoding mein honi chahiye. Excel se 'Save As CSV' karo.")

# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div class='footer'>
    <p>🖤 BHRT Identity Stripping Engine v1.0 | B2B Bulk Processing</p>
    <p>Created by J.B.S. Mandloi | MIT License</p>
    <p style="margin-top: 8px;">
        <a href="https://github.com/jitendrazmandloi-collab/bhrt-engine" target="_blank" style="color: #6366f1; text-decoration: none;">
            GitHub ↗
        </a>
    </p>
</div>
""", unsafe_allow_html=True)
