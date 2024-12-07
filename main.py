import streamlit as st
import openai

st.title('네이버 스마트스토어의 FAQ 응대 챗봇')

# set the openai api key
if not st.session_state.get("api_key") :
    st.session_state.api_key = ""

with st.sidebar :
    st.session_state.api_key = st.text_input("OpenAI API Key", value="", key="chatbot_api_key", type="password")
    openai.api_key = st.session_state.api_key

# 시작 메세지
if "messages" not in st.session_state :
    st.session_state.messages = [{"role" : "assistant", "content" : "안녕하세요! 스마트스토어 고객센터입니다."}]

# 전체 메세지 출력
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 사용자 쿼리 입력
if prompt := st.chat_input() :
    # API key 입력이 안된 경우
    if not st.session_state.api_key :
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    
    # 사용자 쿼리
    st.session_state.messages.append({ "role" : "user", "content" : prompt})
    st.chat_message("user").write(prompt)

    # openai 답변
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=st.session_state.messages
    )
    generated_text = response.to_dict()["choices"][0]["message"]["content"]

    st.session_state.messages.append({"role": "assistant", "content": generated_text})
    st.chat_message("assistant").write(generated_text)