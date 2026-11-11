from openai import OpenAI
import streamlit as st

with st.sidebar:
  api_key = st.text_input("OpenAI API Key", type="password")
  if api_key:
    st.session_state["openai_client"] = OpenAI(api_key=api_key)

pg = st.navigation([
    st.Page("app_pages/Home.py", title="Home", icon=":material/home:"),
    st.Page("app_pages/Chat.py", title="Chat", icon=":material/chat:"),
    st.Page(
        "app_pages/ChatPDF.py", title="ChatPDF", icon=":material/description:"
    ),
    st.Page(
        "app_pages/Library.py",
        title="도서관 챗봇",
        icon=":material/local_library:",
    ),
])

pg.run()