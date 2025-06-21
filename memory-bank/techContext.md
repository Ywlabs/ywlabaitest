# 기술 컨텍스트

## 2024-06-21 오늘 추가된 기술 적용

### 🚀 **배포 시스템 기술**
- **Docker Compose**: 컨테이너 오케스트레이션, 볼륨 마운트, 환경 변수 관리
- **배포 스크립트**: Windows Batch 스크립트 기반 자동화 배포
- **볼륨 마운트**: `/home/ywlabs04/apps_log/enermind/flask/:/app/backend/logs/` 로그 디렉토리 외부 접근
- **환경 변수 자동화**: `.env` 파일 자동 생성 및 배포 스크립트 통합

### 🔧 **로깅 시스템 기술**
- **RotatingFileHandler**: 로그 파일 크기 제한(10MB) 및 백업 관리(5개)
- **다중 핸들러**: 파일 핸들러(app.log, error.log) + 콘솔 핸들러 동시 사용
- **Werkzeug 로거 통합**: Flask 내부 로그도 동일한 핸들러 사용
- **핸들러 중복 방지**: 기존 핸들러 제거 후 새 핸들러 추가 로직

### 🐛 **Flask 애플리케이션 기술**
- **Factory Pattern**: `create_app()` 함수 기반 애플리케이션 생성
- **단일 앱 생성**: Flask 앱을 한 번만 생성하여 중복 방지
- **CORS 설정 통합**: 모든 CORS 설정을 한 곳에서 관리
- **스케줄러 관리**: 환경 스케줄러는 앱 전체 생명주기 동안 실행

## 2024-06 최신 기술 적용 및 참고사항

- **인증 시스템:**
  - JWT 기반 토큰 인증, bcrypt 비밀번호 해싱, 사용자별 권한 관리
  - 프론트엔드에서 권한별 UI/기능 제어, 토큰 갱신 및 보안 관리
- **API 표준화:**
  - 모든 백엔드 API `{ success, code, message, data, error }` 구조로 통일, 프론트엔드 전체 일괄 적용.
- **공통 컴포넌트:**
  - CommonToast, CommonError, CommonLoading 등 공통 UI 컴포넌트 도입 및 전체 적용.
- **타입스크립트/IDE 환경:**
  - env.d.ts, axios.d.ts 등 타입 선언 파일로 .vue, axios import 타입 경고 해결.
  - .vscode, node_modules/.cache 등 캐시 삭제로 IDE 타입 경고 해결.
- **경로 alias:**
  - @/common, @/components, @/widgets 등 tsconfig.json의 paths 설정 활용.
- **불필요 API 및 코드 정리:**
  - /api/routes 등 미사용 API 및 관련 코드 완전 삭제.

## 기술 스택
### 프론트엔드
- Vue 3
- Vite
- Pinia
- Element Plus
- Lottie-web
- localStorage
- marked: Markdown 파서
- dompurify: HTML Sanitizer

### 백엔드
- Python 3.8+
- Flask 2.0+
- Flask-Cors
- Flask-SQLAlchemy
- SQLAlchemy
- python-dotenv
- LangChain
- langchain-openai
- langchain-community
- ChromaDB
- OpenAI API
- sentence-transformers
- numpy
- mysqlclient
- PyMySQL
- httpx
- PyJWT: JWT 토큰 생성/검증
- bcrypt: 비밀번호 해싱

### 데이터베이스
- MySQL
- ChromaDB (for RAG)

## 개발 환경 설정
### 사전 요구사항
- Python 3.8 이상
- Node.js 16 이상
- MySQL 서버 (로컬 또는 원격)
- OpenAI API Key

### 설치 단계
1. 백엔드:
   - Python 가상환경 생성 및 활성화
   - `pip install -r requirements.txt`
   - `.env` 파일에 DB, OpenAI, JWT 등 환경 변수 설정
2. 프론트엔드:
   - `npm install`
   - `.env` 파일에 API URL 등 환경 변수 설정
3. DB 초기화 및 서버 실행

## 의존성
### 프로덕션 의존성
- 프론트엔드: vue, vue-router, pinia, element-plus, axios, @vueuse/core, lottie-web, marked, dompurify
- 백엔드: Flask, Flask-Cors, Flask-SQLAlchemy, SQLAlchemy, openai, mysqlclient, PyMySQL, sentence-transformers, numpy, langchain, langchain-openai, langchain-community, chromadb, PyJWT, bcrypt

### 개발 의존성
- 프론트엔드: typescript, @vitejs/plugin-vue, vue-tsc, @types/node, vite, path
- 백엔드: pytest, black, flake8, python-dotenv

## 기술적 제약사항
- 프론트엔드: HMR/동적 import 관련 Vite 환경 이슈(해결). `dompurify`를 통해 XSS 공격 방지 필수.
- 위젯별 실데이터 연동은 추후 확장
- 백엔드는 Python 3.8+ 및 MySQL 환경 필요
- OpenAI API Key 필수
- 프론트엔드는 Vue 3 및 Vite 기반, Node 16+ 필요
- 환경 변수 미설정 시 일부 기능 동작 불가
- JWT 토큰 만료 시 자동 갱신 로직 필요

## 환경 변수

### 백엔드 (.env 예시)
```
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret_key
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=ywlabs
MYSQL_PORT=3306
OPENAI_API_KEY=your_openai_api_key
FLASK_DEBUG=True
```

### 프론트엔드 (.env 예시)
```
VITE_API_BASE_URL=http://localhost:5000
```

## 참고사항
- 기술 스택, 환경 변수, 의존성 변경 시 이 문서를 반드시 업데이트하세요.
- 버전별 요구사항을 명확히 문서화하세요
- JWT 토큰 보안 및 만료 관리에 주의하세요 