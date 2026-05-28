import streamlit as st
import sys
import os

# Add the engine to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bhrt_engine import process, to_json

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="BHRT Engine",
    page_icon="🖤",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CUSTOM CSS - Dark Theme
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

    h1 {
        color: #e0e0e0 !important;
        font-weight: 700 !important;
        letter-spacing: -1px;
    }

    h2, h3 {
        color: #b0b0b0 !important;
        font-weight: 600 !important;
    }

    .stTextArea textarea {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 12px !important;
        color: #e0e0e0 !important;
        font-size: 16px !important;
        padding: 16px !important;
    }

    .stTextArea textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 2px rgba(99,102,241,0.2) !important;
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

    .stExpander {
        background: rgba(255,255,255,0.02) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 12px !important;
    }

    .stJson {
        background: rgba(0,0,0,0.3) !important;
        border-radius: 12px !important;
    }
</style>
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
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ============================================================
# INPUT SECTION
# ============================================================
st.markdown("""
<h3 style="color: #b0b0b0; margin-bottom: 16px;">
    📥 Input Text
</h3>
""", unsafe_allow_html=True)

st.markdown("""
<p style="color: rgba(255,255,255,0.4); font-size: 14px; margin-bottom: 12px;">
    Koi bhi text daalo — naam, phone, email, emotions sab hata ke sirf structure bachega.
    <br>English, Hindi, Hinglish — sab chalega.
</p>
""", unsafe_allow_html=True)

# Example texts
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
    index=0
)

if selected_example == "Custom":
    user_text = st.text_area(
        "Apna text yahan likho:",
        height=200,
        placeholder="Yahan apna text paste karo..."
    )
else:
    user_text = st.text_area(
        "Text:",
        value=example_texts[selected_example],
        height=200
    )

# ============================================================
# PROCESS BUTTON
# ============================================================
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    process_clicked = st.button("⚡ PROCESS KARO", use_container_width=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ============================================================
# OUTPUT SECTION
# ============================================================
if process_clicked and user_text.strip():
    with st.spinner("Identity strip ho rahi hai..."):
        result = process(user_text)

    st.markdown("""
    <div style="text-align: center; margin: 20px 0;">
        <h2 style="color: #6366f1;">✅ Output Ready</h2>
    </div>
    """, unsafe_allow_html=True)

    # --- STRUCTURE TEXT ---
    st.markdown("""
    <h3 style="color: #b0b0b0; margin-top: 24px;">
        📝 Structure Text (Identity Removed)
    </h3>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='output-box'>
        {result.structure_text if result.structure_text else '<i style="color: rgba(255,255,255,0.3);">(Sab identity thi, structure mein kuch nahi bacha)</i>'}
    </div>
    """, unsafe_allow_html=True)

    # --- METRICS ---
    st.markdown("""
    <h3 style="color: #b0b0b0; margin-top: 24px;">
        📊 Metrics
    </h3>
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

    # --- BEHAVIORAL PATTERN ---
    st.markdown("""
    <h3 style="color: #b0b0b0; margin-top: 24px;">
        🎯 Behavioral Pattern
    </h3>
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
        <div style='color: rgba(255,255,255,0.4); font-size: 12px; margin-top: 4px;'>
            Detected behavioral archetype
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- IDENTITY EVIDENCE ---
    st.markdown("""
    <h3 style="color: #b0b0b0; margin-top: 24px;">
        🔒 Identity Removed
    </h3>
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

    # Tags
    if result.identity_types_found:
        st.markdown("<div style='margin: 8px 0;'>", unsafe_allow_html=True)
        for tag in result.identity_types_found:
            st.markdown(f"<span class='tag'>{tag}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --- TOPIC DISTRIBUTION ---
    st.markdown("""
    <h3 style="color: #b0b0b0; margin-top: 24px;">
        📈 Topic Distribution
    </h3>
    """, unsafe_allow_html=True)

    for topic, score in result.topic_distribution.items():
        bar_width = int(score * 100)
        bar_color = '#6366f1' if score > 0 else 'rgba(255,255,255,0.1)'
        st.markdown(f"""
        <div style='margin: 8px 0;'>
            <div style='display: flex; justify-content: space-between; margin-bottom: 4px;'>
                <span style='color: rgba(255,255,255,0.6); font-size: 14px; text-transform: capitalize;'>{topic.replace("_", " ")}</span>
                <span style='color: #6366f1; font-size: 14px; font-weight: 600;'>{score:.1%}</span>
            </div>
            <div style='background: rgba(255,255,255,0.05); border-radius: 8px; height: 8px; overflow: hidden;'>
                <div style='background: linear-gradient(90deg, #6366f1, #8b5cf6); width: {bar_width}%; height: 100%; border-radius: 8px; transition: width 0.5s ease;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # --- IRREVERSIBILITY PROOF ---
    st.markdown("""
    <h3 style="color: #b0b0b0; margin-top: 24px;">
        🔐 Irreversibility Proof
    </h3>
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

    # --- FULL JSON ---
    with st.expander("📋 Full JSON Output (Developers ke liye)"):
        st.json({
            "structure_text": result.structure_text,
            "structure_tags": result.structure_tags,
            "semantic_vector": result.semantic_vector,
            "topic_distribution": result.topic_distribution,
            "behavioral_pattern": result.behavioral_pattern,
            "identity_tokens_found": result.identity_tokens_found,
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

elif process_clicked and not user_text.strip():
    st.warning("⚠️ Pehle text daalo, phir process karo.")

# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div class='footer'>
    <p>🖤 BHRT Identity Stripping Engine v1.0</p>
    <p>Created by J.B.S. Mandloi | MIT License</p>
    <p style="margin-top: 8px;">
        <a href="https://github.com/jitendrazmandloi-collab/bhrt-engine" target="_blank" style="color: #6366f1; text-decoration: none;">
            GitHub ↗
        </a>
    </p>
</div>
""", unsafe_allow_html=True)
