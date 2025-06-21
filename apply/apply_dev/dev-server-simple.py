#!/usr/bin/env python3
"""
간단한 로컬 개발 서버 스크립트 (인코딩 문제 해결)
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """메인 함수"""
    print("=" * 50)
    print("🎯 YWLab 간단한 개발 서버")
    print("=" * 50)
    
    # Frontend 빌드 파일 확인
    frontend_dist = Path("frontend/dist/index.html")
    
    if not frontend_dist.exists():
        print("❌ Frontend 빌드 파일이 없습니다.")
        print("💡 다음 명령어를 수동으로 실행해주세요:")
        print("   cd frontend && npm run build")
        print("   cd ..")
        return
    
    print("✅ Frontend 빌드 파일 확인됨")
    print("🚀 Flask 서버 시작...")
    print("📍 서버 주소: http://localhost:5000")
    print("🔄 서버를 중지하려면 Ctrl+C를 누르세요.")
    print("-" * 50)
    
    # Flask 서버 시작
    try:
        subprocess.run([sys.executable, "app.py"], cwd="backend")
    except KeyboardInterrupt:
        print("\n👋 서버가 중지되었습니다.")

if __name__ == "__main__":
    main() 