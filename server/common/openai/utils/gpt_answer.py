import json
from typing import Dict, Any

def format_response(response : Dict[str, Any]) -> str :
    answer = response.answer
    questions = response.additional_questions

    # 추가 질문을 문자열로 변환
    questions = "".join([f"- {q}\n" for q in questions])
    
    # 최종 문자열
    formatted_response = f"""{answer}\n\n추가로 도움이 필요하신가요?\n{questions}"""
    return formatted_response