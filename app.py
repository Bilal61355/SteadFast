import streamlit as st
from groq import Groq
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pandas as pd

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(r"C:\steadfast_ai\steadfast-494407-90536fd8219a-json-googlesheets.json", scope)
sheets_client = gspread.authorize(creds)
sheet = sheets_client.open("Steadfast Waitlist").sheet1

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.set_page_config(page_title="Steadfast", page_icon="⚡", layout="wide")
st.markdown('<style>div[data-stale="true"] { opacity: 1 !important; }</style>', unsafe_allow_html=True)

st.markdown("""
<style>
            * { transition: none !important; animation: none !important; }

[data-testid="stAppViewContainer"],
[data-testid="stApp"],
.stApp,
.main,
section {
    opacity: 1 !important;
    visibility: visible !important;
    background: #0A0A0A !important;
}

iframe { display: none; }
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

* { margin: 0; padding: 0; box-sizing: border-box; }

.stApp {
    background: #0A0A0A;
    background-image:
        radial-gradient(ellipse at 20% 20%, rgba(200, 169, 110, 0.07) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 80%, rgba(74, 144, 164, 0.05) 0%, transparent 50%);
    font-family: 'DM Sans', sans-serif;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* Navbar */
.navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 22px 60px;
    border-bottom: 1px solid rgba(200, 169, 110, 0.15);
    background: rgba(10,10,10,0.95);
    position: sticky;
    top: 0;
    z-index: 999;
    backdrop-filter: blur(12px);
}
.nav-logo {
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 800;
    color: #F5F5F0;
    letter-spacing: 3px;
    text-transform: uppercase;
}
.nav-logo span { color: #C8A96E; }
.nav-tagline {
    font-size: 12px;
    color: #555;
    letter-spacing: 1px;
    text-transform: uppercase;
    font-family: 'DM Sans', sans-serif;
}
.nav-badge {
    background: rgba(200, 169, 110, 0.1);
    border: 1px solid rgba(200, 169, 110, 0.3);
    color: #C8A96E;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 12px;
    font-family: 'DM Sans', sans-serif;
    letter-spacing: 1px;
}

/* Hero */
.hero {
    padding: 80px 60px 60px;
    text-align: center;
    max-width: 860px;
    margin: 0 auto;
}
.hero-eyebrow {
    font-size: 11px;
    letter-spacing: 3px;
    color: #C8A96E;
    text-transform: uppercase;
    font-family: 'DM Sans', sans-serif;
    margin-bottom: 20px;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 54px;
    font-weight: 800;
    color: #F5F5F0;
    line-height: 1.1;
    margin-bottom: 20px;
}
.hero-title span { color: #C8A96E; }
.hero-sub {
    font-size: 17px;
    color: #888;
    line-height: 1.7;
    font-family: 'DM Sans', sans-serif;
    font-weight: 300;
    max-width: 560px;
    margin: 0 auto;
}

/* Stats bar */
.stats-bar {
    display: flex;
    justify-content: center;
    gap: 64px;
    padding: 32px 60px;
    border-top: 1px solid rgba(255,255,255,0.04);
    border-bottom: 1px solid rgba(255,255,255,0.04);
    background: rgba(255,255,255,0.01);
}
.stat-item { text-align: center; }
.stat-number {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 800;
    color: #C8A96E;
    line-height: 1;
}
            
.stApp { opacity: 1 !important; transition: none !important; }
[data-testid="stAppViewContainer"] { opacity: 1 !important; }
            
.stat-label {
    font-size: 12px;
    color: #444;
    font-family: 'DM Sans', sans-serif;
    margin-top: 4px;
    letter-spacing: 0.5px;
}

/* Tool section wrapper */
.tool-section {
    padding: 60px 60px 0;
    max-width: 820px;
    margin: 0 auto;
}

/* Section headers */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 26px;
    font-weight: 700;
    color: #F5F5F0;
    margin-bottom: 8px;
}
.section-sub {
    font-size: 14px;
    color: #555;
    margin-bottom: 32px;
    font-family: 'DM Sans', sans-serif;
    line-height: 1.7;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid rgba(255,255,255,0.06) !important;
    gap: 8px;
    justify-content: center;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    color: #555 !important;
    background: transparent !important;
    border: none !important;
    padding: 12px 32px !important;
    border-radius: 0 !important;
    letter-spacing: 0.5px;
}
.stTabs [aria-selected="true"] {
    color: #C8A96E !important;
    border-bottom: 2px solid #C8A96E !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab-panel"] { padding: 40px 0 0 !important; }

/* Textarea */
.stTextArea textarea {
    background: #111 !important;
    color: #F5F5F0 !important;
    border: 1px solid rgba(200, 169, 110, 0.2) !important;
    border-radius: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    padding: 16px !important;
    min-height: 180px !important;
}
.stTextArea textarea:focus {
    border: 1px solid rgba(200, 169, 110, 0.6) !important;
    box-shadow: 0 0 0 3px rgba(200, 169, 110, 0.08) !important;
}
.stTextArea label {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    color: #888 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
}

/* Button */
.stButton button {
    background: linear-gradient(135deg, #C8A96E, #b8935a) !important;
    color: #0A0A0A !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 14px 32px !important;
    margin-top: 16px !important;
    width: 100% !important;
}
.stButton button:hover {
    background: linear-gradient(135deg, #d4b87a, #C8A96E) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px rgba(200, 169, 110, 0.25) !important;
}

/* Output */
.output-card {
    background: #111;
    border: 1px solid rgba(200, 169, 110, 0.2);
    border-left: 3px solid #C8A96E;
    border-radius: 12px;
    padding: 28px 32px;
    color: #D0D0C8;
    font-family: 'DM Sans', sans-serif;
    font-size: 15px;
    line-height: 1.8;
    margin-top: 24px;
    white-space: pre-line;
}
.output-label {
    font-size: 11px;
    letter-spacing: 2px;
    color: #C8A96E;
    text-transform: uppercase;
    font-family: 'DM Sans', sans-serif;
    margin-bottom: 16px;
    display: block;
}

/* File uploader */
.stFileUploader section {
    background: #111 !important;
    border: 1px dashed rgba(200, 169, 110, 0.3) !important;
    border-radius: 12px !important;
}
.stFileUploader label {
    color: #888 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
}

/* Why section */
.why-section {
    padding: 100px 60px;
    max-width: 1100px;
    margin: 0 auto;
}
.why-eyebrow {
    font-size: 11px;
    letter-spacing: 3px;
    color: #C8A96E;
    text-transform: uppercase;
    font-family: 'DM Sans', sans-serif;
    margin-bottom: 16px;
    text-align: center;
}
.why-title {
    font-family: 'Syne', sans-serif;
    font-size: 40px;
    font-weight: 800;
    color: #F5F5F0;
    text-align: center;
    margin-bottom: 16px;
    line-height: 1.15;
}
.why-title span { color: #C8A96E; }
.why-sub {
    font-size: 16px;
    color: #555;
    text-align: center;
    font-family: 'DM Sans', sans-serif;
    margin-bottom: 64px;
    line-height: 1.7;
}
.problems-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
    margin-bottom: 80px;
}
.problem-card {
    background: #0F0F0F;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 32px 28px;
    transition: border 0.3s;
}
.problem-card:hover {
    border: 1px solid rgba(200, 169, 110, 0.25);
}
.problem-icon {
    font-size: 28px;
    margin-bottom: 16px;
}
.problem-title {
    font-family: 'Syne', sans-serif;
    font-size: 17px;
    font-weight: 700;
    color: #F5F5F0;
    margin-bottom: 10px;
}
.problem-desc {
    font-size: 14px;
    color: #555;
    font-family: 'DM Sans', sans-serif;
    line-height: 1.7;
}

/* Who is it for */
.who-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-top: 48px;
}
.who-card {
    background: rgba(200, 169, 110, 0.04);
    border: 1px solid rgba(200, 169, 110, 0.12);
    border-radius: 12px;
    padding: 24px 20px;
    text-align: center;
}
.who-icon { font-size: 24px; margin-bottom: 12px; }
.who-title {
    font-family: 'Syne', sans-serif;
    font-size: 15px;
    font-weight: 700;
    color: #F5F5F0;
    margin-bottom: 8px;
}
.who-desc {
    font-size: 13px;
    color: #555;
    font-family: 'DM Sans', sans-serif;
    line-height: 1.6;
}
.who-section-title {
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #F5F5F0;
    text-align: center;
    margin-bottom: 8px;
}
.who-section-sub {
    font-size: 14px;
    color: #555;
    text-align: center;
    font-family: 'DM Sans', sans-serif;
    margin-bottom: 0;
}

/* Section divider */
.section-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(200,169,110,0.2), transparent);
    margin: 0 60px;
}

/* CTA band */
.cta-band {
    margin: 80px 60px;
    background: linear-gradient(135deg, rgba(200,169,110,0.08), rgba(74,144,164,0.05));
    border: 1px solid rgba(200,169,110,0.15);
    border-radius: 20px;
    padding: 60px;
    text-align: center;
}
.cta-title {
    font-family: 'Syne', sans-serif;
    font-size: 34px;
    font-weight: 800;
    color: #F5F5F0;
    margin-bottom: 16px;
}
.cta-title span { color: #C8A96E; }
.cta-sub {
    font-size: 16px;
    color: #666;
    font-family: 'DM Sans', sans-serif;
    margin-bottom: 32px;
}
.cta-btn {
    display: inline-block;
    background: linear-gradient(135deg, #C8A96E, #b8935a);
    color: black;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 13px;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 16px 40px;
    border-radius: 8px;
    text-decoration: none;
}
.cta-note {
    font-size: 12px;
    color: #333;
    font-family: 'DM Sans', sans-serif;
    margin-top: 16px;
}

/* Footer */
.footer {
    padding: 40px 60px;
    border-top: 1px solid rgba(255,255,255,0.04);
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.footer-left {
    font-family: 'Syne', sans-serif;
    font-size: 14px;
    font-weight: 700;
    color: #222;
    letter-spacing: 2px;
}
.footer-right {
    font-size: 12px;
    color: #333;
    font-family: 'DM Sans', sans-serif;
}
.footer-right a {
    color: #444;
    text-decoration: none;
    margin-left: 24px;
}
.footer-right a:hover { color: #C8A96E; }

.stSpinner > div { border-top-color: #C8A96E !important; }
</style>
""", unsafe_allow_html=True)

