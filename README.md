# YW Labs AI Chatbot

영우랩스의 AI 챗봇 프로젝트입니다. 이 프로젝트는 회사 정보, 휴가 관리, 직원 정보 등에 대한 질문에 답변할 수 있는 지능형 챗봇 시스템을 제공합니다.

## 목차

- [주요 기능](#주요-기능)
- [기술 스택](#기술-스택)
- [시스템 요구사항](#시스템-요구사항)
- [설치 및 실행](#설치-및-실행)
- [프로젝트 구조](#프로젝트-구조)
- [API 문서](#api-문서)
- [개발 가이드](#개발-가이드)
- [테스트](#테스트)
- [배포](#배포)
- [문제 해결](#문제-해결)
- [기여](#기여)
- [라이선스](#라이선스)

## 주요 기능

### 1. 회사 정보 및 소개
- 회사 연혁 및 비전
- 조직 구조
- 주요 서비스 및 제품
- 뉴스 및 공지사항

### 2. 휴가 관리 시스템
- 휴가 신청 및 조회
- 휴가 정책 안내
- 휴가 일정 캘린더
- 승인 프로세스 안내

### 3. 직원 정보 조회
- 조직도 조회
- 연락처 정보
- 부서별 정보
- 직원 검색

### 4. 자연어 기반 질의응답
- 문맥 이해 및 응답
- 다국어 지원
- 대화 이력 관리
- 맞춤형 응답 생성

### 5. 벡터 기반 유사도 검색
- 의미 기반 검색
- 유사 질문 매칭
- 검색 결과 순위화
- 실시간 검색

## 기술 스택

### Backend
- Python 3.8+
- Flask 2.0+
- SQLAlchemy
- OpenAI API
- LangChain
- FAISS

### Frontend
- React 18
- TypeScript
- Material-UI
- Redux Toolkit
- Axios

### Database
- SQLite
- Redis (캐싱)

### DevOps
- Docker
- GitHub Actions
- Nginx

## 시스템 요구사항

### 최소 요구사항
- Python 3.8 이상
- Node.js 16 이상
- 4GB RAM
- 10GB 저장 공간

### 권장 사항
- Python 3.10 이상
- Node.js 18 이상
- 8GB RAM
- 20GB 저장 공간

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
`.env` 파일을 생성하고 다음 환경 변수를 설정합니다:
```env
OPENAI_API_KEY=your_api_key
DATABASE_URL=sqlite:///app.db
REDIS_URL=redis://localhost:6379
```

4. 데이터베이스 초기화
```bash
python backend/init_db.py
```

5. 백엔드 서버 실행
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

2. 환경 변수 설정
`.env` 파일을 생성하고 다음 환경 변수를 설정합니다:
```env
REACT_APP_API_URL=http://localhost:5000
```

3. 개발 서버 실행
```bash
npm run dev
```

## 프로젝트 구조

# 프로젝트 폴더 구조 및 공통 모듈 가이드 (2024-06 기준)

## 1. 핵심 폴더 구조

```
backend/
├── core/
│   ├── handlers/      # intent별 후처리 핸들러 함수/클래스 (핸들러 패턴)
│   ├── embeddings/    # 임베딩 모델 래퍼 및 벡터 유틸 (HuggingFace/OpenAI 등)
│   ├── utils/         # 범용 유틸리티 함수 (날짜, 문자열 등)
│   ├── parsers/       # 파일/문서 파서(텍스트, PDF, 이미지 등)
│   └── converters/    # 도메인별 Document 변환 함수
├── services/          # 비즈니스 로직(서비스 계층)
├── common/            # 로깅, 예외 등 공통 infra
└── ...
```

- 각 core 하위 폴더에는 반드시 `__init__.py`가 포함되어 패키지로 인식됩니다.
- 서비스 레이어에서는 반드시 core 하위 모듈을 import해서 사용합니다.

## 2. intent별 후처리 구조
- intent별 후처리/DB조회/템플릿 로직은 core/handlers 하위의 핸들러 함수로 분리되어 있습니다.
- intent가 추가될 때는 handler만 추가/수정하면 됩니다.
- intent → handler 매핑은 `core/handlers/intent_handler_map.py`에서 관리합니다.

## 3. 임베딩/유틸/파서/컨버터 구조
- 임베딩 모델 래퍼(`get_hf_embedding`, `get_openai_embedding` 등)는 core/embeddings에 위치합니다.
- 범용 유틸 함수는 core/utils, 도메인별 Document 변환 함수는 core/converters, 파일/문서 파서는 core/parsers에 위치합니다.

## 4. 실무적 장점
- 모든 공통 모듈이 core 하위에 일원화되어 확장성, 유지보수성, 협업 효율이 크게 향상됩니다.
- 서비스 코드는 비즈니스 로직에만 집중할 수 있습니다.

---

### 예시: intent별 핸들러 패턴 사용

```python
from core.handlers.intent_handler_map import INTENT_HANDLER_MAP

handler = INTENT_HANDLER_MAP.get(intent_tag)
if handler:
    return handler(user_message, meta, response)
```

---

> 이 구조는 실무적 확장성과 유지보수성을 극대화하기 위해 설계되었습니다.

## API 문서

### 채팅 API
- `POST /api/chat`
  - 요청: `{ "message": "string", "context": "string" }`
  - 응답: `{ "response": "string", "type": "string" }`

### 벡터 스토어 API
- `POST /api/vector/update`
  - 요청: `{ "pattern_id": "string", "pattern_text": "string" }`
  - 응답: `{ "status": "string" }`

### 직원 정보 API
- `GET /api/employee/{id}`
  - 응답: `{ "name": "string", "department": "string", ... }`

## 개발 가이드

### 코드 스타일
- Python: PEP 8 준수
- JavaScript: ESLint 규칙 준수
- TypeScript: strict 모드 사용

### Git 워크플로우
1. feature/* 브랜치 생성
2. 개발 및 테스트
3. PR 생성
4. 코드 리뷰
5. main 브랜치 병합

## 테스트

### 백엔드 테스트
```bash
cd backend
pytest
```

### 프론트엔드 테스트
```bash
cd frontend
npm test
```

## 배포

### Docker 배포
```bash
docker-compose up -d
```

### 수동 배포
1. 백엔드 빌드
```bash
cd backend
python -m build
```

2. 프론트엔드 빌드
```bash
cd frontend
npm run build
```

## 문제 해결

### 일반적인 문제
1. 데이터베이스 연결 오류
   - 데이터베이스 서버 상태 확인
   - 연결 문자열 확인

2. API 응답 지연
   - 캐시 설정 확인
   - 로그 확인

### 로그 확인
- 백엔드: `backend/logs/`
- 프론트엔드: 브라우저 개발자 도구

## 기여

1. 이슈 생성
2. 브랜치 생성
3. 변경사항 커밋
4. PR 생성

## 라이선스

이 프로젝트는 영우랩스의 내부 사용을 위한 프로젝트입니다.