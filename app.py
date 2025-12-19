import streamlit as st
import openai
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(layout="wide", page_title="AI Neural Engine")

# --- CUSTOM CSS (To match your Portfolio) ---
st.markdown("""
<style>
    .stApp {
        background-color: #050505;
        color: white;
    }
    h1, h2, h3, p, label, .stMarkdown {
        color: white !important;
        font-family: 'Poppins', sans-serif;
    }
    .stTextArea textarea {
        background-color: #111 !important;
        color: #00f2ff !important;
        border: 1px solid #bc13fe !important;
        font-family: 'Courier New', monospace;
    }
    div[data-baseweb="select"] > div {
        background-color: #111;
        color: white;
        border-color: #00f2ff;
    }
    button {
        background-color: transparent !important;
        border: 1px solid #00f2ff !important;
        color: #00f2ff !important;
        transition: 0.3s;
    }
    button:hover {
        background-color: #00f2ff !important;
        color: #000 !important;
        border-color: #00f2ff !important;
    }
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- API KEY SETUP ---
# Streamlit Secrets থেকে কি-টা নিবে
if "OPENAI_API_KEY" in st.secrets:
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("⚠️ OpenAI API Key Missing! Please add it to Streamlit Secrets.")
    st.stop()

# --- MAIN APP LAYOUT ---
st.markdown("<h3 style='text-align: center; color: #bc13fe !important; letter-spacing: 2px;'>NEURAL AI ENGINE</h3>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🕵️ DETECTOR", "🧬 HUMANIZER"])

# === TAB 1: AI DETECTOR ===
with tab1:
    st.caption("Scan text for GPT signatures using OpenAI Analysis")
    det_input = st.text_area("Paste text (min 10 words):", height=150, key="det")
    
    if st.button("SCAN PATTERNS"):
        if len(det_input.split()) < 10:
            st.warning("Text too short to analyze.")
        else:
            with st.spinner("Analyzing Perplexity & Burstiness..."):
                try:
                    # Advanced Prompt for Detection
                    response = client.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "You are an advanced AI detection algorithm. Analyze the given text for 'perplexity' (complexity) and 'burstiness' (sentence variation). If the text is monotonous and predictable, it is AI. If it is varied and complex, it is Human. Reply ONLY with a number between 0 and 100 representing the % probability that the text is AI-generated."},
                            {"role": "user", "content": det_input}
                        ],
                        temperature=0
                    )
                    score_str = response.choices[0].message.content.strip().replace('%', '')
                    try:
                        score = int(float(score_str))
                    except:
                        score = 50 # Fallback
                    
                    st.metric("AI Probability Score", f"{score}%")
                    
                    if score > 70:
                        st.error("VERDICT: 🤖 LIKELY AI GENERATED")
                        st.markdown(f"<div style='height:10px; width:100%; background:#333; border-radius:5px;'><div style='height:100%; width:{score}%; background:#ff2a2a; border-radius:5px;'></div></div>", unsafe_allow_html=True)
                    elif score < 30:
                        st.success("VERDICT: 👤 LIKELY HUMAN WRITTEN")
                        st.markdown(f"<div style='height:10px; width:100%; background:#333; border-radius:5px;'><div style='height:100%; width:{score}%; background:#00ff88; border-radius:5px;'></div></div>", unsafe_allow_html=True)
                    else:
                        st.warning("VERDICT: ⚠️ UNCERTAIN / MIXED")
                        st.markdown(f"<div style='height:10px; width:100%; background:#333; border-radius:5px;'><div style='height:100%; width:{score}%; background:#ffcc00; border-radius:5px;'></div></div>", unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Error: {str(e)}")

# === TAB 2: HUMANIZER ===
with tab2:
    st.caption("Rewrite text to bypass AI detectors (Ghost Protocol)")
    hum_input = st.text_area("Paste AI text here:", height=150, key="hum")
    mode = st.selectbox("Select Strategy", ["Standard Rewrite", "Academic Humanizer", "Ghost Protocol (Max Bypass)"])
    
    if st.button("HUMANIZE TEXT"):
        if not hum_input:
            st.warning("Please enter text first.")
        else:
            with st.spinner("Injecting human imperfections..."):
                try:
                    system_prompt = ""
                    if mode == "Standard Rewrite":
                        system_prompt = "Rewrite the following text to make it sound more natural and conversational. Keep the meaning the same."
                    elif mode == "Academic Humanizer":
                        system_prompt = "Rewrite this for an academic context. Use varied sentence structures and sophisticated vocabulary. Avoid common AI phrases like 'In conclusion', 'Delve', 'Crucial'. Increase perplexity."
                    else:
                        system_prompt = "You are a 'Ghost Writer'. Rewrite this text to aggressively bypass AI detectors. Instructions: 1. Mix very short sentences with long complex ones (High Burstiness). 2. Use rare synonyms. 3. Occasionally start sentences with conjunctions (And, But). 4. Remove all AI-typical words. Make it sound like a smart human wrote it."

                    response = client.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": hum_input}
                        ],
                        temperature=0.7
                    )
                    
                    result = response.choices[0].message.content
                    st.subheader("Humanized Result:")
                    st.text_area("Output", value=result, height=200)
                    st.success("✨ Text rewritten with high perplexity!")
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
