# 🛠️ 개발서버 빌드 배포

이 폴더는 로컬 개발 환경에서 사용하는 빌드 및 배포 스크립트들을 포함합니다.

## 📁 파일 구조

```
deploy/dev-server/
├── dev-server.py           # 통합 개발 서버 (프론트엔드 빌드 + 백엔드 실행)
├── dev-server-simple.py    # 간단한 개발 서버
├── auto-dev.py             # 자동 환경 설정 + 개발 서버
├── dev.bat                 # Windows용 개발 서버 실행 배치 파일
├── activate-and-run.bat    # 가상환경 활성화 + 개발 서버 실행
└── README.md               # 이 파일
```

## 🚀 사용 방법

### 1. 자동 환경 설정 + 개발 서버
```bash
# 프로젝트 루트에서 실행
python deploy/dev-server/auto-dev.py

# 또는 npm 스크립트 사용
npm run auto
```

### 2. 수동 개발 서버 실행
```bash
# 프로젝트 루트에서 실행
python deploy/dev-server/dev-server.py

# 또는 npm 스크립트 사용
npm run dev
```

### 3. Windows 배치 파일 사용
```bash
# 개발 서버 실행
deploy/dev-server/dev.bat

# 가상환경 활성화 + 개발 서버 실행
deploy/dev-server/activate-and-run.bat
```

### 4. 간단한 개발 서버
```bash
# 간단한 버전 (빌드 없이)
python deploy/dev-server/dev-server-simple.py
```

## 🔧 동작 방식

### auto-dev.py
1. **가상환경 확인/생성**
2. **의존성 설치** (Python + Node.js)
3. **프론트엔드 빌드** (`npm run build:dev`)
4. **백엔드 서버 시작** (Flask)

### dev-server.py
1. **프론트엔드 빌드 확인**
2. **빌드 파일 없으면 자동 빌드**
3. **백엔드 서버 시작**

### dev-server-simple.py
1. **빌드 과정 생략**
2. **바로 백엔드 서버 시작**

## 📋 환경 요구사항

### 필수 설치
- **Python 3.11+**
- **Node.js 18+**
- **npm**

### 권장 설치
- **Git**
- **VS Code** (개발용)

### 가상환경
```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 가상환경 활성화 (Linux/Mac)
source venv/bin/activate
```

## 🐛 문제 해결

### npm 명령어 오류
```bash
# Node.js 설치 확인
node --version
npm --version

# npm 캐시 정리
npm cache clean --force

# node_modules 재설치
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Python 패키지 오류
```bash
# 가상환경 확인
python -c "import sys; print('가상환경:', '활성화됨' if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) else '비활성화됨')"

# 패키지 재설치
pip install -r backend/requirements.txt
```

### 포트 충돌
```bash
# 포트 사용 확인
netstat -ano | findstr :5000

# 프로세스 종료
taskkill /PID <PID> /F
```

### 빌드 오류
```bash
# 프론트엔드 빌드 수동 실행
cd frontend
npm run build:dev

# 백엔드 서버 수동 실행
cd backend
python app.py
```

## 📊 로그 확인

### 개발 서버 로그
```bash
# 실시간 로그 확인
tail -f backend/logs/app.log

# Flask 로그
python deploy/dev-server/dev-server.py 2>&1 | tee dev.log
```

### 빌드 로그
```bash
# 프론트엔드 빌드 로그
cd frontend
npm run build:dev --verbose

# 백엔드 로그
cd backend
python app.py --debug
```

## 🔄 자동화 스크립트

### package.json 스크립트
```json
{
  "scripts": {
    "dev": "python deploy/dev-server/dev-server.py",
    "dev:auto": "python deploy/dev-server/auto-dev.py",
    "auto": "python deploy/dev-server/auto-dev.py"
  }
}
```

### Windows 배치 파일
```batch
@echo off
cd /d %~dp0
python deploy/dev-server/dev-server.py
pause
```

## 📞 지원

- **개발 이슈**: GitHub Issues
- **빌드 오류**: 로그 파일 확인
- **환경 설정**: auto-dev.py 사용 권장 