# ── NAVBAR ──────────────────────────────────────────────
st.markdown("""
<div class="navbar">
    <div>
        <div class="nav-logo">STEADY<span>FAST</span></div>
        <div class="nav-tagline">Agency Automation Platform</div>
    </div>
    <div class="nav-badge">⚡ Beta — Free Access</div>
</div>
""", unsafe_allow_html=True)

# ── HERO ─────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">↳ AI-Powered Back Office for Agencies</div>
    <div class="hero-title">Never miss a follow-up <span>again.</span></div>
    <div class="hero-sub">Steadfast handles your meeting follow-ups, voicemail summaries, client reports and competitor monitoring — so you focus entirely on growth.</div>
</div>
""", unsafe_allow_html=True)

# ── STATS ─────────────────────────────────────────────────
st.markdown("""
<div class="stats-bar">
    <div class="stat-item">
        <div class="stat-number">3 sec</div>
        <div class="stat-label">Average email generated</div>
    </div>
    <div class="stat-item">
        <div class="stat-number">4 hrs</div>
        <div class="stat-label">Saved per week per agency</div>
    </div>
    <div class="stat-item">
        <div class="stat-number">100%</div>
        <div class="stat-label">Automated. Zero manual work</div>
    </div>
    <div class="stat-item">
        <div class="stat-number">$0</div>
        <div class="stat-label">To get started today</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── TOOLS ─────────────────────────────────────────────────
