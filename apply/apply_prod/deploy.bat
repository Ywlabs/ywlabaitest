@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo 🚀 YWLab 로컬 빌드 및 서버 배포 시작...
echo ========================================

:: 환경 변수 설정 (필요시 수정)
set SERVER_HOST=192.168.0.94
set SERVER_USER=ywlabs04
set SERVER_PATH=/home/ywlabs04/apps/enermind

echo 📋 배포 정보:
echo    서버: %SERVER_USER%@%SERVER_HOST%
echo    경로: %SERVER_PATH%
echo ========================================

:: 프론트엔드 빌드
echo 📦 [1/6] 프론트엔드 빌드 시작...
echo    📁 프론트엔드 디렉토리로 이동...
cd ..\..\frontend
echo    📦 npm install 실행 중...
call npm install
if errorlevel 1 (
    echo ❌ [1/6] npm install 실패
    exit /b 1
)
echo    ✅ npm install 완료

echo    🔨 npm run build:prod 실행 중...
call npm run build:prod
if errorlevel 1 (
    echo ❌ [1/6] 프론트엔드 빌드 실패
    exit /b 1
)
echo    ✅ 프론트엔드 빌드 완료
cd ..\apply\apply_prod
echo ✅ [1/6] 프론트엔드 빌드 완료
echo ========================================

:: 백엔드 준비
echo 🔧 [2/6] 백엔드 환경 설정...
if not exist ".env" (
    echo    ❌ .env 파일이 없습니다!
    echo    ⚠️  배포 전에 .env 파일을 생성하고 실제 API 키와 설정값을 입력해주세요.
    echo    📝 필요한 항목:
    echo       - OPENAI_API_KEY: OpenAI API 키
    echo       - DB_HOST, DB_USER, DB_PASSWORD, DB_NAME: 데이터베이스 정보
    echo       - SECRET_KEY, JWT_SECRET: 보안 키
    pause
    exit /b 1
) else (
    echo    ✅ .env 파일 존재
)
echo ✅ [2/6] 백엔드 환경 설정 완료
echo ========================================

:: 서버에 대상 폴더 생성
echo 📁 [3/6] 서버 폴더 생성 중...
echo    🔗 서버 연결 확인 중...
ssh -o ConnectTimeout=5 -o ServerAliveInterval=3 -o ServerAliveCountMax=2 -i %USERPROFILE%\.ssh\id_rsa_ywlab %SERVER_USER%@%SERVER_HOST% "echo '연결 성공'" >nul 2>&1
if errorlevel 1 (
    echo ❌ [3/6] 서버 연결 실패
    exit /b 1
)
echo    ✅ 서버 연결 성공

echo    📁 메인 폴더 확인 중...
ssh -o ConnectTimeout=5 -o ServerAliveInterval=3 -o ServerAliveCountMax=2 -i %USERPROFILE%\.ssh\id_rsa_ywlab %SERVER_USER%@%SERVER_HOST% "mkdir -p %SERVER_PATH% 2>/dev/null || true" >nul 2>&1
echo    ✅ 메인 폴더 준비 완료

echo ✅ [3/6] 서버 폴더 생성 완료
echo ========================================

:: 서버로 파일 전송
echo 📤 [4/6] 서버로 파일 전송 중...
echo    📦 배포 파일 압축 중...

:: 임시 배포 폴더 생성
if exist "temp_deploy" rmdir /s /q "temp_deploy"
mkdir "temp_deploy"
mkdir "temp_deploy\apply_prod"
mkdir "temp_deploy\backend"
mkdir "temp_deploy\frontend"

:: 파일 복사
echo    📁 파일 복사 중...
xcopy /E /I /Y "apply_prod\*" "temp_deploy\apply_prod\"
xcopy /E /I /Y "..\..\backend\*" "temp_deploy\backend\"
xcopy /E /I /Y "..\..\frontend\*" "temp_deploy\frontend\"

:: Dockerfile 경로 수정
echo    🔧 핵심 파일들을 루트로 복사 중...
copy "Dockerfile" "temp_deploy\Dockerfile"
copy "docker-compose.yml" "temp_deploy\docker-compose.yml"
copy "deploy.sh" "temp_deploy\deploy.sh"
copy ".env" "temp_deploy\.env"

