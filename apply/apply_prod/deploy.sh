#!/bin/bash

# YWLab 상용 배포 스크립트
# 서버에서 실행

set -e  # 오류 발생 시 스크립트 중단

echo "🚀 YWLab 상용 배포 시작..."

# 현재 디렉토리 확인
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 환경변수 파일 확인 및 복사
echo "📁 환경변수 파일 확인..."
if [ -f "env.example" ] && [ ! -f ".env" ]; then
    echo "📋 env.example을 .env로 복사..."
    cp env.example .env
    echo "⚠️  .env 파일이 생성되었습니다!"
    echo "⚠️  실제 API 키와 설정값으로 수정 후 배포를 진행해주세요!"
    echo "📝 수정 방법: nano .env"
    echo "📝 수정 후 다시 배포 스크립트를 실행해주세요!"
    exit 1  # 수정 후 다시 실행하도록 중단
elif [ -f ".env" ]; then
    echo "✅ .env 파일 존재"
else
    echo "❌ env.example 파일이 없습니다!"
    exit 1
fi

# 로그 및 업로드 디렉토리 생성
echo "📁 필요한 디렉토리 생성..."
mkdir -p logs uploads

# 기존 컨테이너 정리
echo "🧹 기존 컨테이너 정리..."
docker compose down --remove-orphans 2>/dev/null || true

# Docker 이미지 빌드
echo "🔨 Docker 이미지 빌드 중..."
docker compose build --no-cache

# 컨테이너 시작
echo "🚀 컨테이너 시작..."
docker compose up -d

# 컨테이너 상태 확인
echo "📊 컨테이너 상태 확인..."
docker compose ps

# 로그 확인으로 구동 완료 판단
echo "📋 애플리케이션 로그 확인 중..."
echo "⏳ Flask 서버 시작 대기 중... (최대 60초)"

# 60초 동안 로그에서 "Flask 서버 시작" 메시지 대기
for i in {1..60}; do
    if docker compose logs app | grep -q "Flask 서버 시작"; then
        echo "✅ Flask 서버가 정상적으로 시작되었습니다!"
        break
    fi
    
    if [ $i -eq 60 ]; then
        echo "⚠️  Flask 서버 시작 메시지를 찾을 수 없습니다."
        echo "📋 최근 로그 확인:"
        docker compose logs --tail=20 app
        echo "✅ 배포는 완료되었지만, 로그 확인이 필요합니다."
    fi
    
    sleep 1
done

echo "✅ 배포 성공! 애플리케이션이 시작되었습니다."
echo "🌐 접속 URL:"
echo "   - 외부 접속: http://enermind.ywlabs.com"
echo "   - IP 접속: http://192.168.0.94:8085"
echo "   - 내부 접속: http://127.0.0.1:8085"
echo "📋 로그 확인: tail -f /home/ywlabs04/apps_log/enermind/flask/app.log"
echo "🎉 배포 완료!" 