st.markdown('<div class="tool-section">', unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["✉️   Meeting Follow-Up", "🎙️   Voicemail Transcriber", "🎯   Cold Email Writer", "📊   Client Report", "🔍   Competitor Monitor"])
with tab1:
    st.markdown("""
    <div class="section-title">Meeting Follow-Up Generator</div>
    <div class="section-sub">Paste rough notes from any call or meeting.<br>
    Steadfast writes a professional follow-up email instantly — before your client even gets home.</div>
    """, unsafe_allow_html=True)

    notes = st.text_area("YOUR MEETING NOTES", height=200,
        placeholder="e.g. Called Sarah at Bloom Agency. Discussed pricing — she likes the $2k/month retainer. Wants full proposal by Friday. Main concern is onboarding timeline...")

    if st.button("Generate Follow-Up Email →", key="email_btn"):
        if notes:
            with st.spinner("Writing your email..."):
                prompt = f"""You are a senior account manager at a top agency.
                Write a warm, professional, concise follow-up email based on these meeting notes.
                Include: friendly opening referencing the conversation, brief summary of key points,
                clear action items with deadlines, confident next steps, professional sign-off.
                Make it feel personal, not templated. Meeting notes: {notes}"""
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )
                result = response.choices[0].message.content
                st.markdown(f"""
                <div style="margin-top:24px">
                    <span class="output-label">✓ Your follow-up email is ready</span>
                    <div class="output-card">{result}</div>
                </div>""", unsafe_allow_html=True)
        else:
            st.warning("Please paste your meeting notes first.")

