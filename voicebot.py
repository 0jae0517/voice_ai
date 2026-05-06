import streamlit as st
import openai
import os
from datetime import datetime
from gtts import gTTS
import base64
from io import BytesIO

# 기능 구현 함수
def STT(audio_file, apikey):
    if not apikey:
        st.error("OpenAI API KEY를 입력해주세요.")
        st.stop()

    audio_bytes = audio_file.getvalue()
    file_obj = BytesIO(audio_bytes)
    file_obj.name = "input.wav"

    client = openai.OpenAI(api_key=apikey)
    response = client.audio.transcriptions.create(
        model="whisper-1",
        file=file_obj,
        language="ko"
    )

    return response.text

def ask_gpt(prompt, model, apikey):
    if not apikey:
        st.error("OpenAI API KEY를 입력해주세요.")
        st.stop()

    client = openai.OpenAI(api_key=apikey)
    response = client.chat.completions.create(
        model=model,
        messages=prompt
    )
    gptResponse = response.choices[0].message.content
    return gptResponse

def TTS(response):
    # gTTS를 활용하여 음성 파일 생성
    filename = "output.mp3"
    tts = gTTS(text=response, lang='ko')
    tts.save(filename)

    # 음원 파일 자동 재생
    with open(filename, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio autoplay>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(md, unsafe_allow_html=True)
    # 파일 삭제
    os.remove(filename)

# 메인 함수
def main():
    # 기본 설정
    st.set_page_config(
        page_title="영재의 음성 비서 ",
        layout="wide"
        )
    
    # session state 초기화 
    if "chat" not in st.session_state:
        st.session_state["chat"] = []

    if "OPENAI_API" not in st.session_state:
        st.session_state["OPENAI_API"] = ""

    if "message" not in st.session_state:
        st.session_state["message"] = [{"role": "system", "content": "You are a thoughtful assistant. Respond to all input in 25 words and answer in Korean"}]

    if "check_audio" not in st.session_state:
        st.session_state["check_audio"] = False
    # 초기화 정의
    if "check_reset" not in st.session_state:
        st.session_state["check_reset"] = False

    if "audio_key" not in st.session_state:
        st.session_state["audio_key"] = 0

    if "last_audio_bytes" not in st.session_state:
        st.session_state["last_audio_bytes"] = None

    if "last_question" not in st.session_state:
        st.session_state["last_question"] = ""

    # 제목
    st.header("영재의 음성 비서 ")

    # 구분선
    st.markdown("---")

    # 기본 설명
    with st.expander("음성 비서에 관하여", expanded=True):
        st.write(
            """
            - 음성 비서의 UI는 스트림릿을 활용했습니다.
            - STT(Speech-To-Text) 기능은 OpenAI의 Whisper AI를 활용했습니다.
            - TTS(Text-To-Speech) 기능은 gTTS(Google Text-to-Speech)를 활용했습니다.
            - 답변은 OpenAI의 GPT 모델을 활용했습니다.
            - TTS(Text-To-Speech)는 구글의 Google Translate TTS를 활용했습니다.
            """
        )

        st.markdown("")

    # 사이드 바 생성
    with st.sidebar:

        # OpenAI API 키 입력받기
        st.session_state["OPENAI_API"] = st.text_input(label="OPENAI API KEY", placeholder="Enter Your API Key", value=st.session_state["OPENAI_API"], type="password")

        st.markdown("---")

        # GPT 모델을 선택하기 위한 라디오 버튼 생성
        model_label = st.radio(label="GPT 모델", options=["정확도 우선(gpt-4)", "속도 우선(gpt-3.5-turbo)"])

        if model_label == "정확도 우선(gpt-4)":
            model = "gpt-4"
        else:
            model = "gpt-3.5-turbo"

        st.caption(f"선택된 모델: {model}")

        st.markdown("")

        # 리셋 버튼 생성
        if st.button(label="대화 및 녹음 초기화"):
            # 리셋 코드
            st.session_state["chat"] = []
            st.session_state["message"] = [{"role": "system", "content": "You are a thoughtful assistant. Respond to all input in 25 words and answer in Korean"}]
            st.session_state["check_reset"] = False
            st.session_state["audio_key"] += 1
            st.session_state["last_audio_bytes"] = None
            st.session_state["last_question"] = ""
            st.rerun()

    # 기능 구현 공간 
    col1, col2 = st.columns(2)

    with col1:
        # 왼쪽 영역 작성
        st.subheader("질문하기")

        if not st.session_state["OPENAI_API"]:
            st.warning("먼저 사이드바에서 OpenAI API KEY를 입력해주세요.")

        # 음성 녹음 아이콘 추가
        audio = st.audio_input(
            "클릭하여 녹음하기",
            sample_rate=16000,
            key=f"audio_input_{st.session_state['audio_key']}",
            disabled=not bool(st.session_state["OPENAI_API"])
        )

        if st.session_state["last_question"]:
            st.info(f"최근 인식된 질문: {st.session_state['last_question']}")

        if audio is not None and (st.session_state["check_reset"] == False):
            audio_bytes = audio.getvalue()

            if audio_bytes != st.session_state["last_audio_bytes"]:
                st.session_state["last_audio_bytes"] = audio_bytes
                st.audio(audio)

                try:
                    with st.spinner("음성을 텍스트로 변환하는 중입니다..."):
                        question = STT(audio, st.session_state["OPENAI_API"])

                    st.session_state["last_question"] = question
                    st.success("음성 인식 완료")
                    st.write(f"인식된 질문: {question}")

                    now = datetime.now().strftime("%H:%M")
                    st.session_state["chat"] = st.session_state["chat"] + [("user", now, question)]
                    st.session_state["message"] = st.session_state["message"] + [
                        {"role": "user", "content": question}
                    ]

                    with st.spinner("답변을 생성하는 중입니다..."):
                        response = ask_gpt(st.session_state["message"], model, st.session_state["OPENAI_API"])

                    # GPT 모델에 넣을 프롬프트를 위해 답변 내용 저장
                    st.session_state["message"] = st.session_state["message"] + [{"role": "assistant", "content": response}]

                    # 채팅 시각화를 위한 답변 내용 저장
                    now = datetime.now().strftime("%H:%M")
                    st.session_state["chat"] = st.session_state["chat"] + [("bot", now, response)]

                    with st.spinner("음성 답변을 생성하는 중입니다..."):
                        # gTTS를 활용하여 음성 파일 생성 및 재생
                        TTS(response)

                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")

    with col2:
        # 오른쪽 영역 작성
        st.subheader("질문/답변")

        if len(st.session_state["chat"]) == 0:
            st.info("아직 대화가 없습니다. 왼쪽에서 음성을 녹음해 질문해보세요.")

        # 채팅 형식으로 시각화하기
        for sender, time, message in st.session_state["chat"]:
            if sender == "user":
                with st.chat_message("user"):
                    st.write(message)
                    st.caption(time)
            else:
                with st.chat_message("assistant"):
                    st.write(message)
                    st.caption(time)

if __name__ == "__main__":
    main()
