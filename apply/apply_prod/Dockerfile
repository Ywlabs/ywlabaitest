# YWLab 통합 애플리케이션 Dockerfile
FROM node:18-alpine as frontend-build

WORKDIR /app/frontend

# 프론트엔드 의존성 설치
COPY frontend/package*.json ./
RUN npm install

# 프론트엔드 소스 복사 및 빌드
COPY frontend/ ./
ARG BUILD_MODE=prod
RUN npm run build:${BUILD_MODE}

# 빌드 결과 확인
RUN ls -la dist/

# Python 백엔드 빌드
FROM python:3.11-slim as backend-build

WORKDIR /app

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 설치
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 최종 이미지
FROM python:3.11-slim

WORKDIR /app

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 복사
COPY --from=backend-build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=backend-build /usr/local/bin /usr/local/bin

# 백엔드 소스 복사
COPY backend/ ./backend/

# 프론트엔드 빌드 결과를 올바른 경로에 복사
COPY --from=frontend-build /app/frontend/dist ./frontend/dist

# 복사 결과 확인
RUN ls -la frontend/dist/ || echo "frontend/dist 폴더가 없습니다"
RUN ls -la backend/ || echo "backend 폴더가 없습니다"

# 환경변수 설정
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app/backend

# 포트 노출
EXPOSE 8085

# 헬스체크
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://127.0.0.1:8085/api/health || exit 1

# 애플리케이션 시작
CMD ["python", "backend/app.py"] 