with tab2:
    st.markdown("""
    <div class="section-title">Voicemail Transcriber</div>
    <div class="section-sub">Upload any voicemail audio file.<br>
    Steadfast transcribes it and tells you exactly who called, what they need, and what to do next.</div>
    """, unsafe_allow_html=True)

    audio_file = st.file_uploader("UPLOAD VOICEMAIL AUDIO", type=["mp3", "mp4", "wav", "m4a"])

    if st.button("Transcribe & Analyse →", key="audio_btn"):
        if audio_file:
            with st.spinner("Transcribing audio..."):
                transcription = client.audio.transcriptions.create(
                    file=(audio_file.name, audio_file.read()),
                    model="whisper-large-v3",
                )
                transcript_text = transcription.text
                st.markdown(f"""
                <div style="margin-top:24px">
                    <span class="output-label">✓ Transcript</span>
                    <div class="output-card">{transcript_text}</div>
                </div>""", unsafe_allow_html=True)

            with st.spinner("Analysing action items..."):
                prompt = f"""From this voicemail transcript extract and format clearly:
                1. Caller Name (if mentioned)
                2. What They Want
                3. Urgency Level (Low / Medium / High) with reason
                4. Recommended Action with suggested timeline
                Be concise and professional. Transcript: {transcript_text}"""
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )
                result = response.choices[0].message.content
                st.markdown(f"""
                <div style="margin-top:20px">
                    <span class="output-label">✓ Action Summary</span>
                    <div class="output-card">{result}</div>
                </div>""", unsafe_allow_html=True)
        else:
            st.warning("Please upload an audio file first.")

