import streamlit as st
from bson.objectid import ObjectId
from utils import send_api

st.title("네이버 스마트스토어의 FAQ 응대 챗봇")

# taskId 세팅
if not st.session_state.get("taskId"):
    st.session_state.taskId = str(ObjectId())

# 최초 메세지 출력
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕하세요! 스마트스토어 고객센터입니다."}
    ]

# 메세지 전체 출력
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 유저 쿼리
if prompt := st.chat_input("궁금한 점을 입력해주세요."):
    # 유저 쿼리 입력 받고 출력
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 유저 쿼리에 대한 답변 출력
    with st.spinner("Generating the answer..."):
        data = {
            "service": "naver_store_faq",
            "taskId": st.session_state.taskId,
            "messages": st.session_state.messages,
        }

        try:
            response = send_api(data, "/api/chat_stream")
            response.raise_for_status()  # HTTP Error Check

            # 스트리밍 출력
            with st.chat_message("assistant"):
                output_area = st.empty()  # 스트리밍 출력을 위한 공간 생성
                current_text = ""
                for chunk in response.iter_content(chunk_size=1024):
                    current_text += chunk.decode("utf-8")
                    output_area.markdown(current_text)
        except Exception as e:
            st.error(f"Request failed : {e}")
            current_text = f"Error : {str(e)}"
        st.session_state.messages.append({"role": "assistant", "content": current_text})
