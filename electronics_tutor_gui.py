import streamlit as st
from chat_with_local_model import get_bot_reply

st.set_page_config(page_title="Electronics Tutor Bot", page_icon="⚡")

st.title("⚡ Electronics Tutor Bot (Offline)")
st.write("Ask me questions about electronics! I’ll try my best to help.")

# Input box
user_input = st.text_input("Enter your question:")

# When user clicks the button
if st.button("Ask") and user_input:
    reply, source = get_bot_reply(user_input)
    st.markdown(f"**Answer ({source.upper()}):**")
    st.write(reply)

    # Log to file
    with open("chat_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{source}] You: {user_input}\nBot: {reply}\n\n")