with tab3:
    st.markdown("""
    <div class="section-title">Cold Email Writer</div>
    <div class="section-sub">Write a personalised cold email for one lead — or upload a CSV and generate hundreds at once.</div>
    """, unsafe_allow_html=True)

    your_name_ce = st.text_input("YOUR NAME", placeholder="Type Your Name Here", key="ce_name")
    your_offer_ce = st.text_input("WHAT YOU'RE OFFERING", placeholder="AI automation tools for agencies", key="ce_offer")

    mode = st.radio("", ["Single Lead", "Bulk Upload"], horizontal=True)

    if mode == "Single Lead":
        col1, col2 = st.columns(2)
        with col1:
            lead_name = st.text_input("LEAD'S FULL NAME", placeholder="Type Lead's Name Here")
            lead_role = st.text_input("THEIR ROLE / TITLE", placeholder="Type Their Role/Title Here")
        with col2:
            lead_company = st.text_input("COMPANY NAME", placeholder="Type Company Name Here")
            lead_website = st.text_input("COMPANY WEBSITE", placeholder="Type Company Website Here")

        if st.button("Write Cold Email →", key="single_btn"):
            if lead_name and lead_company and your_offer_ce:
                with st.spinner("Writing your personalised email..."):
                    prompt = f"""You are an expert cold email copywriter. Write a short, 
                    personalised cold email to {lead_name} who is a {lead_role} at {lead_company} 
                    (website: {lead_website}).
                    The email is from {your_name_ce} who is offering: {your_offer_ce}.
                    Based on their role and company, intelligently identify their most likely 
                    pain point yourself and use it naturally in the email.
                    Rules:
                    - Maximum 5 sentences
                    - First line must reference something specific about their company or role
                    - Never use generic openers like 'I hope this finds you well'
                    - One clear call to action at the end — a simple question, not a hard sell
                    - Conversational and human, not corporate
                    - Include a subject line at the top
                    Format:
                    Subject: [subject line]
                    [email body]"""

                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt}]
                    )
                    result = response.choices[0].message.content
                    st.markdown(f"""
                    <div style="margin-top:24px">
                        <span class="output-label">✓ Your personalised cold email is ready</span>
                        <div class="output-card">{result}</div>
                    </div>""", unsafe_allow_html=True)
            else:
                st.warning("Please fill in lead name, company and your offer.")


    else:
        st.markdown("""
        <div class="output-card" style="margin-bottom:24px;">
            <span class="output-label">📄 CSV Format Required</span>
            Your CSV must have these exact column headers:<br><br>
            <strong style="color:#C8A96E;">name, role, company, website</strong><br><br>
            Example: Sarah Johnson, Marketing Director, Bloom Agency, bloomagency.com
        </div>
        """, unsafe_allow_html=True)

        csv_file = st.file_uploader("UPLOAD YOUR LEADS CSV", type=["csv"])

        if st.button("Generate All Emails →", key="bulk_btn"):
            if csv_file and your_name_ce and your_offer_ce:
                df = pd.read_csv(csv_file)

                if not {"name", "role", "company", "website"}.issubset(df.columns.str.lower()):
                    st.warning("Your CSV must have these columns: name, role, company, website")
                else:
                    df.columns = df.columns.str.lower()
                    results = []
                    progress = st.progress(0)
                    status = st.empty()

                    for i, row in df.iterrows():
                        status.markdown(f"<p style='color:#C8A96E; font-size:13px;'>Writing email {i+1} of {len(df)} — {row['name']} at {row['company']}...</p>", unsafe_allow_html=True)

                        prompt = f"""You are an expert cold email copywriter. Write a short, 
                        personalised cold email to {row['name']} who is a {row['role']} at {row['company']} 
                        (website: {row['website']}).
                        The email is from {your_name_ce} who is offering: {your_offer_ce}.
                        Based on their role and company, intelligently identify their most likely 
                        pain point yourself and use it naturally in the email.
                        Rules:
                        - Maximum 5 sentences
                        - First line must reference something specific about their company or role  
                        - Never use generic openers like 'I hope this finds you well'
                        - One clear call to action at the end — a simple question, not a hard sell
                        - Conversational and human, not corporate
                        - Include a subject line at the top
                        Format:
                        Subject: [subject line]
                        [email body]"""

                        response = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[{"role": "user", "content": prompt}]
                        )
                        results.append({
                            "name": row["name"],
                            "company": row["company"],
                            "email_content": response.choices[0].message.content
                        })
                        progress.progress((i + 1) / len(df))

                    status.markdown("<p style='color:#C8A96E; font-size:13px;'>✓ All emails generated.</p>", unsafe_allow_html=True)

                    result_df = pd.DataFrame(results)
                    st.download_button(
                        label="⬇️  Download Emails CSV",
                        data=result_df.to_csv(index=False),
                        file_name="steadfast_cold_emails.csv",
                        mime="text/csv"
                    )

                    st.markdown("<span class='output-label' style='margin-top:24px; display:block;'>✓ Preview — First 3 Emails</span>", unsafe_allow_html=True)
                    for r in results[:3]:
                        st.markdown(f"""
                        <div class="output-card" style="margin-bottom:16px;">
                            <strong style="color:#C8A96E;">{r['name']} — {r['company']}</strong><br><br>
                            {r['email_content']}
                        </div>""", unsafe_allow_html=True)

                    if len(results) > 3:
                        st.markdown(f"<p style='color:#555; font-size:13px;'>+ {len(results) - 3} more emails in the downloaded CSV.</p>", unsafe_allow_html=True)
            else:
                st.warning("Please fill in your name, offer and upload a CSV.")
                