:: 복사 확인
echo    ✅ 복사된 파일 확인:
dir "temp_deploy\deploy.sh" >nul 2>&1 && echo       ✅ deploy.sh 복사됨 || echo       ❌ deploy.sh 복사 실패
dir "temp_deploy\Dockerfile" >nul 2>&1 && echo       ✅ Dockerfile 복사됨 || echo       ❌ Dockerfile 복사 실패
dir "temp_deploy\frontend\package.json" >nul 2>&1 && echo       ✅ frontend/package.json 복사됨 || echo       ❌ frontend/package.json 복사 실패

:: TAR 압축 (Windows 10 이상에서 tar 명령어 사용)
echo    🔨 TAR 압축 중...
echo    📊 압축할 파일 크기 확인 중...
dir /s "temp_deploy" | find "File(s)" >nul 2>&1 && echo       파일 개수 확인됨 || echo       파일 개수 확인 실패

:: 기존 압축 파일 삭제
if exist "deploy.tar.gz" (
    echo    🗑️  기존 압축 파일 삭제 중...
    del "deploy.tar.gz"
)

cd temp_deploy
echo    📦 압축 시작 (진행률 표시 없음)...
tar -czf ..\deploy.tar.gz --exclude=node_modules --exclude=.git --exclude=*.log --exclude=*.tmp --exclude=*.cache *
cd ..

echo    ✅ TAR 압축 완료

:: 압축 파일 전송
echo    📤 압축 파일 전송 중...
scp -i %USERPROFILE%\.ssh\id_rsa_ywlab deploy.tar.gz %SERVER_USER%@%SERVER_HOST%:%SERVER_PATH%
if errorlevel 1 (
    echo ❌ [4/6] 압축 파일 전송 실패
    exit /b 1
)
echo    ✅ 압축 파일 전송 완료

:: 서버에서 압축 해제
echo    📦 서버에서 압축 해제 중...
ssh -i %USERPROFILE%\.ssh\id_rsa_ywlab %SERVER_USER%@%SERVER_HOST% "cd %SERVER_PATH% && tar -xzf deploy.tar.gz && rm deploy.tar.gz"
if errorlevel 1 (
    echo ❌ [4/6] 서버 압축 해제 실패
    exit /b 1
)
echo    ✅ 서버 압축 해제 완료

:: 임시 파일 정리
echo    🧹 임시 파일 정리 중...
rmdir /s /q "temp_deploy"
echo    ✅ 임시 파일 정리 완료

echo ✅ [4/6] 파일 전송 완료
echo ========================================

:: 서버에서 배포 실행
echo 🚀 [5/6] 서버에서 배포 실행 중...
echo    🔗 서버에 SSH 연결 중...
ssh -i %USERPROFILE%\.ssh\id_rsa_ywlab %SERVER_USER%@%SERVER_HOST% "cd %SERVER_PATH% && echo '=== 현재 디렉토리 내용 ===' && ls -la && echo '=== apply_prod 폴더 내용 ===' && ls -la apply_prod/ && if [ -f 'deploy.sh' ]; then echo '루트에서 deploy.sh 실행'; chmod +x deploy.sh && ./deploy.sh; elif [ -f 'apply_prod/deploy.sh' ]; then echo 'apply_prod에서 deploy.sh 실행'; chmod +x apply_prod/deploy.sh && cd apply_prod && ./deploy.sh; else echo 'deploy.sh 파일을 찾을 수 없습니다'; exit 1; fi"
if errorlevel 1 (
    echo ❌ [5/6] 서버 배포 실패
    exit /b 1
)
echo ✅ [5/6] 서버 배포 완료
echo ========================================

echo ✅ [6/6] 배포 완료!
echo 🌐 접속 URL:
echo    - 외부 접속: http://enermind.ywlabs.com
echo    - IP 접속: http://192.168.0.94:8085
echo    - 내부 접속: http://127.0.0.1:8085
echo ========================================
pause 