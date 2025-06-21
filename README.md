# YWLab AI Test Platform

YWLab의 AI 테스트 플랫폼으로, Frontend(Vue.js)와 Backend(Flask)가 통합된 웹 애플리케이션입니다.

## 📋 목차

- [프로젝트 구조](#프로젝트-구조)
- [기술 스택](#기술-스택)
- [개발 환경 설정](#개발-환경-설정)
- [로컬 개발 서버 실행](#로컬-개발-서버-실행)
- [배포 방법](#배포-방법)
- [API 문서](#api-문서)
- [기여 가이드](#기여-가이드)

## 🏗️ 프로젝트 구조

```
workspace-ywlabaitest/
├── backend/                    # Flask 백엔드
│   ├── app.py                 # 메인 애플리케이션
│   ├── config.py              # 환경별 설정
│   ├── requirements.txt       # Python 의존성
│   ├── core/                  # 핵심 모듈
│   │   ├── handlers/          # 인텐트별 핸들러
│   │   ├── embeddings/        # 임베딩 관련
│   │   ├── utils/             # 유틸리티
│   │   └── parsers/           # 문서 파서
│   ├── services/              # 비즈니스 로직
│   ├── routes/                # API 라우트
│   ├── metadata/              # 정책 문서 등
│   └── chromadb/              # 벡터 데이터베이스
├── frontend/                   # Vue.js 프론트엔드
│   ├── src/
│   │   ├── components/        # Vue 컴포넌트
│   │   ├── views/             # 페이지 뷰
│   │   ├── router/            # 라우터 설정
│   │   └── common/            # 공통 모듈
│   ├── package.json           # Node.js 의존성
│   └── vite.config.js         # Vite 설정
├── auto-dev.py                # 자동 개발 환경 설정
├── dev-server.py              # 통합 개발 서버
├── activate-and-run.bat       # Windows 자동 실행
└── package.json               # 프로젝트 설정
```

## 🛠️ 기술 스택

### Backend
- **Python 3.11+**
- **Flask** - 웹 프레임워크
- **ChromaDB** - 벡터 데이터베이스
- **MariaDB** - 관계형 데이터베이스
- **OpenAI API** - AI 모델
- **HuggingFace** - 임베딩 모델

### Frontend
- **Vue.js 3** - 프론트엔드 프레임워크
- **Vite** - 빌드 도구
- **Element Plus** - UI 컴포넌트
- **Vue Router** - 라우팅
- **Axios** - HTTP 클라이언트

### DevOps
- **Docker** - 컨테이너화
- **GitHub Actions** - CI/CD
- **Nginx** - 리버스 프록시

## 🚀 개발 환경 설정

### 1. 사전 요구사항

- **Python 3.11+**
- **Node.js 18+**
- **npm** 또는 **yarn**
- **Git**

### 2. 프로젝트 클론

```bash
git clone https://github.com/your-username/ywlab-ai-test.git
cd ywlab-ai-test
```

### 3. 자동 환경 설정 (권장)

#### Windows
```bash
# 배치 파일 실행
activate-and-run.bat
```

#### 모든 OS
```bash
# npm 스크립트 실행
npm run auto

# 또는 Python 스크립트 직접 실행
python auto-dev.py
```

### 4. 수동 환경 설정

#### 4.1 Python 가상환경 설정
```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Python 의존성 설치
cd backend
pip install -r requirements.txt
cd ..
```

#### 4.2 Frontend 의존성 설치
```bash
cd frontend
npm install
cd ..
```

#### 4.3 환경변수 설정
```bash
# backend/.env 파일 생성 (예시)
cp backend/env.example backend/.env

# 환경변수 편집
DATABASE_URL=mysql://username:password@host:port/database
OPENAI_API_KEY=your_openai_api_key
SECRET_KEY=your_secret_key_here

# 로그 설정
LOG_LEVEL=INFO
LOG_DIR=./logs

# 파일 업로드 설정
UPLOAD_FOLDER=./uploads
MAX_CONTENT_LENGTH=16777216
```

## 🖥️ 로컬 개발 서버 실행

### 1. 자동 실행 (권장)

```bash
# 모든 것을 자동으로 처리
npm run auto
```

### 2. 수동 실행

```bash
# 1. 가상환경 활성화
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 2. Frontend 빌드
cd frontend && npm run build && cd ..

# 3. 개발 서버 시작
python dev-server.py
```

### 3. 접속 확인

- **메인 페이지**: http://localhost:5000
- **API 헬스체크**: http://localhost:5000/health
- **로그인**: http://localhost:5000/login

## 🚀 배포

### 개발 환경

#### 1. 자동 환경 설정 + 개발 서버
```bash
# 프로젝트 루트에서 실행
npm run auto

# 또는 직접 실행
python deploy/dev-server/auto-dev.py
```

#### 2. 수동 개발 서버 실행
```bash
# 프로젝트 루트에서 실행
npm run dev

# 또는 직접 실행
python deploy/dev-server/dev-server.py
```

#### 3. Windows 배치 파일 사용
```bash
# 개발 서버 실행
deploy/dev-server/dev.bat

# 가상환경 활성화 + 개발 서버 실행
deploy/dev-server/activate-and-run.bat
```

### 상용 환경 (Docker)

#### 1. Docker 이미지 빌드
```bash
# 프로젝트 루트에서
cd deploy/docker-prod
docker build -t ywlab-app:latest ../..
```

#### 2. Docker Compose 실행
```bash
# 개발 환경
cd deploy/docker-prod
docker-compose -f docker-compose.dev.yml up -d

# 상용 환경
cd deploy/docker-prod
docker-compose -f docker-compose.prod.yml up -d
```

#### 3. 배포 스크립트 사용
```bash
# 개발 환경 배포
npm run deploy:dev

# 상용 환경 배포
npm run deploy:prod
```

### 3. GitHub Actions 자동 배포

#### 3.1 GitHub Secrets 설정
GitHub 저장소의 Settings → Secrets and variables → Actions에서 다음 설정:

**개발 환경:**
```
DEV_HOST=your_dev_server_ip
DEV_USERNAME=your_ssh_username
DEV_SSH_KEY=your_private_ssh_key
DEV_SECRET_KEY=your_dev_secret_key
DEV_JWT_SECRET=your_dev_jwt_secret
DEV_DB_HOST=your_dev_db_host
DEV_DB_USER=your_dev_db_user
DEV_DB_PASSWORD=your_dev_db_password
DEV_DB_NAME=your_dev_db_name
DEV_DB_PORT=your_dev_db_port
DEV_OPENAI_API_KEY=your_dev_openai_api_key
```

**상용 환경:**
```
PROD_HOST=your_prod_server_ip
PROD_USERNAME=your_ssh_username
PROD_SSH_KEY=your_private_ssh_key
PROD_SECRET_KEY=your_prod_secret_key
PROD_JWT_SECRET=your_prod_jwt_secret
PROD_DB_HOST=your_prod_db_host
PROD_DB_USER=your_prod_db_user
PROD_DB_PASSWORD=your_prod_db_password
PROD_DB_NAME=your_prod_db_name
PROD_DB_PORT=your_prod_db_port
PROD_OPENAI_API_KEY=your_prod_openai_api_key
```

#### 3.2 자동 배포 트리거
- `develop` 브랜치에 push → 개발 서버 자동 배포
- `main` 브랜치에 push → 상용 서버 자동 배포
- 매주 월요일 새벽 2시 → 자동 배포

### 4. 수동 배포

#### 4.1 상용 서버 설정
```bash
# 서버에 접속
ssh user@your-server.com

# 배포 디렉토리 생성
mkdir -p /opt/production
cd /opt/production

# 환경변수 파일 생성
cat > backend/.env.prod << EOF
APP_PROFILE=prod
FLASK_ENV=production
FLASK_APP=app.py
SECRET_KEY=your_production_secret_key
JWT_SECRET=your_production_jwt_secret
JWT_EXPIRE_MINUTES=60
DB_HOST=your_db_host
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=your_db_name
DB_PORT=your_db_port
OPENAI_API_KEY=your_openai_api_key
RAG_CHROMA_DIR=./chromadb/rag_db
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log
DEBUG=False
EOF
```

#### 4.2 배포 실행
```bash
# 최신 이미지 pull
docker pull ghcr.io/your-repo/ywlab-app:latest

# 컨테이너 교체
cd deploy/docker-prod
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d

# 헬스체크
curl -f http://localhost:5000/health
```

### 5. Nginx 설정

```nginx
# /etc/nginx/sites-available/production
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 📚 API 문서

### 인증 API
- `POST /api/auth/login` - 로그인
- `POST /api/auth/logout` - 로그아웃
- `POST /api/auth/refresh` - 토큰 갱신

### 채팅 API
- `POST /api/chat` - AI 채팅
- `GET /api/chat/history` - 채팅 기록

### 직원 정보 API
- `GET /api/employee/info` - 직원 정보 조회
- `PUT /api/employee/info` - 직원 정보 수정

### 매출 정보 API
- `GET /api/sales/status` - 매출 현황
- `GET /api/sales/trend` - 매출 트렌드

### 위젯 API
- `GET /api/widgets` - 위젯 목록
- `POST /api/widgets` - 위젯 생성

## 🔧 개발 가이드

### 1. 코드 스타일

#### Python
- **PEP 8** 준수
- **한글 주석** 사용
- **타입 힌트** 사용

#### JavaScript/Vue
- **ESLint** 규칙 준수
- **Vue 3 Composition API** 사용
- **한글 주석** 사용

### 2. 브랜치 전략

```
main          # 상용 배포
├── develop   # 개발/스테이징
├── feature/* # 기능 개발
└── hotfix/*  # 긴급 수정
```

### 3. 커밋 메시지 규칙

```
feat: 새로운 기능 추가
fix: 버그 수정
docs: 문서 수정
style: 코드 스타일 변경
refactor: 코드 리팩토링
test: 테스트 추가/수정
chore: 빌드 프로세스 변경
```

## 🐛 문제 해결

### 1. 일반적인 문제

#### ChromaDB 컬렉션 오류
```bash
# ChromaDB 디렉토리 초기화
rm -rf backend/chromadb
python dev-server.py
```

#### Frontend 빌드 오류
```bash
# node_modules 재설치
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

#### Python 패키지 오류
```bash
# 가상환경 재설정
rm -rf venv
python -m venv venv
venv\Scripts\activate
pip install -r backend/requirements.txt
```

### 2. 로그 확인

```bash
# Flask 로그
tail -f backend/logs/app.log

# Docker 로그
docker-compose logs -f app

# Nginx 로그
tail -f /var/log/nginx/access.log
```

## 📞 지원

- **이슈 리포트**: [GitHub Issues](https://github.com/your-username/ywlab-ai-test/issues)
- **문서**: [Wiki](https://github.com/your-username/ywlab-ai-test/wiki)
- **이메일**: support@ywlab.com

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 👥 기여자

- **개발팀** - 초기 개발
- **AI팀** - AI 모델 통합
- **DevOps팀** - 배포 자동화

---

**YWLab AI Test Platform** - AI 기술을 활용한 스마트한 업무 환경을 제공합니다.