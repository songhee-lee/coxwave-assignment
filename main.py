import streamlit as st

from config import settings
from llm import llm

st.title('네이버 스마트스토어의 FAQ 응대 챗봇')

# openAI API KEY 세팅
if not st.session_state.get("api_key") :
    st.session_state.api_key = ""

with st.sidebar:
    api_key = st.text_input("OpenAI API Key", value="", key="chatbot_api_key", type="password")
    st.session_state.api_key = llm.set_api_key(api_key)

# 최초 메세지 출력
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": settings.prompt.SYSTEM_PROMPT},
        {"role": "assistant", "content": "안녕하세요! 스마트스토어 고객센터입니다."}
    ]

# 메세지 전체 출력
for msg in st.session_state.messages:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])


# 유저 쿼리
if prompt := st.chat_input():
    # api key 입력 안된 경우
    if not st.session_state.api_key:
        st.info("Please add your proper OpenAI API key to continue.")
        st.stop()

    # 유저 쿼리 입력 받고 출력
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 유저 쿼리에 대한 답변 출력
    generated_text = llm.generate(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": generated_text})
    st.chat_message("assistant").write(generated_text)