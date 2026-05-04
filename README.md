# 음성 비서 프로그램 (Voice Assistant with Streamlit & OpenAI)

## 프로젝트 소개
이 프로젝트는 **Streamlit** 기반 UI와 **OpenAI API**를 활용하여 음성 인식(STT), 대화형 응답(GPT), 음성 출력(TTS)을 구현한 간단한 음성 비서 애플리케이션입니다.  
사용자는 음성으로 질문을 입력하고, GPT 모델의 답변을 **텍스트와 음성**으로 받을 수 있습니다.

## 주요 기능
-  **STT (Speech-to-Text)**: OpenAI Whisper 모델을 활용해 음성을 텍스트로 변환  
-  **대화형 응답**: GPT-4 / GPT-3.5-turbo 모델을 통해 질문에 대한 답변 생성  
-  **TTS (Text-to-Speech)**: gTTS를 활용해 GPT 답변을 음성으로 변환 및 재생  
-  **채팅 UI**: Streamlit을 활용한 직관적인 대화 인터페이스 제공  
-  **API Key 관리**: 사이드바에서 OpenAI API Key 입력 및 모델 선택 가능  

## 사용 기술
- Python  
- Streamlit  
- OpenAI Whisper, GPT 모델  
- gTTS (Google Text-to-Speech)  
- HTML/CSS 기반 채팅 UI 커스터마이징  

## 실행 방법
```bash
# 저장소 클론
git clone https://github.com/username/repo-name.git
cd repo-name

# 필요한 라이브러리 설치
pip install -r requirements.txt

# 실행
streamlit run app.py
