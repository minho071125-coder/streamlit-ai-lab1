import streamlit as st

st.title("📄 ChatPDF - 문서 기반 Q&A 챗봇")
st.write("PDF 파일을 업로드하고 문서 내용에 대해 자유롭게 질문해 보세요!")

if "openai_client" in st.session_state:
  client = st.session_state["openai_client"]

  uploaded_file = st.file_uploader("PDF 파일을 선택하세요", type=["pdf"])

  if uploaded_file is not None:
    st.success("PDF 파일이 성공적으로 업로드되었습니다!")

    question = st.text_input("업로드된 문서에 대해 질문하세요:")
    if question:
      with st.spinner("문서 내용을 분석하고 답변을 생성하는 중입니다..."):
        response = client.responses.create(
            model="gpt-6-luna",
            input=f"다음 문서 내용을 참고하여 질문에 답해주세요.\n질문: {question}",
        )
        st.write(response.output_text)
else:
  st.warning("👈 왼쪽 사이드바에 OpenAI API Key를 먼저 입력해주세요!")