#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ChromaDB 컬렉션 초기화 스크립트
"""

import sys
import os

# 프로젝트 루트를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    """메인 함수"""
    try:
        print("ChromaDB 컬렉션 초기화 시작...")
        
        # 환경변수 설정 (개발 환경용)
        os.environ.setdefault('DB_HOST', '192.168.0.200')
        os.environ.setdefault('DB_USER', 'ywlabsdev')
        os.environ.setdefault('DB_PASSWORD', 'ywlabs#20151010Q')
        os.environ.setdefault('DB_NAME', 'ywlabtest')
        os.environ.setdefault('DB_PORT', '3307')
        os.environ.setdefault('APP_PROFILE', 'dev')
        
        # ChromaDB 서비스 import 및 초기화
        from services.chroma_service import initialize_collections
        
        print("컬렉션 초기화 중...")
        initialize_collections()
        
        print("✓ ChromaDB 컬렉션 초기화 완료!")
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 