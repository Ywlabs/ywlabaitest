@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo 🚀 YWLab Quick Deploy (Fast Mode)
echo ========================================

:: 환경 변수 설정
set SERVER_HOST=192.168.0.94
set SERVER_USER=ywlabs04
set SERVER_PATH=/home/ywlabs04/apps/enermind

echo 📋 Deployment Info:
echo    Server: %SERVER_USER%@%SERVER_HOST%
echo    Path: %SERVER_PATH%
echo ========================================

:: 프론트엔드 빌드 (기본값: 빌드)
echo 📦 [1/3] Frontend build...
cd ..\..\frontend
echo    🔨 npm run build:prod running...
call npm run build:prod
if errorlevel 1 (
    echo ❌ Frontend build failed
    exit /b 1
)
echo    ✅ Frontend build completed
cd ..\apply\apply_prod

:: 파일 압축 및 전송
echo 📦 [2/3] Compressing and transferring...
if exist "temp_quick" rmdir /s /q "temp_quick"
mkdir "temp_quick"
mkdir "temp_quick\backend"
mkdir "temp_quick\frontend"

:: 파일 복사
echo    📁 Copying files...
xcopy /E /I /Y "..\..\backend\*" "temp_quick\backend\"
xcopy /E /I /Y "..\..\frontend\dist\*" "temp_quick\frontend\dist\"
copy "docker-compose.yml" "temp_quick\"
copy "Dockerfile" "temp_quick\"

:: .env 파일 생성 (.env로 복사)
if exist ".env" (
    echo    📁 Copying .env file...
    copy ".env" "temp_quick\.env"
) else (
    echo    ⚠️  .env not found, creating basic .env...
    echo APP_PROFILE=prod > "temp_quick\.env"
    echo OPENAI_API_KEY=your-openai-api-key-here >> "temp_quick\.env"
    echo LOG_LEVEL=INFO >> "temp_quick\.env"
)

:: 압축 및 전송
if exist "quick-deploy.tar.gz" del "quick-deploy.tar.gz"
cd temp_quick
tar -czf ..\quick-deploy.tar.gz *
cd ..

scp -i %USERPROFILE%\.ssh\id_rsa_ywlab quick-deploy.tar.gz %SERVER_USER%@%SERVER_HOST%:%SERVER_PATH%
if errorlevel 1 (
    echo ❌ File transfer failed
    exit /b 1
)

:: 서버에서 압축 해제 및 컨테이너 재시작
echo    📦 Extracting and restarting...
ssh -i %USERPROFILE%\.ssh\id_rsa_ywlab %SERVER_USER%@%SERVER_HOST% "cd %SERVER_PATH% && tar -xzf quick-deploy.tar.gz && rm quick-deploy.tar.gz && mkdir -p /home/ywlabs04/apps_log/enermind/flask/ && chmod 755 /home/ywlabs04/apps_log/enermind/flask/ && docker compose up -d"

if errorlevel 1 (
    echo ❌ Server deployment failed
    exit /b 1
)

:: 임시 파일 정리
rmdir /s /q "temp_quick"
del "quick-deploy.tar.gz"

echo ✅ [3/3] Deployment completed!
echo ========================================
echo 🌐 Access URLs:
echo    - External: http://enermind.ywlabs.com
echo    - IP Access: http://192.168.0.94:8085
echo 📋 Log access:
echo    - Server logs: tail -f /home/ywlabs04/apps_log/enermind/flask/*.log
echo    - Container logs: docker logs -f ywlab-app
echo ========================================
pause 