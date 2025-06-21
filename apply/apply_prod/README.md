# 🚀 YWLab 상용 서버 배포

이 폴더는 YWLab 애플리케이션의 상용 서버 배포를 위한 파일들을 포함합니다.

## 📁 파일 구조

```
apply/apply_prod/
├── docker-compose.yml    # Docker Compose 설정
├── Dockerfile           # Docker 이미지 빌드
├── deploy.sh            # 서버 배포 스크립트 (Linux)
├── deploy.bat           # 로컬 배포 스크립트 (Windows)
├── deploy-quick.bat     # 빠른 배포 스크립트 (Windows)
└── README.md            # 이 파일
```

## 🔧 환경 설정

### 필수 파일
- **`.env`**: 백엔드 환경변수 파일 (로컬에서 생성 필요)
- **`frontend/dist/`**: 프론트엔드 빌드 결과

### .env 파일 생성
배포 전에 로컬에서 `.env` 파일을 생성하고 실제 값으로 설정해야 합니다:

```bash
# apply/apply_prod 폴더에서 .env 파일 생성
cd apply/apply_prod

# .env 파일 예시
APP_PROFILE=prod
SECRET_KEY=your-secret-key-here
DEBUG=False

# DB 정보
DB_HOST=your-db-host-here
DB_USER=your-db-user-here
DB_PASSWORD=your-db-password-here
DB_NAME=your-db-name-here
DB_PORT=3306

# OpenAI API Key
OPENAI_API_KEY=your-openai-api-key-here

# JWT 인증 설정
JWT_SECRET=your-jwt-secret-key
JWT_EXPIRE_MINUTES=60

# ChromaDB 설정
RAG_CHROMA_DIR=./chromadb/rag_db

# 로그 설정
LOG_LEVEL=INFO
LOG_DIR=/app/backend/logs

# 파일 업로드 설정
UPLOAD_FOLDER=./uploads
MAX_CONTENT_LENGTH=16777216

# CORS 설정
CORS_ORIGINS=http://localhost:3000,http://localhost:5000
```

## 🚀 배포 방법

### 방법 1: Windows에서 자동 배포 (권장)

1. **환경 설정**
   ```bash
   # deploy.bat 파일에서 서버 정보 수정
   set SERVER_HOST=your-server-ip
   set SERVER_USER=your-username
   set SERVER_PATH=/home/your-username/apps/enermind
   ```

2. **.env 파일 준비**
   ```bash
   # apply/apply_prod 폴더에 .env 파일 생성
   # 실제 API 키, DB 정보 등 입력
   ```

3. **배포 실행**
   ```bash
   # Windows에서 실행
   apply\apply_prod\deploy.bat
   ```

### 방법 2: 빠른 배포 (증분 업데이트)

```bash
# Windows에서 실행 (로컬 .env 파일 필요)
apply\apply_prod\deploy-quick.bat
```

### 방법 3: 수동 배포

1. **로컬에서 빌드**
   ```bash
   # 프론트엔드 빌드
   cd frontend
   npm install
   npm run build:prod
   cd ..
   ```

2. **서버로 파일 전송**
   ```bash
   # apply/apply_prod 폴더 전송 (.env 포함)
   scp -r apply/apply_prod user@server:/home/user/apply/
   
   # 백엔드 소스 전송
   scp -r backend user@server:/home/user/apply/apply_prod/
   
   # 프론트엔드 빌드 결과 전송
   scp -r frontend/dist user@server:/home/user/apply/apply_prod/frontend/dist
   ```

3. **서버에서 배포**
   ```bash
   # 서버에 SSH 접속
   ssh user@server
   
   # 배포 실행
   cd /home/user/apply/apply_prod
   chmod +x deploy.sh
   ./deploy.sh
   ```

## 🐳 Docker 명령어

### 컨테이너 관리
```bash
# 컨테이너 상태 확인
docker compose ps

# 컨테이너 시작
docker compose up -d

# 컨테이너 중지
docker compose down

# 컨테이너 재시작
docker compose restart app

# 컨테이너 완전 재시작
docker compose down
docker compose up -d
```

### 이미지 관리
```bash
# 이미지 빌드 (캐시 없이)
docker compose build --no-cache

# 이미지 빌드 후 시작
docker compose build --no-cache && docker compose up -d

# 이미지 확인
docker images | grep ywlab
```

### 로그 관리
```bash
# 실시간 로그 모니터링
docker compose logs -f app

# 최근 로그 확인
docker compose logs --tail=100 app

# 특정 시간 이후 로그
docker compose logs --since="2024-06-21T10:00:00" app

# 로그 파일로 저장
docker compose logs app > app.log
```

