#!/usr/bin/env python3
"""
자동 가상환경 관리 및 개발 서버 실행 스크립트
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_venv():
    """가상환경 상태 확인"""
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

def get_venv_activate_path():
    """가상환경 활성화 스크립트 경로 반환"""
    if platform.system() == "Windows":
        return "venv\\Scripts\\activate.bat"
    else:
        return "venv/bin/activate"

def create_venv():
    """가상환경 생성"""
    print("📦 새 가상환경을 생성합니다...")
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ 가상환경 생성 완료!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 가상환경 생성 실패: {e}")
        return False

def install_requirements():
    """Python 패키지 설치"""
    print("📥 Python 패키지 설치 중...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"], check=True)
        print("✅ Python 패키지 설치 완료!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Python 패키지 설치 실패: {e}")
        return False

def install_frontend():
    """Frontend 패키지 설치"""
    print("📦 Frontend 패키지 설치 중...")
    try:
        # npm 경로 확인 및 실행
        npm_cmd = "npm"
        if platform.system() == "Windows":
            # Windows에서 npm 경로 확인
            possible_paths = [
                "D:\\Programs\\nodejs\\npm.cmd",
                "C:\\Program Files\\nodejs\\npm.cmd",
                "C:\\Program Files (x86)\\nodejs\\npm.cmd",
                os.path.expanduser("~\\AppData\\Roaming\\npm\\npm.cmd")
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    npm_cmd = path
                    break
        
        subprocess.run([npm_cmd, "install"], cwd="frontend", check=True)
        print("✅ Frontend 패키지 설치 완료!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Frontend 패키지 설치 실패: {e}")
        return False

def build_frontend():
    """Frontend 빌드"""
    print("🔨 Frontend 빌드 중...")
    try:
        # npm 경로 확인 및 실행
        npm_cmd = "npm"
        if platform.system() == "Windows":
            # Windows에서 npm 경로 확인
            possible_paths = [
                "D:\\Programs\\nodejs\\npm.cmd",
                "C:\\Program Files\\nodejs\\npm.cmd",
                "C:\\Program Files (x86)\\nodejs\\npm.cmd",
                os.path.expanduser("~\\AppData\\Roaming\\npm\\npm.cmd")
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    npm_cmd = path
                    break
        
        subprocess.run([npm_cmd, "run", "build:dev"], cwd="frontend", check=True)
        print("✅ Frontend 빌드 완료!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Frontend 빌드 실패: {e}")
        return False

def start_dev_server():
    """개발 서버 시작"""
    print("🚀 개발 서버 시작...")
    try:
        subprocess.run([sys.executable, "apply/apply_dev/dev-server.py"])
    except KeyboardInterrupt:
        print("\n👋 서버가 중지되었습니다.")

def main():
    """메인 함수"""
    print("=" * 50)
    print("🎯 YWLab 자동 개발 환경 설정")
    print("=" * 50)
    
    # 현재 디렉토리 확인
    if not Path("backend").exists() or not Path("frontend").exists():
        print("❌ 프로젝트 루트 디렉토리에서 실행해주세요.")
        return
    
    # 가상환경 상태 확인
    if check_venv():
        print("✅ 가상환경이 이미 활성화되어 있습니다.")
    else:
        print("⚠️ 가상환경이 활성화되지 않았습니다.")
        
        # 가상환경 존재 확인
        venv_path = Path("venv")
        if not venv_path.exists():
            print("📦 가상환경이 없습니다. 새로 생성합니다...")
            if not create_venv():
                return
        
        # 가상환경 활성화 안내
        activate_path = get_venv_activate_path()
        print(f"🔄 가상환경을 활성화해주세요:")
        if platform.system() == "Windows":
            print(f"   {activate_path}")
        else:
            print(f"   source {activate_path}")
        print("   그 후 이 스크립트를 다시 실행하세요.")
        return
    
    # 의존성 설치 확인
    print("📋 의존성 설치 상태 확인...")
    
    # Frontend 의존성 확인
    frontend_node_modules = Path("frontend/node_modules")
    if not frontend_node_modules.exists():
        print("📦 Frontend 의존성 설치 중...")
        if not install_frontend():
            return
    
    # Backend 의존성 확인 (가상환경에서)
    try:
        import flask
        print("✅ Python 의존성 확인됨")
    except ImportError:
        print("📥 Python 의존성 설치 중...")
        if not install_requirements():
            return
    
    # Frontend 빌드 (항상 최신 소스 적용)
    print("🔨 Frontend 빌드 중...")
    if not build_frontend():
        return
    
    print("✅ 모든 준비 완료!")
    print("=" * 50)
    
    # 개발 서버 시작
    start_dev_server()

if __name__ == "__main__":
    main() 