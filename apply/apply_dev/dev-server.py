#!/usr/bin/env python3
"""
로컬 개발용 통합 서버 스크립트
Frontend + Backend를 하나의 포트에서 서빙
"""

import os
import sys
import subprocess
import time
import platform
from pathlib import Path

def get_npm_command():
    """OS에 따른 npm 명령어 반환"""
    if platform.system() == "Windows":
        # Windows에서는 npm.cmd 또는 npm.exe 사용
        npm_commands = ["npm.cmd", "npm.exe", "npm"]
    else:
        npm_commands = ["npm"]
    
    for cmd in npm_commands:
        try:
            subprocess.run([cmd, "--version"], 
                         capture_output=True, 
                         check=True)
            return cmd
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    
    return None

def check_frontend_build():
    """Frontend 빌드 파일 존재 확인"""
    frontend_dist = Path("frontend/dist")
    index_html = frontend_dist / "index.html"
    
    if not index_html.exists():
        print("❌ Frontend 빌드 파일이 없습니다.")
        print("📦 Frontend 빌드를 시작합니다...")
        
        # npm 명령어 확인
        npm_cmd = get_npm_command()
        if not npm_cmd:
            print("❌ npm을 찾을 수 없습니다.")
            print("💡 Node.js가 설치되어 있는지 확인해주세요.")
            print("💡 다음 명령어를 수동으로 실행해주세요:")
            print("   cd frontend && npm run build:dev")
            return False
        
        # Frontend 빌드 실행
        try:
            print(f"🔧 npm 명령어: {npm_cmd}")
            
            # Windows에서 인코딩 문제 해결
            if platform.system() == "Windows":
                # Windows에서는 shell=True와 함께 실행
                result = subprocess.run([npm_cmd, "run", "build:dev"], 
                                      cwd="frontend", 
                                      check=True, 
                                      capture_output=True, 
                                      text=True,
                                      encoding='utf-8',
                                      shell=True)
            else:
                result = subprocess.run([npm_cmd, "run", "build:dev"], 
                                      cwd="frontend", 
                                      check=True, 
                                      capture_output=True, 
                                      text=True,
                                      encoding='utf-8')
            
            print("✅ Frontend 빌드 완료!")
            if result.stdout:
                print("📋 빌드 로그:")
                print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"❌ Frontend 빌드 실패: {e}")
            if e.stdout:
                print("📋 stdout:", e.stdout)
            if e.stderr:
                print("📋 stderr:", e.stderr)
            print("💡 다음 명령어를 수동으로 실행해주세요:")
            print("   cd frontend && npm run build:dev")
            return False
    else:
        print("✅ Frontend 빌드 파일 확인됨")
    
    return True

def start_dev_server():
    """개발 서버 시작"""
    print("🚀 로컬 통합 개발 서버 시작...")
    print("📍 서버 주소: http://localhost:8085")
    print("📝 Frontend + Backend가 하나의 포트에서 서빙됩니다.")
    print("🔄 서버를 중지하려면 Ctrl+C를 누르세요.")
    print("-" * 50)
    
    # Backend 서버 시작
    try:
        subprocess.run([sys.executable, "app.py"], cwd="backend")
    except KeyboardInterrupt:
        print("\n👋 서버가 중지되었습니다.")

def main():
    """메인 함수"""
    print("=" * 50)
    print("🎯 YWLab 통합 개발 서버")
    print("=" * 50)
    
    # 현재 디렉토리 확인
    if not Path("backend").exists() or not Path("frontend").exists():
        print("❌ 프로젝트 루트 디렉토리에서 실행해주세요.")
        print("💡 workspace-ywlabaitest 디렉토리에서 실행하세요.")
        return
    
    # Frontend 빌드 확인 및 실행
    if not check_frontend_build():
        return
    
    # 개발 서버 시작
    start_dev_server()

if __name__ == "__main__":
    main() 