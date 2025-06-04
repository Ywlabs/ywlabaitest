# 기술 컨텍스트

## 기술 스택
### 프론트엔드
- Vue 3
- TypeScript
- Vite
- Pinia
- Vue Router
- Element Plus
- Axios
- @vueuse/core

### 백엔드
- Python 3.8+
- Flask 2.0+
- Flask-Cors
- Flask-SQLAlchemy
- SQLAlchemy
- python-dotenv
- OpenAI API
- sentence-transformers
- numpy
- mysqlclient
- PyMySQL
- httpx

### 데이터베이스
- MySQL

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
   - `.env` 파일에 DB, OpenAI 등 환경 변수 설정
2. 프론트엔드:
   - `npm install`
   - `.env` 파일에 API URL 등 환경 변수 설정
3. DB 초기화 및 서버 실행

## 의존성
### 프로덕션 의존성
- 프론트엔드: vue, vue-router, pinia, element-plus, axios, @vueuse/core
- 백엔드: Flask, Flask-Cors, Flask-SQLAlchemy, SQLAlchemy, openai, mysqlclient, PyMySQL, sentence-transformers, numpy

### 개발 의존성
- 프론트엔드: typescript, @vitejs/plugin-vue, vue-tsc, @types/node, vite, path
- 백엔드: pytest, black, flake8, python-dotenv

## 기술적 제약사항
- 백엔드는 Python 3.8+ 및 MySQL 환경 필요
- OpenAI API Key 필수
- 프론트엔드는 Vue 3 및 Vite 기반, Node 16+ 필요
- 환경 변수 미설정 시 일부 기능 동작 불가

## 환경 변수

### 백엔드 (.env 예시)
```
SECRET_KEY=your_secret_key
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
VITE_API_URL=http://localhost:5000
```

## 참고사항
- 기술 스택, 환경 변수, 의존성 변경 시 이 문서를 반드시 업데이트하세요.
- 버전별 요구사항을 명확히 문서화하세요 