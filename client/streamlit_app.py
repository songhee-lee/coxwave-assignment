import streamlit as st
from bson.objectid import ObjectId

from utils import send_api

st.title('네이버 스마트스토어의 FAQ 응대 챗봇')

# taskId 세팅
if not st.session_state.get("taskId") :
    st.session_state.taskId = str(ObjectId())

# 최초 메세지 출력
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "안녕하세요! 스마트스토어 고객센터입니다."}]

# 메세지 전체 출력
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 유저 쿼리
if prompt := st.chat_input("궁금한 점을 입력해주세요."):
    # 유저 쿼리 입력 받고 출력
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 유저 쿼리에 대한 답변 출력
    with st.spinner("Generating the answer...") :
        data = {
            "service" : "naver_store_faq",
            "taskId" : st.session_state.taskId,
            "messages" : st.session_state.messages,
        }

        response = send_api(data, "/api/chat")
        if "generated_text" in response :
            generated_text = response["generated_text"]
        else :
            generated_text = response["error"]

        st.session_state.messages.append({"role": "assistant", "content": generated_text})
        st.chat_message("assistant").write(generated_text)