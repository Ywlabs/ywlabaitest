import json
from pathlib import Path
from langchain.prompts import PromptTemplate

# 프로필 파일의 절대 경로 설정
# 이 파일(prompt_utils.py)은 backend/core/utils/ 에 위치하므로, 상위 디렉토리로 이동해야 합니다.
PROFILE_PATH = Path(__file__).parent.parent / 'profiles' / 'gpt_prompt_profile.json'

def get_all_profiles():
    """
    gpt_prompt_profile.json 파일에서 모든 프롬프트 프로필을 로드합니다.

    Returns:
        dict: 모든 프롬프트 프로필을 담고 있는 딕셔너리
    """
    try:
        with open(PROFILE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # 실제 운영 환경에서는 로깅 등으로 처리하는 것이 좋습니다.
        print(f"오류: 프로필 파일을 찾을 수 없습니다. 경로: {PROFILE_PATH}")
        return {}
    except json.JSONDecodeError:
        print(f"오류: 프로필 파일의 JSON 형식이 잘못되었습니다. 파일: {PROFILE_PATH}")
        return {}

def get_prompt_profile(profile_name: str):
    """
    지정된 이름의 프롬프트 프로필을 가져옵니다.

    Args:
        profile_name (str): 가져올 프로필의 이름 (예: "RISEN", "COSTAR")

    Returns:
        dict: 해당 프로필의 딕셔너리. 없으면 None.
    """
    profiles = get_all_profiles()
    return profiles.get(profile_name)

def get_langchain_prompt_template(profile_name: str) -> PromptTemplate:
    """
    지정된 프로필을 기반으로 LangChain의 PromptTemplate 객체를 생성합니다.
    새로운 JSON 구조에 최적화되었습니다.

    Args:
        profile_name (str): gpt_prompt_profile.json에 정의된 프로필 이름.

    Returns:
        PromptTemplate: LangChain에서 사용할 수 있는 프롬프트 템플릿 객체.
                        프로필을 찾지 못하거나 형식이 맞지 않으면 None.
    """
    profile = get_prompt_profile(profile_name)
    if not profile:
        print(f"오류: '{profile_name}' 프로필을 찾을 수 없습니다.")
        return None

    template_str = profile.get("template")
    input_vars = profile.get("input_variables")

    if not template_str or not isinstance(input_vars, list):
        print(f"오류: '{profile_name}' 프로필에 'template' 또는 'input_variables'가 유효하지 않습니다.")
        return None

    return PromptTemplate(
        template=template_str,
        input_variables=input_vars
    )

# 사용 예시
if __name__ == '__main__':
    # 1. RISEN 템플릿 사용 예시
    risen_template = get_langchain_prompt_template("RISEN")
    
    if risen_template:
        print("--- RISEN 템플릿 테스트 ---")
        
        # 가이드 출력
        risen_guide = get_prompt_profile("RISEN").get("guide", {})
        print("\n[템플릿 사용 가이드]")
        for key, value in risen_guide.items():
            print(f"- {key}: {value}")

        # 동적 데이터 정의
        dynamic_data = {
            "Role": "당신은 시스템 설계를 담당하는 테크 리드(Tech Lead)입니다.",
            "Instructions": "실시간 환경 데이터를 제공하는 신규 API의 개발 명세서를 작성하세요.",
            "Steps": "1. API 엔드포인트 정의\n2. 요청/응답 스키마 설계\n3. 에러 코드 정의",
            "End_goal": "백엔드 개발자가 즉시 개발에 착수할 수 있는 명확한 명세서 완성.",
            "Narrowing": "내부 시스템 간 연동을 위한 API에 한정. 인증 방식은 API Key 사용."
        }
        
        # 프롬프트 포맷팅
        formatted_prompt = risen_template.format(**dynamic_data)
        
        print("\n[동적으로 완성된 프롬프트]")
        print(formatted_prompt)
        print("-" * 25)

    # 2. 존재하지 않는 프로필 테스트
    non_existent_template = get_langchain_prompt_template("NON_EXISTENT")
    if not non_existent_template:
        print("\n--- 존재하지 않는 프로필 테스트 ---")
        print("프로필을 찾을 수 없습니다.")
        print("-" * 25) 