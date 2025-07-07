import streamlit as st
from chat_with_local_model import get_bot_reply

st.set_page_config(page_title="Electronics Tutor Bot", page_icon="⚡")

st.title("⚡ Electronics Tutor Bot (Offline)")
st.markdown(
    "Ask questions about basic electronics. I’ll either answer from memory or use a local AI model."
)

with st.form("chat_form"):
    user_input = st.text_input("Your question")
    submitted = st.form_submit_button("Ask")

if submitted and user_input:
    if user_input.strip():
        with st.spinner("🤖 Thinking..."):
            reply, source = get_bot_reply(user_input)

        st.success(f"**Answer ({source.upper()}):**")
        st.write(reply)

    # Save chat to log
    with open("chat_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{source}] You: {user_input}\nBot: {reply}\n\n")
