import streamlit as st

st.title("📚 국립부경대학교 도서관 챗봇")
st.write(
    "국립부경대학교 도서관 규정 전문을 바탕으로 질문에 정확하게 답변해 드립니다."
)

# 사이드바에서 저장된 OpenAI 클라이언트 가져오기
if "openai_client" in st.session_state:
  client = st.session_state["openai_client"]

  # 대화 기록 저장 세션 초기화
  if "library_messages" not in st.session_state:
    st.session_state.library_messages = []

  # 기존 대화 기록 출력
  for msg in st.session_state.library_messages:
    with st.chat_message(msg["role"]):
      st.markdown(msg["content"])

  # 사용자 입력 받기
  if prompt := st.chat_input(
      "도서관 휴관일이나 대출 권수에 대해 질문해 보세요..."
  ):
    st.session_state.library_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
      st.markdown(prompt)

    # 국립부경대학교 도서관 규정 전문
    full_regulations = """
        [국립부경대학교 도서관 규정]
        시행 2023.12.27. 부경대학교학교규정 제1316호

        제20조(휴관일) 도서관의 휴관일은 다음 각 호와 같다. 다만, 관장은 필요에 따라 이를 조정할 수 있다.
        1. 자료실: 공휴일, 개교기념일
        2. 일반열람실: 설날, 추석

        제22조(대출책수 및 기간) ① 단행본 대출 책 수 및 기간은 다음 각 호와 같다.
        1. 전임교원, 겸임교원, 명예교수, 강사: 50책 이내 90일
        2. 직원, 조교, 대학원생: 20책 이내 30일
        3. 학부생: 10책 이내 14일
        ② 제1항에 명시된 모든 사람들에 대한 전자책 대출 책 수는 5책 이내로 하며, 대출 기간은 5일로 하되, 연구원 및 도서관회원에게도 동일하게 적용한다.

        제23조(대출 제한 자료) 다음 각 호의 자료는 대출할 수 없다. 다만, 관장이 필요하다고 인정할 때 단기간 대출을 허가할 수 있다.
        1. 연속간행물 2. 참고자료 3. 학위논문 4. 귀중자료 5. 비도서자료 6. 관장이 지정한 그 밖의 자료

        제32조(자료대출 중지) 대출한 자료를 기한 내에 반납하지 아니하면 다른 자료 대출 및 도서관 이용을 중지한다.
        제33조(자료의 변상) 자료를 분실 또는 훼손하였을 경우에는 도서관에 신고하고 신고일로부터 10일 이내에 동일자료로 변상하여야 한다.
        """

    with st.chat_message("assistant"):
      # Responses API 및 instructions에 규정 전문 주입 + 스트리밍 응답
      stream = client.responses.create(
          model="gpt-6-luna",
          instructions=(
              "당신은 국립부경대학교 도서관 안내 챗봇입니다. 아래 명시된 국립부경대학교"
              " 도서관 규정을 바탕으로 사용자의 질문에 정확하게"
              f" 답변하세요.\n\n{full_regulations}"
          ),
          input=st.session_state.library_messages,
          stream=True,
      )
      response = st.write_stream(stream)
      st.session_state.library_messages.append(
          {"role": "assistant", "content": response}
      )
else:
  st.warning("👈 왼쪽 사이드바에 OpenAI API Key를 먼저 입력해주세요!")