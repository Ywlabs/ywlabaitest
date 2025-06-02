# YW Labs AI Chatbot

영우랩스의 AI 챗봇 프로젝트입니다. 이 프로젝트는 회사 정보, 휴가 관리, 직원 정보 등에 대한 질문에 답변할 수 있는 지능형 챗봇 시스템을 제공합니다.

## 주요 기능

- 회사 정보 및 소개
- 휴가 관리 시스템
- 직원 정보 조회
- 자연어 기반 질의응답
- 벡터 기반 유사도 검색

## 기술 스택

- Backend: Python, Flask
- Frontend: React
- Database: SQLite
- AI/ML: LangChain, OpenAI
- Vector Store: FAISS

## 설치 및 실행

### 백엔드 설정

1. Python 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. 의존성 설치
```bash
pip install -r requirements.txt
```

3. 환경 변수 설정
`.env` 파일을 생성하고 필요한 환경 변수를 설정합니다.

4. 백엔드 서버 실행
```bash
cd backend
python app.py
```

### 프론트엔드 설정

1. 의존성 설치
```bash
cd frontend
npm install
```

2. 개발 서버 실행
```bash
npm run dev
```

## 프로젝트 구조

```
.
├── backend/
│   ├── app.py
│   ├── routes/
│   ├── services/
│   └── common/
├── frontend/
│   ├── src/
│   └── public/
└── README.md
```

## API 엔드포인트

- `/api/chat`: 챗봇 대화 API
- `/api/vector`: 벡터 스토어 관리 API
- `/api/employee`: 직원 정보 관리 API

## 라이선스

이 프로젝트는 영우랩스의 내부 사용을 위한 프로젝트입니다.