# FAQ 문서 생성 함수 (독립적인 함수로 유지)
def make_document(key: str, value: str) -> str:
    """
    FAQ 문서 생성 함수
    key: 질문 키
    value: 답변 값
    """
    answer = value.split("위 도움말이 도움이 되었나요?")[0].strip()
    text = f"Query: {key}\nAnswer:\n{answer}"
    
    recommendations = value.split("관련 도움말/키워드")
    if len(recommendations) > 1:
        text += f"\nRecommendations:\n{recommendations[-1].split('도움말 닫기')[0].strip()}"

    return text