# Minor tweak to trigger redeploy

import streamlit as st
from groq import Groq

# ---- Page Config ----
st.set_page_config(page_title="Chemistry Mnemonics", page_icon="🧪")

# ---- Header Section ----
st.markdown("<h1 style='text-align: center;'>🧪 Chemistry Mnemonic Helper</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Struggling with chemistry? Just ask, and get an easy mnemonic to remember it forever! ✨</p>", unsafe_allow_html=True)
st.divider()

# ---- Topic Input ----
col1, col2 = st.columns([3, 1])
with col1:
    user_input = st.text_area("🧠 Enter a chemistry topic or question:", height=120)

with col2:
    popular_topics = [
        "Reactivity Series",
        "Electrochemical Series",
        "Periodic Table Groups",
        "Acid/Base Indicators",
        "Types of Bonds",
        "s, p, d, f block elements"
    ]
    topic_choice = st.selectbox("🔥 Quick Topics", ["Choose a topic..."] + popular_topics)

if topic_choice != "Choose a topic..." and not user_input:
    user_input = topic_choice

# ---- Generate Button ----
if st.button("✨ Generate Mnemonic"):
    if not user_input.strip():
        st.warning("⚠️ Please enter a topic/question.")
    else:
        try:
            # Initialize Groq client
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])

            with st.spinner("🔍 Generating a clever mnemonic for you..."):
                response = client.chat.completions.create(
                    model="llama3-70b-8192",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a creative and friendly tutor. For any chemistry topic given, provide a fun and easy mnemonic to help students remember it better. Keep it short and memorable!"
                        },
                        {
                            "role": "user",
                            "content": user_input
                        }
                    ]
                )

                mnemonic = response.choices[0].message.content

                st.success("Here's your mnemonic 👇")
                st.markdown(f"<div style='background-color:#f0f8ff; padding:15px; border-radius:10px; font-size:18px;'>{mnemonic}</div>", unsafe_allow_html=True)

                # Copy button
                st.code(mnemonic, language="markdown")

        except Exception as e:
            st.error(f"❌ Oops, something went wrong:\n{e}")
