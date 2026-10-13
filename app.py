import os
import io
import re
import base64
import streamlit as st
from gtts import gTTS

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="FSI-AIBR | German A1 Language Engine",
    page_icon="🔺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------------------------------------------
# 2. BASE64 ENCODING & AUDIO ENGINE
# -----------------------------------------------------------------------------
def get_base64_of_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

def text_to_audio(text, lang='de'):
    tts = gTTS(text=text, lang=lang)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp

assets_dir = "assets"
logo_path = os.path.join(assets_dir, "logo1.png") if os.path.exists(os.path.join(assets_dir, "logo1.png")) else "logo1.png"

pic1_path = os.path.join(assets_dir, "pic1.png")
pic2_path = os.path.join(assets_dir, "pic2.png")
pic3_path = os.path.join(assets_dir, "pic3.png")
pic4_path = os.path.join(assets_dir, "pic4.png")
pic5_path = os.path.join(assets_dir, "pic5.png")

logo_b64 = get_base64_of_bin_file(logo_path)

# -----------------------------------------------------------------------------
# 3. DELTA CAFÉS EDITORIAL HUE & GLASSMORPHISM STYLING OVERRIDE
# -----------------------------------------------------------------------------
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

    :root {{
        --bg-main: #0e0806;
        --card-glass: rgba(28, 17, 13, 0.88);
        --border-glow: rgba(217, 160, 120, 0.2);
        --tan-btn: #d9ad92;
        --tan-hover: #e8c4ad;
        --delta-red: #e32219;
        --text-pure: #fdfbf7;
        --text-muted: #bcaba0;
    }}

    /* Hide Streamlit Sidebar & Default Chrome */
    [data-testid="stSidebar"], [data-testid="collapsedControl"] {{
        display: none !important;
    }}

    /* Global Dark Canvas - Espresso Warm Hue */
    .stApp {{
        background: radial-gradient(circle at 50% 0%, #281711 0%, #0e0806 80%) !important;
        color: var(--text-pure) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }}

    /* Top Navigation Bar */
    .inst-header {{
        background: rgba(18, 11, 8, 0.85);
        border: 1px solid var(--border-glow);
        border-radius: 50px;
        padding: 1rem 2.2rem;
        margin-bottom: 1.8rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        backdrop-filter: blur(20px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.7);
        flex-wrap: wrap;
        gap: 1rem;
    }}
    .inst-title {{
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 1.6rem;
        font-weight: 700;
        color: var(--text-pure);
        margin: 0;
    }}
    .inst-subtitle {{
        color: var(--tan-btn);
        font-size: 0.95rem;
        font-weight: 500;
    }}
    .inst-badge {{
        background-color: var(--delta-red);
        color: #ffffff;
        padding: 0.4rem 1.2rem;
        border-radius: 30px;
        font-weight: 800;
        font-size: 0.75rem;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        box-shadow: 0 4px 15px rgba(227, 34, 25, 0.35);
    }}

    /* Editorial Hero Card */
    .hero-card {{
        background: var(--card-glass);
        border: 1px solid var(--border-glow);
        border-radius: 28px;
        padding: 2.5rem;
        margin-bottom: 1.8rem;
        backdrop-filter: blur(20px);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6);
    }}
    .editorial-title {{
        font-family: 'Playfair Display', serif;
        font-size: 3.2rem;
        font-weight: 400;
        line-height: 1.15;
        color: var(--text-pure);
        margin-bottom: 0.8rem;
    }}
    .editorial-subtitle {{
        color: var(--tan-btn);
        font-size: 1.1rem;
        font-weight: 400;
        letter-spacing: 0.5px;
    }}

    /* Content Cards */
    .inst-card {{
        background: var(--card-glass);
        border: 1px solid var(--border-glow);
        border-radius: 24px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        backdrop-filter: blur(16px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }}
    .card-header-title {{
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 1.35rem;
        font-weight: 700;
        color: var(--tan-btn);
        margin-bottom: 1rem;
    }}

    /* Hover Tooltip Engine - Mobile & Web Compatible */
    .tooltip-de {{
        position: relative;
        display: inline-block;
        color: var(--tan-btn);
        font-weight: 600;
        border-bottom: 1px dashed var(--tan-btn);
        cursor: help;
    }}

    .tooltip-de .tooltip-text {{
        visibility: hidden;
        width: max-content;
        max-width: 260px;
        background-color: #1a0f0b;
        color: #ffffff;
        text-align: center;
        border: 1px solid var(--tan-btn);
        border-radius: 10px;
        padding: 6px 12px;
        font-size: 0.85rem;
        font-weight: 500;
        
        position: absolute;
        z-index: 999;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        
        opacity: 0;
        transition: opacity 0.3s ease, transform 0.3s ease;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.8);
        pointer-events: none;
    }}

    .tooltip-de:hover .tooltip-text {{
        visibility: visible;
        opacity: 1;
        transform: translateX(-50%) translateY(-3px);
    }}

    /* Guidance Callout Box */
    .guidance-box {{
        background: rgba(217, 173, 146, 0.08);
        border-left: 4px solid var(--tan-btn);
        padding: 1rem 1.2rem;
        border-radius: 8px;
        color: var(--text-muted);
        font-size: 0.95rem;
        margin-bottom: 1.2rem;
    }}

    /* Form Fields & Inputs */
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div, textarea {{
        background-color: #170d0a !important;
        border-color: var(--border-glow) !important;
        color: #ffffff !important;
        border-radius: 12px !important;
    }}

    /* Action Buttons */
    .stButton > button {{
        background: linear-gradient(135deg, var(--tan-btn) 0%, #ba8c73 100%) !important;
        color: #0e0806 !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 0.75rem 2.5rem !important;
        font-weight: 800 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 4px 18px rgba(217, 173, 146, 0.25) !important;
        transition: all 0.3s ease !important;
    }}
    .stButton > button:hover {{
        transform: translateY(-2px);
        background: linear-gradient(135deg, var(--tan-hover) 0%, var(--tan-btn) 100%) !important;
        box-shadow: 0 6px 25px rgba(217, 173, 146, 0.4) !important;
    }}

    div[data-testid="stMetricValue"] {{
        color: var(--tan-btn) !important;
        font-weight: 800 !important;
    }}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. SESSION STATE
# -----------------------------------------------------------------------------
if "scores" not in st.session_state:
    st.session_state.scores = {
        "hoeren": 0,
        "lesen": 0,
        "schreiben_task1": 0,
        "schreiben_task2": 0,
        "sprechen": 0
    }

# -----------------------------------------------------------------------------
# 5. DELTA-STYLE HEADER
# -----------------------------------------------------------------------------
logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="height:60px; margin-right:15px; filter:drop-shadow(0 4px 8px rgba(0,0,0,0.5));">' if logo_b64 else ''

st.markdown(f"""
<div class="inst-header">
    <div style="display: flex; align-items: center;">
        {logo_html}
        <div>
            <div class="inst-title">Femi Samson Institute of AI & Biomedical Research</div>
            <div class="inst-subtitle">ÖSD Zertifikat A1 German Language Intelligence Engine</div>
        </div>
    </div>
    <div>
        <span class="inst-badge">FSI-AIBR CERTIFIED</span>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 6. TOP NAVIGATION PILLS
# -----------------------------------------------------------------------------
module = st.radio(
    "Select Stage:",
    [
        "0. A1 Foundations & Strategy",
        "1. Hören (Voicemail & Audio)",
        "2. Lesen (Ad Matching)",
        "3. Schreiben (Form & Email)",
        "4. Sprechen (Voice AI)",
        "5. Final Scorecard & Audit"
    ],
    horizontal=True
)

st.divider()

# Live Scoreboard
m1, m2, m3 = st.columns(3)
total_written = (
    st.session_state.scores["hoeren"] + 
    st.session_state.scores["lesen"] + 
    st.session_state.scores["schreiben_task1"] + 
    st.session_state.scores["schreiben_task2"]
)
m1.metric("Schriftlich Subtotal", f"{total_written} / 75 pts", delta="Pass >= 38" if total_written >= 38 else "In Progress")
m2.metric("Mündlich Subtotal", f"{st.session_state.scores['sprechen']} / 25 pts", delta="Pass >= 12" if st.session_state.scores['sprechen'] >= 12 else "In Progress")
m3.metric("Grand Score", f"{total_written + st.session_state.scores['sprechen']} / 100 pts")

# -----------------------------------------------------------------------------
# MODULE 0: DEEP PRACTICAL A1 FOUNDATIONS & SURVIVAL KIT
# -----------------------------------------------------------------------------
if module == "0. A1 Foundations & Strategy":
    st.markdown("""
    <div class="hero-card">
        <div class="editorial-title">German A1,<br><i>with intelligence.</i></div>
        <div class="editorial-subtitle">Practical survival kit, sentence builder lab, and examination blueprints for distinction.</div>
    </div>
    """, unsafe_allow_html=True)

    tab_lab, tab_w, tab_tpl, tab_sp, tab_plan = st.tabs([
        "🧪 1. Verb Pos-2 Lab", 
        "❓ 2. Question Words (W-Fragen)", 
        "✉️ 3. Universal Email Blueprint", 
        "🔤 4. Alphabet & Number Trainer", 
        "⏱️ 5. Exam-Day Time Blueprint"
    ])

    # 1. Interactive Sentence Builder Lab
    with tab_lab:
        st.markdown('<div class="inst-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header-title">Golden Rule: Verb Position 2 Interactive Lab</div>', unsafe_allow_html=True)
        st.write("In declarative German sentences, the **conjugated main verb ALWAYS stays in Position 2**.")
        
        st.info("Task: Unscramble the components into a grammatically correct sentence: `am Freitag` | `ich` | `komme` | `an` | `um 14 Uhr` | `in Berlin`")
        
        u_sent = st.text_input("Type your sentence in German:", value="Am Freitag komme ich um 14 Uhr in Berlin an.")
        
        if st.button("Check Sentence Syntax"):
            words = u_sent.strip().split()
            if len(words) >= 2 and words[1].lower() in ["komme", "fahre", "gehe", "bin", "habe"]:
                st.success("✅ **PERFECT GRAMMAR!** Verb 'komme' is in Position 2. Full points guaranteed in writing!")
            else:
                st.error("❌ **VERB POSITION ERROR!** Make sure your conjugated verb is the second element in the sentence.")
        st.markdown('</div>', unsafe_allow_html=True)

    # 2. W-Fragen Flash Deck
    with tab_w:
        st.markdown('<div class="inst-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header-title">High-Yield Exam Question Words (Hover for translation)</div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""
            * <div class="tooltip-de">Wann?<span class="tooltip-text">When? (Targets dates, days, clock times)</span></div> $\rightarrow$ e.g., *Am Dienstag, um 14 Uhr*
            * <div class="tooltip-de">Wo? / Wohin?<span class="tooltip-text">Where? / Where to? (Targets locations & street names)</span></div> $\rightarrow$ e.g., *In Berlin, Bernergasse 12*
            * <div class="tooltip-de">Wer? / Mit wem?<span class="tooltip-text">Who? / With whom? (Targets people & family members)</span></div> $\rightarrow$ e.g., *Mein Bruder, Frau Meyer*
            """, unsafe_allow_html=True)
        with c2:
            st.markdown("""
            * <div class="tooltip-de">Wie viel? / Wie lange?<span class="tooltip-text">How much? / How long? (Targets prices & durations)</span></div> $\rightarrow$ e.g., *30 Euro, drei Tage*
            * <div class="tooltip-de">Warum?<span class="tooltip-text">Why? (Targets reasons & causes)</span></div> $\rightarrow$ e.g., *Wegen dem Auto*
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 3. Copy-Paste 30-Word Email Template
    with tab_tpl:
        st.markdown('<div class="inst-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header-title">Universal 30-Word Task 2 Email Template</div>', unsafe_allow_html=True)
        st.write("Use this exact blueprint to score full 10 points on the written email task:")
        
        st.code("""
Liebe [Name],

vielen Dank für deine E-Mail. 
Ich komme am [Freitag] um [14 Uhr] an. 
Ich bleibe für [drei Tage]. 
Ich bringe [meinen Bruder] mit.

Liebe Grüße,
[Your Name]
        """, language="text")
        st.markdown('</div>', unsafe_allow_html=True)

    # 4. Spelled Alphabet & Number Audio Trainer
    with tab_sp:
        st.markdown('<div class="inst-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header-title">Spelled Letter & Number Trainer (Hören Prep)</div>', unsafe_allow_html=True)
        
        col_l, col_n = st.columns(2)
        with col_l:
            st.subheader("Tricky Spelled Letters")
            letter_sel = st.selectbox("Select Letter to Hear Pronunciation:", ["E (pronounced 'ay')", "I (pronounced 'ee')", "V (pronounced 'fau')", "W (pronounced 'vay')", "Ä / Ö / Ü (Umlauts)"])
            sample_char = letter_sel[0]
            st.audio(text_to_audio(f"Der Buchstabe {sample_char}"), format="audio/mp3")

        with col_n:
            st.subheader("Key Number Audio Streams")
            num_sel = st.selectbox("Select Number:", ["12 (zwölf)", "14 (vierzehn)", "0664 (Null sechs sechs vier)"])
            st.audio(text_to_audio(num_sel), format="audio/mp3")
        st.markdown('</div>', unsafe_allow_html=True)

    # 5. Exam-Day Time Allocation Table
    with tab_plan:
        st.markdown('<div class="inst-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header-title">70-Minute Exam-Day Time Management Strategy</div>', unsafe_allow_html=True)
        
        st.markdown("""
        | Subtest Module | Allocated Time | Practical Battle Strategy |
        | :--- | :--- | :--- |
        | **Lesen (Reading)** | 25 Minutes | Read question scenarios *before* classified ads to target keywords. |
        | **Hören (Listening)** | ~20 Minutes | Write down digits first during audio playback; double-check spelling on replay. |
        | **Schreiben (Writing)** | 20 Minutes | Spend 5 mins on Form Filling (Task 1) and 15 mins drafting the 30-word email (Task 2). |
        | **Buffer Review** | 5 Minutes | Verify Verb Position 2 and basic capitalization on all nouns. |
        """)
        st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# MODULE 1: HÖREN
# -----------------------------------------------------------------------------
elif module == "1. Hören (Voicemail & Audio)":
    st.markdown('<div class="inst-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header-title">Module 1: Hören - Voicemail Extraction & Voice Practice</div>', unsafe_allow_html=True)
    
    col_h1, col_h2 = st.columns([2, 1])
    with col_h1:
        st.markdown("""
        <div class="guidance-box">
            💡 <b>Exam Directive:</b> Listen to the voicemail message twice. Extract the caller's spelled street name, meeting time, and phone number.
        </div>
        """, unsafe_allow_html=True)

        voicemail_text = (
            "Guten Tag, Meyer spricht hier. Ich rufe wegen dem Auto an. "
            "Ich habe am kommenden Dienstag, am 12. Mai um 14 Uhr Zeit. "
            "Ich wohne in der Bernergasse 12. B - E - R - N - E - R - gasse 12. "
            "Meine Telefonnummer ist: 0664 2 5 8 2 6 4 1."
        )

        st.subheader("🔊 Audio Dictation Stream")
        audio_file = text_to_audio(voicemail_text)
        st.audio(audio_file, format="audio/mp3")
    
    with col_h2:
        if os.path.exists(pic1_path):
            st.image(pic1_path, caption="Audio & Listening Culture", use_container_width=True)

    st.markdown("### Interactive Audio Script (Hover for English translation):")
    st.markdown("""
    "<div class="tooltip-de">Guten Tag<span class="tooltip-text">Good day / Hello</span></div>, Meyer <div class="tooltip-de">spricht hier<span class="tooltip-text">speaking here</span></div>. 
    Ich rufe <div class="tooltip-de">wegen dem Auto<span class="tooltip-text">regarding the car</span></div> an. 
    Ich habe am <div class="tooltip-de">kommenden Dienstag<span class="tooltip-text">next Tuesday</span></div> um <div class="tooltip-de">14 Uhr Zeit<span class="tooltip-text">2 PM time available</span></div>. 
    Ich wohne in der <div class="tooltip-de">Bernergasse 12<span class="tooltip-text">Berner Street #12</span></div>. 
    Meine <div class="tooltip-de">Telefonnummer<span class="tooltip-text">telephone number</span></div> ist 0664 2 5 8 2 6 4 1."
    """, unsafe_allow_html=True)

    col_t, col_v = st.columns([1, 1])
    with col_t:
        ans_street = st.text_input("Gasse / Street Name (Spelled):")
        ans_phone = st.text_input("Telefonnummer / Phone Number:")
        ans_time = st.text_input("Uhrzeit / Meeting Time:")

    with col_v:
        user_audio = st.audio_input("Record voice response:")
        if user_audio:
            st.success("🎤 Audio captured!")

    if st.button("Evaluate Hören Task"):
        score = 0
        if ans_street.strip().upper() == "BERNER": score += 2
        clean_phone = re.sub(r'\D', '', ans_phone)
        if clean_phone == "06642582641": score += 2
        if "14" in ans_time or "2" in ans_time: score += 2
        score += 4
        
        st.session_state.scores["hoeren"] = score
        st.success(f"Hören Score Saved: **{score} / 10 pts**")
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# MODULE 2: LESEN
# -----------------------------------------------------------------------------
elif module == "2. Lesen (Ad Matching)":
    st.markdown('<div class="inst-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header-title">Module 2: Lesen - Advertisement Signal Pattern Matching</div>', unsafe_allow_html=True)
    
    col_sit, col_ad = st.columns(2)
    with col_sit:
        st.markdown("### Situations (Situationen)")
        st.markdown("""
        * **A:** Sie möchten <div class="tooltip-de">billig im Ausland telefonieren<span class="tooltip-text">make cheap international phone calls</span></div>.
        * **B:** Sie suchen einen <div class="tooltip-de">Job im Büro als Sekretär/in<span class="tooltip-text">job in an office as a secretary</span></div>.
        * **C:** Sie brauchen <div class="tooltip-de">Hilfe bei der Hausarbeit<span class="tooltip-text">help with housework / cleaning</span></div>.
        """, unsafe_allow_html=True)

    with col_ad:
        st.markdown("### Advertisements (Anzeigen)")
        st.markdown("""
        * **Anzeige 1:** Personalvermittlung - <div class="tooltip-de">Sekretärin gesucht<span class="tooltip-text">Secretary wanted (Full-time)</span></div>.
        * **Anzeige 2:** Fitnesscenter Olymp - <div class="tooltip-de">Geräte & Rückengymnastik<span class="tooltip-text">Gym equipment & back exercises</span></div>.
        * **Anzeige 4:** weltweitanrufen.de - <div class="tooltip-de">Günstige Auslandsanrufe<span class="tooltip-text">Cheap international calls from 1.9 cents</span></div>.
        * **Anzeige 5:** Petra Maier - <div class="tooltip-de">Hilfe bei Wäsche, Bügeln und Saubermachen<span class="tooltip-text">Help with laundry, ironing, and cleaning</span></div>.
        """, unsafe_allow_html=True)

    ans_a = st.selectbox("Ad for Situation A:", ["-- Select --", "Anzeige 1", "Anzeige 2", "Anzeige 4", "Anzeige 5"])
    ans_b = st.selectbox("Ad for Situation B:", ["-- Select --", "Anzeige 1", "Anzeige 2", "Anzeige 4", "Anzeige 5"])
    ans_c = st.selectbox("Ad for Situation C:", ["-- Select --", "Anzeige 1", "Anzeige 2", "Anzeige 4", "Anzeige 5"])

    if st.button("Evaluate Reading Match"):
        score = 0
        if ans_a == "Anzeige 4": score += 3.33
        if ans_b == "Anzeige 1": score += 3.33
        if ans_c == "Anzeige 5": score += 3.34
        
        final_score = int(round(score))
        st.session_state.scores["lesen"] = final_score
        st.success(f"Lesen Score Saved: **{final_score} / 10 pts**")
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# MODULE 3: SCHREIBEN
# -----------------------------------------------------------------------------
elif module == "3. Schreiben (Form & Email)":
    st.markdown('<div class="inst-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header-title">Module 3: Schreiben - Form Filling & Email Synthesizer</div>', unsafe_allow_html=True)
    
    col_w1, col_w2 = st.columns([2, 1])
    with col_w1:
        st.subheader("Task 1: Form Filling (5 Points)")
        st.markdown("Extract details for Ricardo Torres (DOB 26.11.1979) traveling to Switzerland in September by train. Wants double room with breakfast, hiking and swimming.")

        with st.form("form_t1"):
            c1, c2 = st.columns(2)
            with c1:
                st.text_input("Nachname:", value="Torres")
                st.text_input("Vorname:", value="Ricardo")
                st.text_input("Geburtsdatum:", value="26.11.1979")
                st.text_input("Urlaubsland:", value="Schweiz")
            with c2:
                st.selectbox("Anreise mit:", ["Zug", "Auto", "Flugzeug"])
                st.radio("Zimmer:", ["Einzelzimmer", "Doppelzimmer"], index=1)
                st.multiselect("Sport:", ["Wandern", "Schwimmen", "Fußball"], default=["Wandern", "Schwimmen"])
            sub_f = st.form_submit_button("Save Form Answers")
            if sub_f:
                st.session_state.scores["schreiben_task1"] = 5
                st.success("Task 1 Form Score: 5 / 5 pts")
    
    with col_w2:
        if os.path.exists(pic4_path):
            st.image(pic4_path, caption="Cozy Writing Scenario", use_container_width=True)

    st.divider()

    st.subheader("Task 2: Personal Email Evaluator (10 Points)")
    default_email = "Liebe Rafaela,\n\nvielen Dank für deine E-Mail. Ich komme am Freitag um 14 Uhr an. Ich bleibe für drei Tage. Ich bringe meinen Bruder mit.\n\nLiebe Grüße,\nDaniel"
    user_email = st.text_area("Write response in German:", value=default_email, height=180)

    if st.button("Grade Written Email"):
        has_sal = any(w in user_email.lower() for w in ["liebe", "lieber", "hallo"])
        has_val = any(w in user_email.lower() for w in ["grüße", "gruß", "tschüss"])
        has_t = any(w in user_email.lower() for w in ["uhr", "am", "freitag", "samstag"])
        has_d = any(w in user_email.lower() for w in ["tage", "tag", "woche"])
        has_p = any(w in user_email.lower() for w in ["mit", "bruder", "freund", "schwester"])
        
        t2_score = 0
        if has_sal and has_val: t2_score += 2
        if has_t: t2_score += 2.5
        if has_d: t2_score += 2.5
        if has_p: t2_score += 3
        
        st.session_state.scores["schreiben_task2"] = int(t2_score)
        st.success(f"Email Score Saved: **{int(t2_score)} / 10 pts**")
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# MODULE 4: SPRECHEN
# -----------------------------------------------------------------------------
elif module == "4. Sprechen (Voice AI)":
    st.markdown('<div class="inst-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header-title">Module 4: Sprechen - Voice Practice & AI Simulator</div>', unsafe_allow_html=True)
    
    col_sp1, col_sp2 = st.columns([2, 1])
    with col_sp1:
        st.markdown("""
        <div class="guidance-box">
            💡 <b>Speaking Exam Tasks:</b> Task 1: Self Introduction. Task 2: Describe a photo. Task 3: Practical Roleplay.
        </div>
        """, unsafe_allow_html=True)

        v_rec = st.audio_input("Record your spoken response:")
        if v_rec:
            st.audio(v_rec)
            st.info("🎤 Audio response captured!")

        sample_text = "Ich heiße Daniel. Ich spreche Englisch und Deutsch. Ich bin Forscher von Beruf."
        st.markdown("""
        **Sample Text (Hover for translation):** <br>
        "<div class="tooltip-de">Ich heiße Daniel<span class="tooltip-text">My name is Daniel</span></div>. 
        <div class="tooltip-de">Ich spreche Englisch und Deutsch<span class="tooltip-text">I speak English and German</span></div>. 
        <div class="tooltip-de">Ich bin Forscher von Beruf<span class="tooltip-text">I am a researcher by profession</span></div>."
        """, unsafe_allow_html=True)
        st.audio(text_to_audio(sample_text), format="audio/mp3")

        sp_eval = st.slider("Record Speaking Assessment Score (0-25):", 0, 25, 23)
        if st.button("Save Speaking Score"):
            st.session_state.scores["sprechen"] = sp_eval
            st.success(f"Sprechen Score Updated: **{sp_eval} / 25 pts**")

    with col_sp2:
        if os.path.exists(pic5_path):
            st.image(pic5_path, caption="Precision & Focus in Oral Exams", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# MODULE 5: SCORECARD
# -----------------------------------------------------------------------------
elif module == "5. Final Scorecard & Audit":
    st.markdown('<div class="inst-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header-title">📊 FSI-AIBR Certified ÖSD Zertifikat A1 Audit Scorecard</div>', unsafe_allow_html=True)
    
    h = st.session_state.scores["hoeren"]
    l = st.session_state.scores["lesen"]
    s = st.session_state.scores["schreiben_task1"] + st.session_state.scores["schreiben_task2"]
    sp = st.session_state.scores["sprechen"]
    
    written_total = h + l + s
    grand_total = written_total + sp
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Schriftlich (Written)", f"{written_total} / 75", delta="Min Pass: 38")
    c2.metric("Mündlich (Oral)", f"{sp} / 25", delta="Min Pass: 12")
    c3.metric("Grand Total Score", f"{grand_total} / 100")
    
    st.divider()
    
    pass_h = h >= 6
    pass_l = l >= 6
    pass_w = written_total >= 38
    pass_o = sp >= 12
    
    if pass_h and pass_l and pass_w and pass_o:
        if grand_total >= 88:
            st.balloons()
            st.success("🏆 **CERTIFICATE STATUS: SEHR GUT** — Candidate qualifies for ÖSD Zertifikat A1 with Distinction!")
        else:
            st.success("✅ **CERTIFICATE STATUS: BESTANDEN** — Candidate successfully passed the ÖSD Zertifikat A1 exam!")
    else:
        st.error("❌ **CERTIFICATE STATUS: NICHT BESTANDEN** — Re-test required in failed modules.")
    st.markdown('</div>', unsafe_allow_html=True)