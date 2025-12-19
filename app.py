# app.py ফাইলের কোড আপডেট
import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="My AI Portfolio", page_icon="🤖")

# --- সিক্রেট থেকে API Key নেওয়া ---
# এখন আর কোডে কি (Key) দেখা যাবে না, এটি সার্ভারের গোপন ভল্ট থেকে আসবে
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)

st.title("🤖 My AI Assistant")
st.write("Ask me anything related to my portfolio!")

user_input = st.text_input("Enter your prompt here:", placeholder="Ex: Who are you?")

if st.button("Generate Answer"):
    if user_input:
        try:
            with st.spinner("Thinking..."):
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(user_input)
                st.success("Response:")
                st.write(response.text)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter some text first!")
