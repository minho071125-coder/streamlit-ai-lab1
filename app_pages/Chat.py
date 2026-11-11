import streamlit as st

st.title("💬 Chat - 실시간 스트리밍 챗봇")
st.write("이전 대화를 기억하고 실시간으로 답변하는 챗봇입니다.")

# 사이드바에 저장된 OpenAI 클라이언트 가져오기
if "openai_client" in st.session_state:
  client = st.session_state["openai_client"]

  # 대화 기록을 저장할 세션 상태 초기화
  if "messages" not in st.session_state:
    st.session_state.messages = []


  # Clear 버튼 클릭 시 대화 내용 초기화 함수
  def clear_chat():
    st.session_state.messages = []


  # 대화 내용 초기화 버튼
  st.button("Clear 대화 내용 삭제", on_click=clear_chat)

  # 기존 대화 기록 화면에 출력하기
  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

  # 사용자의 입력 받기
  if prompt := st.chat_input("메시지를 입력하세요..."):
    # 사용자 메시지를 세션에 추가하고 화면에 표시
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
      st.markdown(prompt)

    # 어시스턴트의 스트리밍 응답 생성
    with st.chat_message("assistant"):
      stream = client.responses.create(
          model="gpt-6-luna",
          input=st.session_state.messages,
          stream=True,
      )
      response = st.write_stream(stream)
      # 응답 내용을 세션에 추가
      st.session_state.messages.append(
          {"role": "assistant", "content": response}
      )
else:
  st.warning("👈 왼쪽 사이드바에 OpenAI API Key를 먼저 입력해주세요!")