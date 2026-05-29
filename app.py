import streamlit as st
import sys
import os
import pandas as pd
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bhrt_engine_v2 import process, to_json, get_memory_stats

st.set_page_config(
    page_title="BHRT Engine v2.0",
    page_icon="🖤",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Sora:wght@300;400;600;700&display=swap');

    html, body, .stApp {
        background: #080808 !important;
        font-family: 'Sora', sans-serif;
    }

    /* Hide Streamlit chrome */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 0.5rem 2rem 4rem 2rem; max-width: 1100px; margin: auto; }
    section[data-testid="stSidebar"] { display: none !important; }
    /* Remove default top gap */
    div[data-testid="stAppViewContainer"] > section > div:first-child { padding-top: 0 !important; }
    .stApp > header { height: 0 !important; }

    /* Typography */
    h1, h2, h3, h4, p, label, div { color: #e8e8e8 !important; }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: transparent;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        gap: 0;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: rgba(255,255,255,0.35) !important;
        font-family: 'Sora', sans-serif;
        font-size: 13px;
        font-weight: 500;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        padding: 12px 24px;
        border-bottom: 2px solid transparent;
    }
    .stTabs [aria-selected="true"] {
        color: #e8e8e8 !important;
        border-bottom: 2px solid #e8e8e8 !important;
        background: transparent !important;
    }
    .stTabs [data-baseweb="tab-highlight"] { display: none; }

    /* Textarea */
    .stTextArea textarea {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 8px !important;
        color: #e0e0e0 !important;
        font-family: 'DM Mono', monospace !important;
        font-size: 14px !important;
        padding: 16px !important;
        resize: vertical;
    }
    .stTextArea textarea:focus {
        border-color: rgba(255,255,255,0.25) !important;
        box-shadow: none !important;
    }

    /* Selectbox */
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 8px !important;
        color: #e0e0e0 !important;
    }

    /* Button */
    .stButton > button {
        background: #e8e8e8 !important;
        color: #080808 !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 10px 28px !important;
        font-family: 'Sora', sans-serif !important;
        font-weight: 700 !important;
        font-size: 13px !important;
        letter-spacing: 0.05em !important;
        min-width: 120px !important;
        transition: opacity 0.2s !important;
    }
    .stButton > button:hover { opacity: 0.82 !important; }

    /* Download button */
    .stDownloadButton > button {
        background: transparent !important;
        color: rgba(255,255,255,0.5) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 6px !important;
        font-family: 'Sora', sans-serif !important;
        font-size: 12px !important;
        padding: 8px 18px !important;
    }
    .stDownloadButton > button:hover {
        border-color: rgba(255,255,255,0.3) !important;
        color: rgba(255,255,255,0.8) !important;
    }

    /* Metric */
    [data-testid="stMetric"] { background: transparent; }
    [data-testid="stMetricValue"] {
        font-family: 'DM Mono', monospace !important;
        font-size: 1.8rem !important;
        color: #e8e8e8 !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 11px !important;
        color: rgba(255,255,255,0.35) !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    /* Progress */
    .stProgress > div > div > div { background: #e8e8e8 !important; }

    /* Dataframe */
    .stDataFrame { border: 1px solid rgba(255,255,255,0.07); border-radius: 8px; }

    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.02) !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
        border-radius: 8px !important;
        color: rgba(255,255,255,0.5) !important;
        font-size: 12px;
    }

    /* Card */
    .card {
        background: rgba(255,255,255,0.025);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 10px;
        padding: 20px 24px;
        margin: 8px 0;
    }

    /* Output text box */
    .output-text {
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 8px;
        padding: 20px 24px;
        font-family: 'DM Mono', monospace;
        font-size: 13px;
        line-height: 1.7;
        color: rgba(255,255,255,0.75);
    }

    /* Label */
    .label {
        display: inline-block;
        font-family: 'DM Mono', monospace;
        font-size: 11px;
        color: rgba(255,255,255,0.4);
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 4px;
        padding: 3px 9px;
        margin: 3px 4px 3px 0;
        letter-spacing: 0.03em;
    }

    /* Pattern badge */
    .pattern-badge {
        display: inline-block;
        font-family: 'DM Mono', monospace;
        font-size: 12px;
        font-weight: 500;
        padding: 6px 14px;
        border-radius: 5px;
        letter-spacing: 0.05em;
    }

    /* Section divider */
    .sect-divider {
        height: 1px;
        background: rgba(255,255,255,0.06);
        margin: 32px 0;
    }

    /* Stat row */
    .stat-number {
        font-family: 'DM Mono', monospace;
        font-size: 2.4rem;
        font-weight: 500;
        color: #e8e8e8;
        line-height: 1;
    }
    .stat-label {
        font-size: 11px;
        color: rgba(255,255,255,0.3);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 6px;
    }

    /* Score bar */
    .score-track {
        background: rgba(255,255,255,0.06);
        border-radius: 4px;
        height: 6px;
        margin-top: 8px;
        overflow: hidden;
    }
    .score-fill {
        height: 100%;
        border-radius: 4px;
        background: #e8e8e8;
    }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════════
