#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
비밀번호 해시 수정 스크립트
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.auth_service import update_user_password

def main():
    """메인 함수"""
    print("=== 비밀번호 해시 수정 ===")
    
    # 수정할 사용자 정보
    email = "admin@ywlabs.com"
    new_password = "admin1234"
    
    print(f"이메일: {email}")
    print(f"새 비밀번호: {new_password}")
    
    # 비밀번호 업데이트
    success = update_user_password(email, new_password)
    
    if success:
        print("\n✅ 비밀번호 해시 수정 완료!")
        print(f"이제 {email} / {new_password}로 로그인할 수 있습니다.")
    else:
        print("\n❌ 비밀번호 해시 수정 실패!")

if __name__ == "__main__":
    main() 