### 컨테이너 내부 접속
```bash
# 컨테이너 내부 접속
docker exec -it ywlab-app bash

# 컨테이너 내부 파일 확인
docker exec -it ywlab-app ls -la /app/
docker exec -it ywlab-app ls -la /app/frontend/dist/

# 컨테이너 내부에서 명령어 실행
docker exec -it ywlab-app curl http://127.0.0.1:5000/api/health
```

### 시스템 정보
```bash
# Docker 시스템 정보
docker system df
docker system prune -f

# 컨테이너 리소스 사용량
docker stats ywlab-app

# 네트워크 확인
docker network ls
docker network inspect apply_prod_ywlab-network
```

## 🌐 서버 실행 및 접속

### 서버 시작
```bash
# 서버에서 실행
cd /home/ywlabs04/apps/enermind
docker compose up -d

# 또는 배포 스크립트 사용
./deploy.sh
```

### 접속 URL
- **외부 접속**: `http://enermind.ywlabs.com`
- **IP 접속**: `http://192.168.0.94:8085`
- **내부 접속**: `http://127.0.0.1:8085`

### 헬스체크
```bash
# 헬스체크 API 호출
curl http://192.168.0.94:8085/api/health

# 응답 예시
{
  "status": "healthy",
  "timestamp": 1734567890.123,
  "service": "ywlab-backend",
  "version": "1.0.0"
}
```

## 📊 모니터링

### 애플리케이션 로그
```bash
# 실시간 로그 모니터링
tail -f /home/ywlabs04/apps_log/enermind/flask/app.log

# 에러 로그 확인
tail -f /home/ywlabs04/apps_log/enermind/flask/error.log

# 최근 로그 확인
tail -20 /home/ywlabs04/apps_log/enermind/flask/app.log
```

### 시스템 모니터링
```bash
# 포트 사용 확인
sudo netstat -tlnp | grep :8085

# 프로세스 확인
ps aux | grep python
ps aux | grep nginx

# 디스크 사용량
df -h
du -sh /home/ywlabs04/apps_log/enermind/flask/
```

## 🔄 Nginx 관리

### Nginx 재시작
```bash
# 설정 파일 문법 검사
sudo nginx -t

# 재시작
sudo systemctl restart nginx

# 상태 확인
sudo systemctl status nginx
```

### Nginx 로그
```bash
# 에러 로그 확인
sudo tail -f /var/log/nginx/error.log

# 접근 로그 확인
sudo tail -f /var/log/nginx/access.log

# YWLab 전용 로그
tail -f /home/ywlabs04/apps_log/enermind_access.log
tail -f /home/ywlabs04/apps_log/enermind_error.log
```

## 🛠️ 문제 해결

### 환경변수 문제
```bash
# .env 파일 확인
cat /home/ywlabs04/apps/enermind/.env

# 컨테이너 환경변수 확인
docker exec -it ywlab-app env | grep -E "(OPENAI|DB_)"

# 환경변수 재설정 후 컨테이너 재시작
docker compose down
docker compose up -d
```

### 포트 충돌
```bash
# 포트 사용 확인
sudo netstat -tlnp | grep :8085

# 다른 포트 사용 (docker-compose.yml 수정)
ports:
  - "8086:5000"
```

### 컨테이너 문제
```bash
# 컨테이너 재시작
docker compose restart app

# 완전 재시작
docker compose down
docker compose up -d

# 이미지 재빌드
docker compose build --no-cache
docker compose up -d
```

### 로그 문제
```bash
# 로그 디렉토리 권한 확인
ls -la /home/ywlabs04/apps_log/enermind/flask/

# 로그 디렉토리 생성
mkdir -p /home/ywlabs04/apps_log/enermind/flask/

# 권한 수정
chmod 755 /home/ywlabs04/apps_log/enermind/flask/
```

### 네트워크 문제
```bash
# 방화벽 확인
sudo ufw status

# 포트 열기
sudo ufw allow 8085

# Docker 네트워크 확인
docker network ls
docker network inspect apply_prod_ywlab-network
```

## 📞 지원

- **배포 이슈**: 로그 확인 후 담당자 연락
- **환경 설정**: `.env` 파일 점검
- **네트워크**: 방화벽 및 포트 설정 확인
- **Docker**: 컨테이너 상태 및 로그 확인
- **Nginx**: 설정 파일 및 로그 확인 