st.markdown("""
<div style="padding: 20px 0 24px 0;">
    <div style="display: flex; align-items: baseline; gap: 12px;">
        <span style="font-family: 'DM Mono', monospace; font-size: 11px; color: rgba(255,255,255,0.25); letter-spacing: 0.12em; text-transform: uppercase;">BHRT ENGINE</span>
        <span style="font-family: 'DM Mono', monospace; font-size: 11px; color: rgba(255,255,255,0.15);">v2.0</span>
    </div>
    <h1 style="font-size: 2.2rem; font-weight: 700; margin: 6px 0 0 0; letter-spacing: -0.03em; color: #e8e8e8 !important;">
        Behavioral Identity Stripping
    </h1>
    <p style="color: rgba(255,255,255,0.3) !important; font-size: 13px; margin: 6px 0 0 0; font-weight: 300;">
        Remove personal identity from text. Preserve structure and behavioral signal.
    </p>
</div>
<div class="sect-divider"></div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
#  TABS
# ══════════════════════════════════════════════════════
tab1, tab2, tab3 = st.tabs(["Single Text", "Bulk CSV", "System"])

# ══════════════════════════════════════════════════════
#  TAB 1: SINGLE TEXT
# ══════════════════════════════════════════════════════
with tab1:
    example_texts = {
        "English (Professional)": "My name is Priya Sharma and I am 28 years old. I work as a project manager at a tech company in Bangalore. Yesterday, I had a difficult meeting with my client Mr. Gupta. My phone is +919876543210 and email is priya.s@email.com.",
        "Hinglish (Emotional)": "Main aaj bahut udaas hoon. Kal mujhe office mein gussa aaya tha. Mera boss ne mujhe daanta. Mujhe lagta hai main fail ho gaya. Mera phone 9876543210 hai.",
        "Hinglish (Narrative)": "Hum dono sath ghum rahe the jab achanak ek janvar dikh gya. Hum wahan se nikal gaye. Bahut ajeeb experience tha.",
        "Custom": ""
    }

    col_sel, _ = st.columns([2, 3])
    with col_sel:
        selected = st.selectbox("Example:", list(example_texts.keys()), index=0, label_visibility="collapsed")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    user_text = st.text_area(
        "Text",
        value=example_texts[selected] if selected != "Custom" else "",
        height=160,
        label_visibility="collapsed",
        placeholder="Yahan apna text paste karo..."
    )

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    col_btn, _ = st.columns([1, 4])
    with col_btn:
        run = st.button("Process", key="single_run")

    if run and user_text.strip():
        with st.spinner(""):
            result = process(user_text)

        st.markdown("<div class='sect-divider'></div>", unsafe_allow_html=True)

        # ── Structure Text ──────────────────────────────
        st.markdown("<p style='font-size:11px; text-transform:uppercase; letter-spacing:0.1em; color:rgba(255,255,255,0.3); margin-bottom:8px;'>Structure Text</p>", unsafe_allow_html=True)
        if result.structure_text:
            st.markdown(f"<div class='output-text'>{result.structure_text}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='output-text' style='color:rgba(255,255,255,0.2);font-style:italic;'>No structure remaining — text was fully identity.</div>", unsafe_allow_html=True)

        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

        # ── Scores ──────────────────────────────────────
        st.markdown("<p style='font-size:11px; text-transform:uppercase; letter-spacing:0.1em; color:rgba(255,255,255,0.3); margin-bottom:16px;'>Scores</p>", unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        scores = [
            ("Privacy", result.privacy_score),
            ("Utility", result.utility_score),
            ("BHRT", result.bhrt_score),
        ]
        for col, (label, val) in zip([c1, c2, c3], scores):
            with col:
                st.markdown(f"""
                <div class="card">
                    <div class="stat-number">{val:.0f}</div>
                    <div class="stat-label">{label} / 100</div>
                    <div class="score-track"><div class="score-fill" style="width:{val}%;"></div></div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

        # ── Identity Removed ─────────────────────────────
        c4, c5 = st.columns([1, 2])
        with c4:
            st.markdown(f"""
            <div class="card" style="text-align:center;">
                <div class="stat-number" style="color:#e8e8e8;">{result.identity_tokens_found}</div>
                <div class="stat-label">tokens stripped</div>
            </div>
            """, unsafe_allow_html=True)
        with c5:
            st.markdown(f"""
            <div class="card">
                <div class="stat-label" style="margin-bottom:10px;">Behavioral Pattern</div>
                <span class="pattern-badge" style="background:rgba(255,255,255,0.06); color:#e8e8e8;">{result.behavioral_pattern}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

        # ── Topic Distribution ───────────────────────────
        st.markdown("<p style='font-size:11px; text-transform:uppercase; letter-spacing:0.1em; color:rgba(255,255,255,0.3); margin-bottom:12px;'>Topic Distribution</p>", unsafe_allow_html=True)
        for topic, score in result.topic_distribution.items():
            bar = int(score * 100)
            st.markdown(f"""
            <div style="margin:6px 0;">
                <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                    <span style="font-size:12px; color:rgba(255,255,255,0.45); text-transform:capitalize;">{topic.replace('_',' ')}</span>
                    <span style="font-family:'DM Mono',monospace; font-size:12px; color:rgba(255,255,255,0.5);">{score:.0%}</span>
                </div>
                <div class="score-track"><div class="score-fill" style="width:{bar}%; opacity:0.7;"></div></div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

        # ── Identity Types ───────────────────────────────
        if result.identity_types_found:
            st.markdown("<p style='font-size:11px; text-transform:uppercase; letter-spacing:0.1em; color:rgba(255,255,255,0.3); margin-bottom:8px;'>Identity Types Removed</p>", unsafe_allow_html=True)
            tags_html = "".join(f"<span class='label'>{t}</span>" for t in result.identity_types_found)
            st.markdown(tags_html, unsafe_allow_html=True)

        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

        # ── Proof ────────────────────────────────────────
        st.markdown(f"""
        <div class="card" style="display:flex; gap:32px; align-items:center; flex-wrap:wrap;">
            <div>
                <div class="stat-label">Processing ID</div>
                <div style="font-family:'DM Mono',monospace; font-size:12px; color:rgba(255,255,255,0.5); margin-top:4px;">{result.processing_id[:16]}…</div>
            </div>
            <div>
                <div class="stat-label">Salt Destroyed</div>
                <div style="font-family:'DM Mono',monospace; font-size:12px; color:rgba(255,255,255,0.5); margin-top:4px;">{'✓ Yes' if result.salt_destroyed else 'No'}</div>
            </div>
            <div>
                <div class="stat-label">VPS Reversal</div>
                <div style="font-family:'DM Mono',monospace; font-size:12px; color:rgba(255,255,255,0.5); margin-top:4px;">{'Impossible' if result.vps_impossible else 'Possible'}</div>
            </div>
            <div>
                <div class="stat-label">Language</div>
                <div style="font-family:'DM Mono',monospace; font-size:12px; color:rgba(255,255,255,0.5); margin-top:4px;">{result.language_detected}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("Raw JSON"):
            st.json({
                "structure_text": result.structure_text,
                "structure_tags": result.structure_tags,
                "semantic_vector": result.semantic_vector,
                "topic_distribution": result.topic_distribution,
                "behavioral_pattern": result.behavioral_pattern,
                "identity_tokens_found": result.identity_tokens_found,
                "learned_words_used": result.learned_words_used,
                "identity_types_found": result.identity_types_found,
                "pii_types_removed": result.pii_types_removed,
                "privacy_score": result.privacy_score,
                "utility_score": result.utility_score,
                "bhrt_score": result.bhrt_score,
                "identity_hash": result.identity_hash[:16] + "...",
                "salt_destroyed": result.salt_destroyed,
                "vps_impossible": result.vps_impossible,
                "processing_id": result.processing_id,
                "language_detected": result.language_detected,
            })

    elif run and not user_text.strip():
        st.markdown("<p style='color:rgba(255,255,255,0.4); font-size:13px;'>Pehle text daalo.</p>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
#  TAB 2: CSV BULK
# ══════════════════════════════════════════════════════
with tab2:
    st.markdown("""
    <div style="padding: 24px 0 16px 0;">
        <p style="color:rgba(255,255,255,0.35); font-size:13px; margin:0;">
            CSV upload karo — batch processing with full output.
        </p>
    </div>
    """, unsafe_allow_html=True)

    sample_data = {'text': [
        'My name is Rajesh and I am very sad today. My phone is 9876543210.',
        'Main aaj bahut khush hoon. Mera email rajesh@test.com hai.',
        'We had a meeting with the client in Mumbai. The budget was Rs.50000.',
        'Mujhe lagta hai main fail ho gaya. Mera boss ne mujhe daanta.',
        'I felt frustrated at work yesterday. My manager moved the deadline again.',
    ]}
    sample_df = pd.DataFrame(sample_data)

    col_dl, _ = st.columns([1, 3])
    with col_dl:
        st.download_button(
            "Download Sample CSV",
            data=sample_df.to_csv(index=False).encode('utf-8'),
            file_name='bhrt_sample.csv',
            mime='text/csv',
        )

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload CSV", type=['csv'], label_visibility="collapsed")

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.markdown(f"<p style='color:rgba(255,255,255,0.35); font-size:13px;'>{len(df)} rows loaded.</p>", unsafe_allow_html=True)

            text_columns = df.select_dtypes(include=['object']).columns.tolist()
            if not text_columns:
                st.error("No text columns found.")
            else:
                col_s, _ = st.columns([2, 3])
                with col_s:
                    selected_col = st.selectbox("Column:", text_columns, label_visibility="collapsed")

                col_rb, _ = st.columns([1, 4])
                with col_rb:
                    run_bulk = st.button(f"Process {len(df)} rows", key="bulk_run")

                if run_bulk:
                    progress = st.progress(0)
                    status = st.empty()
                    results = []

                    for idx, row in df.iterrows():
                        text = str(row[selected_col])
                        if text and text != 'nan':
                            r = process(text)
                            results.append({
                                'original_text': text,
                                'structure_text': r.structure_text,
                                'behavioral_pattern': r.behavioral_pattern,
                                'privacy_score': r.privacy_score,
                                'utility_score': r.utility_score,
                                'bhrt_score': r.bhrt_score,
                                'identity_tokens_found': r.identity_tokens_found,
                                'identity_types_found': ', '.join(r.identity_types_found),
                                'pii_types_removed': ', '.join(r.pii_types_removed) if r.pii_types_removed else '',
                                'language_detected': r.language_detected,
                                'processing_id': r.processing_id,
                            })
                        else:
                            results.append({'original_text': text, 'structure_text': '', 'behavioral_pattern': 'EMPTY',
                                            'privacy_score': 0, 'utility_score': 0, 'bhrt_score': 0,
                                            'identity_tokens_found': 0, 'identity_types_found': '',
                                            'pii_types_removed': '', 'language_detected': 'unknown', 'processing_id': ''})

                        progress.progress(min((idx + 1) / len(df), 1.0))
                        status.markdown(f"<p style='color:rgba(255,255,255,0.3);font-size:12px;'>Row {idx + 1} / {len(df)}</p>", unsafe_allow_html=True)

                    progress.empty()
                    status.empty()

                    results_df = pd.DataFrame(results)
                    st.markdown("<div class='sect-divider'></div>", unsafe_allow_html=True)

                    c1, c2, c3, c4 = st.columns(4)
                    with c1: st.metric("Avg Privacy", f"{results_df['privacy_score'].mean():.0f}")
                    with c2: st.metric("Avg Utility", f"{results_df['utility_score'].mean():.0f}")
                    with c3: st.metric("Avg BHRT", f"{results_df['bhrt_score'].mean():.0f}")
                    with c4: st.metric("Top Pattern", results_df['behavioral_pattern'].value_counts().index[0])

                    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
                    st.dataframe(results_df, use_container_width=True)

                    c_dl1, c_dl2, _ = st.columns([1, 1, 3])
                    with c_dl1:
                        st.download_button("Download Full", data=results_df.to_csv(index=False).encode('utf-8'),
                                           file_name='bhrt_processed.csv', mime='text/csv')
                    with c_dl2:
                        summary = results_df[['structure_text','behavioral_pattern','privacy_score','bhrt_score']]
                        st.download_button("Download Summary", data=summary.to_csv(index=False).encode('utf-8'),
                                           file_name='bhrt_summary.csv', mime='text/csv')

        except Exception as e:
            st.error(f"Error: {str(e)}")

# ══════════════════════════════════════════════════════
#  TAB 3: SYSTEM
# ══════════════════════════════════════════════════════
with tab3:
    st.markdown("""
    <div style="padding: 24px 0 16px 0;">
        <p style="color:rgba(255,255,255,0.35); font-size:13px; margin:0;">
            Engine statistics and memory state.
        </p>
    </div>
    """, unsafe_allow_html=True)

    try:
        stats = get_memory_stats()
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.metric("Learned Words", stats['learned_words'])
        with c2: st.metric("Patterns", stats['learned_patterns'])
        with c3: st.metric("Context Rules", stats['context_rules'])
        with c4: st.metric("Total Processed", stats['total_processed'])

        st.markdown("<div class='sect-divider'></div>", unsafe_allow_html=True)

        memory_path = os.path.join(os.path.dirname(__file__), 'bhrt_memory.json')
        if os.path.exists(memory_path):
            with open(memory_path, 'r', encoding='utf-8') as f:
                memory = json.load(f)

            learned = memory.get('learned_words', {})
            if learned:
                st.markdown("<p style='font-size:11px; text-transform:uppercase; letter-spacing:0.1em; color:rgba(255,255,255,0.3); margin-bottom:12px;'>Learned Words</p>", unsafe_allow_html=True)
                ldf = pd.DataFrame([
                    {'word': k, 'category': v['category'], 'confidence': round(v['confidence'], 3),
                     'seen': v['seen'], 'source': v.get('added_by', 'auto')}
                    for k, v in learned.items()
                ]).sort_values('seen', ascending=False)
                st.dataframe(ldf, use_container_width=True)
            else:
                st.markdown("<p style='color:rgba(255,255,255,0.25); font-size:13px;'>No learned words yet. Process text to begin silent learning.</p>", unsafe_allow_html=True)

            patterns = memory.get('learned_patterns', {})
            if patterns:
                st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
                st.markdown("<p style='font-size:11px; text-transform:uppercase; letter-spacing:0.1em; color:rgba(255,255,255,0.3); margin-bottom:12px;'>Learned Patterns</p>", unsafe_allow_html=True)
                pdf = pd.DataFrame([
                    {'pattern': k, 'category': v['category'], 'confidence': round(v['confidence'], 3), 'seen': v['seen']}
                    for k, v in patterns.items()
                ])
                st.dataframe(pdf, use_container_width=True)

    except Exception as e:
        st.markdown(f"<p style='color:rgba(255,255,255,0.3); font-size:13px;'>Memory not initialized. Process text first.</p>", unsafe_allow_html=True)

# ── Footer ──────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding:48px 0 24px 0;">
    <p style="font-family:'DM Mono',monospace; font-size:11px; color:rgba(255,255,255,0.12); letter-spacing:0.08em;">
        BHRT ENGINE v2.0 · J.B.S. Mandloi · Apache 2.0
    </p>
</div>
""", unsafe_allow_html=True)
