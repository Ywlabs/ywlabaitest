# YW Labs AI Chatbot

영우랩스의 AI 챗봇 프로젝트입니다. 이 프로젝트는 회사 정보, 휴가 관리, 직원 정보, 정책 안내 등 다양한 사내 정보를 자연어로 질의·응답할 수 있는 지능형 챗봇 시스템을 제공합니다.

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
- 회사 연혁, 비전, 조직 구조, 서비스/제품, 공지사항 안내

### 2. 휴가 관리 시스템
- 휴가 신청/조회, 정책 안내, 일정 캘린더, 승인 프로세스 안내

### 3. 직원 정보 조회
- 조직도, 연락처, 부서별 정보, 직원 검색

### 4. 정책/규정 안내 (RAG)
- 사내 정책/규정 문서 기반 RAG(검색+생성) 답변
- 정책/복지/매출 등 도메인별 문서 검색 및 요약

### 5. 자연어 기반 질의응답
- 문맥 이해, 맞춤형 응답, 다국어 지원, 대화 이력 관리

### 6. 벡터 기반 유사도 검색
- 의미 기반 검색, 유사 질문 매칭, 실시간 검색, 임계값 기반 품질 제어

### 7. 위젯/링크/동적 응답
- 매출/복지 등 위젯 연동, 사내 시스템 링크 제공, 동적 파라미터 처리

## 기술 스택

### Backend
- Python 3.8+
- Flask 2.0+
- LangChain
- ChromaDB (벡터스토어)
- OpenAI API
- SQLAlchemy
- MySQL (운영 DB)
- Redis (선택적 캐싱)

### Frontend
- **Vue.js 3.0**
- TypeScript
- Pinia (상태관리)
- Vite (번들러)
- Axios
- Element Plus (UI)
- marked (Markdown 파서)
- dompurify (HTML Sanitizer)
- Lottie-web (애니메이션)

### Database
- MySQL (운영)
- ChromaDB (벡터스토어)
- SQLite (개발/테스트, 선택)

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
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=ywlabs
MYSQL_PORT=3306
```

4. 데이터베이스 초기화
```bash
# 예시: 초기화 스크립트가 있다면 실행
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
VITE_API_BASE_URL=http://localhost:5000
```

3. 개발 서버 실행
```bash
npm run dev
```

## 프로젝트 구조 (2024-06 최신)

```
backend/
├── core/
│   ├── handlers/      # intent별 후처리 핸들러(핸들러 패턴, 확장성/유지보수성)
│   ├── embeddings/    # 임베딩 모델 래퍼 및 벡터 유틸(HuggingFace/OpenAI 등)
│   ├── utils/         # 범용 유틸리티 함수(날짜, 문자열 등)
│   ├── parsers/       # 파일/문서 파서(텍스트, PDF, 이미지 등)
│   └── converters/    # 도메인별 Document 변환 함수(위젯 등)
├── services/          # 비즈니스 로직(서비스 계층, DB/외부연동/핸들러 호출)
├── common/            # 로깅, 예외, 공통 infra
├── memory-bank/       # 정책/진행상황/컨텍스트/이슈 등 메모리 뱅크(운영/개발 싱크)
├── database/          # DB 연결/초기화/쿼리
├── config/            # 환경설정, 상수, 시크릿
├── logs/              # 백엔드 로그
└── ...
frontend/
├── src/components/    # ChatInterface, 공통 UI 컴포넌트
├── src/widgets/       # 매출/복지 등 도메인별 위젯
├── src/views/         # 주요 페이지/화면
├── src/store/         # Pinia 상태관리
├── src/utils/         # 프론트 유틸 함수
└── ...
```

- **core/**: 모든 공통 모듈 일원화(핸들러, 임베딩, 유틸, 파서, 컨버터)
  - 서비스 계층에서는 반드시 core 하위 모듈만 import
  - intent별 후처리/DB조회/템플릿 로직은 core/handlers 하위 핸들러로 분리, intent→handler 매핑은 코드 내에서 관리(예시: INTENT_HANDLER_MAP)
- **services/**: 실제 비즈니스 로직(핸들러 호출, DB/외부 API 연동 등)
- **memory-bank/**: 정책/진행상황/컨텍스트/이슈 등 기록, 코드-정책-운영 싱크 유지. 문서 기반으로 프로젝트의 모든 의사결정과 진행상황을 체계적으로 관리함.
- **frontend/**: **Vue.js 3.0** 기반, ChatInterface/위젯/상태관리 등 컴포넌트화

### 실무적 장점
- 모든 공통/핵심 모듈이 core 하위에 일원화되어 확장성, 유지보수성, 협업 효율이 크게 향상됨
- 서비스 코드는 비즈니스 로직에만 집중, 정책/핸들러/템플릿/유틸 등은 core에서 일관 관리
- memory-bank로 정책/진행상황/컨텍스트/이슈를 명확히 관리, 코드-운영 싱크 보장

### 예시: intent별 핸들러 패턴
```python
from core.handlers import employee_info_handler, sales_status_handler
INTENT_HANDLER_MAP = {
    'employee_info': employee_info_handler,
    'sales_status': sales_status_handler,
    # ...
}
handler = INTENT_HANDLER_MAP.get(intent_tag)
if handler:
    return handler(user_message, meta, response)
```

## API 문서

### 채팅 API
- `POST /api/chat`
  - 요청: `{ "message": "string" }`
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
- Python: PEP 8, 함수별 한글 docstring, response_type 기반 분기, [USER] 로그 포맷 등 준수
- JavaScript/TypeScript: ESLint, strict 모드, 컴포넌트/스토어 분리

### Git 워크플로우
1. feature/* 브랜치 생성
2. 개발 및 테스트
3. PR 생성
4. 코드 리뷰
5. main 브랜치 병합

### 메모리 뱅크/정책 관리
- memory-bank 폴더에 진행상황, 컨텍스트, 정책, 이슈 등 기록
- 코드/정책/운영 싱크 유지, 변경 이력 명확히 관리
- memory-bank는 프로젝트의 모든 의사결정, 기술 패턴, 진행상황, 이슈를 체계적으로 관리하는 핵심 문서 저장소임

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