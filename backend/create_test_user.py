#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
테스트용 사용자 생성 스크립트
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.auth_service import create_test_user

def main():
    """메인 함수"""
    print("=== 테스트 사용자 생성 ===")
    
    # 테스트 사용자 정보
    test_email = "test@ywlabs.com"
    test_password = "test1234"
    test_name = "테스트 사용자"
    
    print(f"이메일: {test_email}")
    print(f"비밀번호: {test_password}")
    print(f"이름: {test_name}")
    
    # 사용자 생성
    success = create_test_user(test_email, test_password, test_name, "user")
    
    if success:
        print("\n✅ 테스트 사용자 생성 완료!")
        print(f"이제 {test_email} / {test_password}로 로그인할 수 있습니다.")
    else:
        print("\n❌ 테스트 사용자 생성 실패!")

if __name__ == "__main__":
    main() 