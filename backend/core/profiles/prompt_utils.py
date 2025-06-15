import json
import os
from typing import Dict, List, Optional

def load_prompt_profile(profile_name: str) -> Dict:
    """
    프롬프트 프로필을 로드하는 함수
    
    Args:
        profile_name: 프로필 이름 (예: 'policy_assistant', 'hr_assistant')
        
    Returns:
        Dict: 프로필 정보 (role과 rules 포함)
        
    Raises:
        FileNotFoundError: 프로필 파일을 찾을 수 없는 경우
        KeyError: 요청한 프로필이 존재하지 않는 경우
    """
    # 프로필 파일 경로
    profile_path = os.path.join(os.path.dirname(__file__), 'gpt_prompt_profile.json')
    
    # 프로필 파일 로드
    with open(profile_path, 'r', encoding='utf-8') as f:
        profiles = json.load(f)
    
    # 요청한 프로필이 존재하는지 확인
    if profile_name not in profiles:
        raise KeyError(f"프로필 '{profile_name}'을 찾을 수 없습니다.")
    
    return profiles[profile_name]

def format_system_prompt(profile_name: str) -> str:
    """
    시스템 프롬프트를 포맷팅하는 함수
    
    Args:
        profile_name: 프로필 이름
        
    Returns:
        str: 포맷팅된 시스템 프롬프트
    """
    profile = load_prompt_profile(profile_name)
    
    # 프롬프트 포맷팅
    prompt = f"{profile['role']}\n다음 규칙을 반드시 지켜주세요:\n"
    
    # 규칙 추가
    for i, rule in enumerate(profile['rules'], 1):
        prompt += f"{i}. {rule}\n"
    
    return prompt.strip()

def get_available_profiles() -> List[str]:
    """
    사용 가능한 프로필 목록을 반환하는 함수
    
    Returns:
        List[str]: 프로필 이름 목록
    """
    profile_path = os.path.join(os.path.dirname(__file__), 'gpt_prompt_profile.json')
    
    with open(profile_path, 'r', encoding='utf-8') as f:
        profiles = json.load(f)
    
    return list(profiles.keys()) 