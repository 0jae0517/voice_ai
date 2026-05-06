# 영재의 음성 비서

Streamlit을 기반으로 제작한 한국어 음성 비서 웹 애플리케이션입니다.  
사용자가 마이크로 질문을 녹음하면 음성을 텍스트로 변환하고, GPT 모델을 통해 답변을 생성한 뒤, 생성된 답변을 음성으로 재생합니다.

## 주요 기능

- 마이크를 이용한 음성 질문 입력
- OpenAI Whisper를 활용한 음성 인식(STT)
- OpenAI GPT 모델을 활용한 답변 생성
- gTTS를 활용한 한국어 음성 답변 출력(TTS)
- 대화 기록 표시
- 대화 및 녹음 초기화 기능
- GPT 모델 선택 기능

## 사용 기술

| 구분 | 기술 |
|---|---|
| 개발 언어 | Python |
| 웹 프레임워크 | Streamlit |
| 음성 인식 | OpenAI Whisper API |
| 답변 생성 | OpenAI GPT API |
| 음성 출력 | gTTS |
| 배포 | Streamlit Community Cloud |

## 프로젝트 구조

```text
voice_ai/
├── voicebot.py
├── requirements.txt
└── README.md
```

## 설치 방법

1. 저장소를 클론합니다.

```bash
git clone https://github.com/0jae_0517/voice_ai.git
cd voice_ai
```

2. 필요한 패키지를 설치합니다.

```bash
pip install -r requirements.txt
```

3. Streamlit 앱을 실행합니다.

```bash
streamlit run voicebot.py
```

## requirements.txt

```txt
streamlit>=1.56.0
openai
gTTS
```

## 사용 방법

1. 앱을 실행합니다.
2. 사이드바에 OpenAI API Key를 입력합니다.
3. 사용할 GPT 모델을 선택합니다.
4. `클릭하여 녹음하기` 버튼을 눌러 질문을 녹음합니다.
5. 녹음이 완료되면 음성이 텍스트로 변환됩니다.
6. GPT가 질문에 대한 답변을 생성합니다.
7. 답변이 화면에 표시되고 음성으로 재생됩니다.
8. 초기화 버튼을 누르면 대화 기록과 녹음 입력이 초기화됩니다.

## 주요 코드 설명

### 1. STT 기능

사용자의 음성 입력을 OpenAI Whisper API를 통해 텍스트로 변환합니다.

```python
response = client.audio.transcriptions.create(
    model="whisper-1",
    file=file_obj,
    language="ko",
)
```

`language="ko"` 옵션을 통해 한국어 음성 인식을 지정합니다.

### 2. GPT 답변 생성

음성에서 변환된 질문을 GPT 모델에 전달하여 답변을 생성합니다.

```python
response = client.chat.completions.create(
    model=model,
    messages=prompt
)
```

사용자는 사이드바에서 `gpt-4` 또는 `gpt-3.5-turbo` 모델을 선택할 수 있습니다.

### 3. TTS 기능

GPT가 생성한 답변을 gTTS를 이용해 한국어 음성 파일로 변환하고 자동 재생합니다.

```python
tts = gTTS(text=response, lang='ko')
tts.save(filename)
```

### 4. 초기화 기능

초기화 버튼을 누르면 대화 기록, GPT 메시지 기록, 음성 입력 상태가 초기화됩니다.

```python
st.session_state["chat"] = []
st.session_state["message"] = [{"role": "system", "content": "You are a thoughtful assistant. Respond to all input in 25 words and answer in Korean"}]
st.session_state["check_reset"] = False
st.session_state["audio_key"] += 1
st.rerun()
```

## Streamlit Cloud 배포 방법

1. GitHub에 프로젝트 파일을 업로드합니다.
2. Streamlit Community Cloud에 접속합니다.
3. GitHub 저장소를 연결합니다.
4. 메인 파일 경로를 `voicebot.py`로 설정합니다.
5. 배포를 실행합니다.

## 배포 시 주의사항

- `requirements.txt`에 `audiorecorder`, `pyaudio`, `pydub`를 넣지 않습니다.
- 현재 코드는 Streamlit 기본 위젯인 `st.audio_input()`을 사용합니다.
- OpenAI API Key는 코드에 직접 작성하지 않고, 앱 실행 후 사이드바에서 입력합니다.
- 마이크 권한이 허용되어 있어야 음성 녹음이 가능합니다.
- Streamlit Cloud 배포 시 Python 버전은 3.11 또는 3.12 사용을 권장합니다.

## 오류 해결

### 1. OpenAI API KEY를 입력해주세요.

사이드바에 OpenAI API Key가 입력되지 않은 상태입니다.  
API Key를 입력한 뒤 다시 녹음해주세요.

### 2. 음성이 이상하게 인식되는 경우

다음 사항을 확인합니다.

- 마이크 권한이 허용되어 있는지 확인
- 녹음된 음성이 실제로 잘 들리는지 확인
- 너무 짧게 말하지 않고 2~3초 이상 또렷하게 말하기
- 주변 소음이 적은 환경에서 녹음하기

### 3. pyaudio 또는 portaudio 오류가 발생하는 경우

`requirements.txt`에 다음 패키지가 들어가 있는지 확인합니다.

```txt
audiorecorder
pyaudio
pydub
```

현재 프로젝트에서는 위 패키지가 필요하지 않습니다.  
`requirements.txt`는 아래처럼 유지하는 것을 권장합니다.

```txt
streamlit>=1.56.0
openai
gTTS
```

## 향후 개선 방향

- 텍스트 직접 입력 기능 추가
- 답변 길이 조절 옵션 추가
- 음성 인식 결과 수정 기능 추가
- API Key를 Streamlit Secrets로 관리
- 대화 기록 다운로드 기능 추가
- GPT 모델 선택지를 사용자 친화적인 이름으로 변경

## 라이선스

본 프로젝트는 학습 및 포트폴리오 목적으로 제작되었습니다.
