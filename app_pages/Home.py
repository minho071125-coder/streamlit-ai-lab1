import base64
from openai import OpenAI
import streamlit as st

st.title("🏠 Home - 생성 AI 응용프로그래밍")
st.write("사이드바에서 API Key를 입력한 뒤 아래 기능을 사용해 보세요!")

# 사이드바에서 저장된 클라이언트 가져오기
if "openai_client" in st.session_state:
  client = st.session_state["openai_client"]

  st.write("---")
  st.subheader("💬 실습 3: 텍스트 생성")

  user_prompt = st.text_input("질문을 입력하세요:")
  if user_prompt:
    response = client.responses.create(
        model="gpt-6-luna",
        input=user_prompt,
    )
    st.write(response.output_text)

  st.write("---")
  st.subheader("🎨 실습 4: 이미지 생성")

  img_prompt = st.text_input("생성할 이미지의 설명을 입력하세요:")
  if st.button("이미지 생성"):
    with st.spinner("이미지를 생성 중입니다... 잠시만 기다려주세요!"):
      img = client.images.generate(
          model="gpt-image-2.6-flare",
          prompt=img_prompt,
      )
      image_bytes = base64.b64decode(img.data[0].b64_json)
      st.image(image_bytes)
else:
  st.warning("👈 왼쪽 사이드바에 OpenAI API Key를 먼저 입력해주세요!")
