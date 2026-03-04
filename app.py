import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="LLM Final Task", page_icon="💻")

st.title("💻 LLM Final Task")
st.write("A chatbot that helps you write and review code.")

# Sidebar
mode = st.sidebar.selectbox(
    "Select Mode",
    ["Coding Assistant", "Code Reviewer"]
)

api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []

# System prompts
ASSISTANT_PROMPT = """
You are an expert coding assistant.
Help the user write clean, efficient code.
Explain your reasoning step by step.
"""

REVIEWER_PROMPT = """
You are a senior code reviewer.
Analyze the provided code for bugs,
security issues, performance problems,
and style improvements.
Provide actionable feedback.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

# show previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Ask something about code...")

if prompt:

    if not api_key:
        st.error("Please enter your API key.")
        st.stop()

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-flash-latest")

    system_prompt = ASSISTANT_PROMPT if mode == "Coding Assistant" else REVIEWER_PROMPT

    full_prompt = system_prompt + "\nUser: " + prompt

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        response = model.generate_content(full_prompt)
        answer = response.text

    except Exception as e:
        answer = f"Error: {str(e)}"

    st.session_state.messages.append({"role": "assistant", "content": answer})

    with st.chat_message("assistant"):
        st.markdown(answer)

    