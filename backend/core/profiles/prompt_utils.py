import json
import os
from typing import Dict, List, Optional
from langchain_core.prompts import ChatPromptTemplate

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

def get_prompt_template(profile_name: str) -> Optional[ChatPromptTemplate]:
    """
    LangChain용 ChatPromptTemplate을 생성하는 함수
    - 'template'과 'input_variables' 키가 있는 프로필에만 적용됩니다.
    """
    try:
        profile = load_prompt_profile(profile_name)
        
        # 1. System/User 역할이 분리된 새 방식 처리
        if "system_template" in profile and "user_template" in profile:
            system_template_content = profile["system_template"]
            user_template_content = profile["user_template"]

            # 배열 -> 문자열 변환
            system_template_string = "\n".join(system_template_content) if isinstance(system_template_content, list) else system_template_content
            user_template_string = "\n".join(user_template_content) if isinstance(user_template_content, list) else user_template_content

            return ChatPromptTemplate.from_messages([
                ("system", system_template_string),
                ("human", user_template_string)
            ])

        # 2. 기존 단일 템플릿 방식 호환성 유지
        elif "template" in profile and "input_variables" in profile:
            template_content = profile["template"]
            
            # 템플릿이 배열이면 문자열로 합칩니다.
            if isinstance(template_content, list):
                template_string = "\n".join(template_content)
            else:
                template_string = template_content

            return ChatPromptTemplate.from_template(
                template=template_string
            )
        else:
            # 템플릿 형식이 아닌 경우, 에러 대신 None을 반환하여 호출 측에서 처리하도록 함
            return None
            
    except (KeyError, FileNotFoundError) as e:
        # 프로필을 찾지 못한 경우에도 None 반환
        print(f"Error loading prompt template for '{profile_name}': {e}")
        return None

def format_system_prompt(profile_name: str) -> str:
    """
    시스템 프롬프트를 포맷팅하는 함수
    
    Args:
        profile_name: 프로필 이름
        
    Returns:
        str: 포맷팅된 시스템 프롬프트
    """
    profile = load_prompt_profile(profile_name)
    
    # 템플릿 기반 프로필인지 확인
    if 'template' in profile:
        # 템플릿 기반 프로필은 이 함수로 포맷팅하지 않음
        raise ValueError(f"'{profile_name}'은 템플릿 기반 프로필이므로 format_system_prompt를 사용할 수 없습니다.")

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