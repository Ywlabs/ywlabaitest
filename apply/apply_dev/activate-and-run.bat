@echo off
echo ================================================
echo YWLab 자동 가상환경 활성화 및 개발 서버
echo ================================================

REM 가상환경 경로 확인
if exist "venv\Scripts\activate.bat" (
    echo ✅ 가상환경 발견: venv
    echo 🔄 가상환경 활성화 중...
    call venv\Scripts\activate.bat
) else (
    echo ❌ 가상환경이 없습니다.
    echo 📦 새 가상환경을 생성합니다...
    python -m venv venv
    echo 🔄 가상환경 활성화 중...
    call venv\Scripts\activate.bat
    echo 📥 Python 패키지 설치 중...
    pip install -r backend\requirements.txt
)

echo ✅ 가상환경 활성화 완료!
echo 📦 Frontend 패키지 설치 중...
cd frontend && npm install && cd ..

echo 🚀 개발 서버 시작...
python dev-server.py

pause 