with tab4:
    st.markdown("""
    <div class="section-title">Client Report Generator</div>
    <div class="section-sub">Paste your raw campaign data and numbers.<br>
    Steadfast writes a complete professional client report instantly — ready to send.</div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        client_name = st.text_input("CLIENT NAME", placeholder="Type Client Name Here")
        report_period = st.text_input("REPORT PERIOD", placeholder="e.g. September 2024")

    with col2:
        agency_name = st.text_input("YOUR AGENCY NAME", placeholder="Type Your Agency Name Here")
        report_type = st.selectbox("REPORT TYPE", [
            "Monthly Performance Report",
            "Social Media Report",
            "SEO Report",
            "Paid Ads Report",
            "Email Marketing Report"
        ])

    campaign_data = st.text_area("PASTE YOUR RAW CAMPAIGN DATA", height=200,
        placeholder="""e.g.
Website traffic: 12,400 visits (up 18% from last month)
Google Ads: 340 clicks, $2.40 CPC, 12 conversions
Instagram: 4,200 reach, 380 likes, 45 new followers
Email campaign: 2,800 sent, 31% open rate, 4.2% CTR
Top performing post: Product launch reel — 8,400 views
Goals missed: Blog traffic target was 5,000, got 3,200""")

    goals = st.text_input("THIS MONTH'S GOALS (optional)", placeholder="Increase website traffic, grow Instagram following, improve email CTR")

    if st.button("Generate Client Report →", key="report_btn"):
        if client_name and campaign_data and agency_name:
            with st.spinner("Writing your client report..."):
                prompt = f"""You are a senior account manager at a top marketing agency.
                Write a professional, well-structured {report_type} for the period {report_period}.
                
                Client: {client_name}
                Agency: {agency_name}
                Goals this period: {goals}
                
                Raw campaign data:
                {campaign_data}
                
                Structure the report exactly like this:
                1. Executive Summary (2-3 sentences, highlight the biggest win)
                2. Key Results (list each metric clearly with context — is it good or bad?)
                3. What Worked Well (2-3 points with brief explanation)
                4. What Needs Improvement (2-3 points, be honest but constructive)
                5. Recommendations for Next Month (3 specific actionable suggestions)
                6. Closing Note (warm, professional, forward-looking)
                
                Rules:
                - Professional but not robotic — write like a trusted advisor
                - Use the actual numbers from the data provided
                - Be specific, never vague
                - Keep each section concise and scannable
                - Make the client feel their investment is worthwhile"""

                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )
                result = response.choices[0].message.content

                cleaned = result.replace('\n\n\n', '\n\n').strip()
                st.markdown(f"""
                            <div style="margin-top:24px">
                            <span class="output-label">✓ Your client report is ready</span>
                            <div class="output-card">{cleaned}</div>
                            </div>""", unsafe_allow_html=True)

                st.download_button(
                    label="⬇️  Download Report as Text",
                    data=result,
                    file_name=f"steadfast_{client_name}_{report_period}_report.txt",
                    mime="text/plain"
                )
        else:
            st.warning("Please fill in client name, agency name and campaign data.")

with tab5:
    st.markdown("""
    <div class="section-title">Competitor Monitor</div>
    <div class="section-sub">Enter up to 5 competitor URLs.<br>
    Steadfast analyses each one and tells you exactly what they're doing — messaging, services, pricing and positioning.</div>
    """, unsafe_allow_html=True)

    your_business = st.text_input("YOUR BUSINESS TYPE", placeholder="Digital marketing agency specialising in social media")

    st.markdown("<p style='color:#888; font-size:13px; letter-spacing:1px; text-transform:uppercase; margin-top:16px;'>COMPETITOR URLS</p>", unsafe_allow_html=True)

    urls = []
    col1, col2 = st.columns(2)
    with col1:
        url1 = st.text_input("Competitor 1", placeholder="https://competitor1.com", label_visibility="collapsed")
        url2 = st.text_input("Competitor 2", placeholder="https://competitor2.com", label_visibility="collapsed")
        url3 = st.text_input("Competitor 3", placeholder="https://competitor3.com", label_visibility="collapsed")
    with col2:
        url4 = st.text_input("Competitor 4", placeholder="https://competitor4.com", label_visibility="collapsed")
        url5 = st.text_input("Competitor 5", placeholder="https://competitor5.com", label_visibility="collapsed")

    urls = [u for u in [url1, url2, url3, url4, url5] if u.strip()]

    if st.button("Analyse Competitors →", key="competitor_btn"):
        if urls and your_business:
            import requests
            from bs4 import BeautifulSoup

            all_results = []
            progress = st.progress(0)
            status = st.empty()

            for i, url in enumerate(urls):
                status.markdown(f"<p style='color:#C8A96E; font-size:13px;'>Analysing {url}...</p>", unsafe_allow_html=True)
                try:
                    headers = {"User-Agent": "Mozilla/5.0"}
                    response = requests.get(url, headers=headers, timeout=10)
                    soup = BeautifulSoup(response.text, "html.parser")

                    for tag in soup(["script", "style", "nav", "footer", "header"]):
                        tag.decompose()

                    text = soup.get_text(separator=" ", strip=True)
                    text = " ".join(text.split())[:3000]

                    prompt = f"""You are a sharp business analyst. Analyse this competitor website content for a {your_business}.

                    Website: {url}
                    Content: {text}

                    Provide a concise analysis covering:
                    1. Main Headline / Positioning (what's their core message?)
                    2. Services Offered (list their main services)
                    3. Target Audience (who are they going after?)
                    4. Pricing (if mentioned)
                    5. Key Strengths (what are they doing well?)
                    6. Weaknesses / Gaps (what are they missing or doing poorly?)
                    7. One Opportunity (how can you compete against them?)

                    Be specific, sharp, and actionable. No fluff."""

                    ai_response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt}]
                    )
                    analysis = ai_response.choices[0].message.content
                    all_results.append({"url": url, "analysis": analysis, "success": True})

                except Exception as e:
                    all_results.append({"url": url, "analysis": f"Could not fetch this website. It may be blocking automated access.", "success": False})

                progress.progress((i + 1) / len(urls))

            status.markdown("<p style='color:#C8A96E; font-size:13px;'>✓ Analysis complete.</p>", unsafe_allow_html=True)

            for r in all_results:
                color = "#C8A96E" if r["success"] else "#ff6b6b"
                cleaned = r["analysis"].replace('\n\n\n', '\n\n').strip()
                st.markdown(f"""
                <div style="margin-top:24px">
                    <span class="output-label" style="color:{color};">{'✓' if r['success'] else '✗'} {r['url']}</span>
                    <div class="output-card">{cleaned}</div>
                </div>""", unsafe_allow_html=True)

            if all_results:
                full_report = "\n\n---\n\n".join([f"URL: {r['url']}\n\n{r['analysis']}" for r in all_results])
                st.download_button(
                    label="⬇️  Download Full Competitor Report",
                    data=full_report,
                    file_name="steadfast_competitor_analysis.txt",
                    mime="text/plain"
                )
        else:
            st.warning("Please enter your business type and at least one competitor URL.")


st.markdown('</div>', unsafe_allow_html=True)

# ── SECTION DIVIDER ───────────────────────────────────────
st.markdown('<div style="height:80px"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ── WHY STEADFAST ─────────────────────────────────────────
st.markdown("""
<div class="why-section">
    <div class="why-eyebrow">↳ The Problem We Solve</div>
    <div class="why-title">Agencies lose clients not from<br>bad work — but <span>bad admin.</span></div>
    <div class="why-sub">The invisible, repetitive tasks that pile up every single day are silently<br>killing your growth. Steadfast eliminates them completely.</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="padding: 0 60px; max-width:1100px; margin: 0 auto;">
<div class="problems-grid">
    <div class="problem-card">
        <div class="problem-icon">📭</div>
        <div class="problem-title">Follow-ups never get sent</div>
        <div class="problem-desc">After a great call, the follow-up email sits in your head for 3 days. The client moves on. The deal dies. This happens to every agency, every week.</div>
    </div>
    <div class="problem-card">
        <div class="problem-icon">🕐</div>
        <div class="problem-title">Reports eat your entire day</div>
        <div class="problem-desc">Monthly client reports take 3–5 hours each. Multiply that by 10 clients and you've lost an entire week every month just writing documents.</div>
    </div>
    <div class="problem-card">
        <div class="problem-icon">📵</div>
        <div class="problem-title">Voicemails pile up unactioned</div>
        <div class="problem-desc">Leads call. You don't pick up. The voicemail sits there. By the time you listen and respond, they've already hired someone else.</div>
    </div>
    <div class="problem-card">
        <div class="problem-icon">🕵️</div>
        <div class="problem-title">You have no idea what competitors are doing</div>
        <div class="problem-desc">Your competitors are changing pricing, launching services, and updating messaging. You find out 3 months later — if at all.</div>
    </div>
    <div class="problem-card">
        <div class="problem-icon">📧</div>
        <div class="problem-title">Cold outreach gets ignored</div>
        <div class="problem-desc">Generic cold emails get 1–2% reply rates. Personalised ones get 15–30%. But personalising 200 emails manually takes days you don't have.</div>
    </div>
    <div class="problem-card">
        <div class="problem-icon">🔥</div>
        <div class="problem-title">Always reacting, never growing</div>
        <div class="problem-desc">When admin takes 40% of your time, there's nothing left for strategy, new clients, or creative work. You're always putting out fires.</div>
    </div>
</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-divider" style="margin: 60px 60px 0;"></div>', unsafe_allow_html=True)

st.markdown("""
<div style="padding: 60px 60px 0; max-width:1100px; margin: 0 auto;">
    <div class="who-section-title">Built for every kind of agency</div>
    <div class="who-section-sub">Whether you're a solo freelancer or a growing team — if you deal with clients, Steadfast was made for you.</div>
    <div class="who-grid">
        <div class="who-card">
            <div class="who-icon">🧑‍💻</div>
            <div class="who-title">Freelancers</div>
            <div class="who-desc">Solo operators juggling 5+ clients with zero admin support. Every hour saved is an hour billed.</div>
        </div>
        <div class="who-card">
            <div class="who-icon">📣</div>
            <div class="who-title">Marketing Agencies</div>
            <div class="who-desc">Teams running campaigns, reports, and client calls simultaneously. Automate the repetitive. Focus on creative.</div>
        </div>
        <div class="who-card">
            <div class="who-icon">💼</div>
            <div class="who-title">Consultants</div>
            <div class="who-desc">High-value professionals whose time is billed by the hour. Every minute on admin is money lost.</div>
        </div>
        <div class="who-card">
            <div class="who-icon">🏢</div>
            <div class="who-title">Small to Large Businesses</div>
            <div class="who-desc">SMBs without a dedicated ops team. Steadfast becomes your back office without the salary.</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── CTA BAND ──────────────────────────────────────────────
st.markdown("""
<div class="cta-band">
    <div class="cta-title">Ready to run a <span>sharper agency?</span></div>
    <div class="cta-sub">Join agencies already using Steadfast to eliminate admin and focus entirely on growth.</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    with st.form("waitlist_form"):
        st.markdown("<p style='color:#888; font-size:13px; text-align:center; letter-spacing:1px; text-transform:uppercase; margin-bottom:16px;'>Join the waitlist — free beta access</p>", unsafe_allow_html=True)
        name = st.text_input("Your Name", placeholder="John Smith")
        email = st.text_input("Your Email", placeholder="john@agency.com")
        submitted = st.form_submit_button("Get Free Access →")

        if submitted:
            if name and email:
                sheet.append_row([name, email, datetime.now().strftime("%Y-%m-%d %H:%M")])
                st.success("You're on the list. We'll be in touch shortly.")
            else:
                st.warning("Please fill in both fields.")

st.markdown("""
<div style="text-align:center; padding-bottom:60px;">
    <div class="cta-note">No credit card required · Free during beta · Cancel anytime</div>
</div>
""", unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <div class="footer-left">STEADFAST</div>
    <div class="footer-right">
        © 2026 Steadfast
        <a href="mailto:hello@steadfastai.co">hello@steadfastai.co</a>
        <a href="#">Privacy</a>
        <a href="#">Terms</a>
    </div>
</div>
""", unsafe_allow_html=True)