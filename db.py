import os
import pickle
import chromadb
import openai
from typing import List, Dict, Any

from config import settings

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

class DB:
    """
    데이터베이스 클래스
    ChromaDB와 FAQ 데이터를 관리
    """
    def __init__(self) -> None:
        """
        기본 세팅 초기화
        """
        self.file_path: str = settings.db.FILE_PATH               # FAQ 데이터 경로
        self.db_path: str = settings.db.CHROMADB_COLLECTION_PATH  # ChromaDB 경로
        self.data: Dict[str, Any] = {}                            # 데이터 저장 변수

        # ChromaDB 클라이언트 설정
        client = chromadb.PersistentClient(path=settings.db.CHROMADB_PATH)
        self.chroma_db = self.get_or_create_collection(client, settings.db.CHROMADB_NAME)  # ChromaDB 생성 또는 가져오기

        # OpenAI API 키 설정
        openai.api_key = settings.llm.API_KEY

    def load_data(self) -> Dict[str, Any]:
        """
        참고 데이터 로드
        파일 경로에서 데이터 불러오기
        """
        if not os.path.exists(self.file_path):
            print(f"파일의 경로가 올바르지 않습니다: {self.file_path}")
        else:
            print("데이터 불러오기...")
            with open(self.file_path, "rb") as f:
                return pickle.load(f)

    def add_to_chromadb(self, documents: List[str], embeddings: List[List[float]]) -> None:
        """
        ChromaDB에 데이터 추가
        documents: FAQ 문서 리스트
        embeddings: 문서 임베딩 리스트
        """
        self.chroma_db.add(
            documents=documents, 
            embeddings=embeddings,
            ids=list(map(str, range(len(documents))))
        )

    def get_or_create_collection(self, client, name: str): 
        """
        컬렉션 생성 또는 가져오기
        client: ChromaDB 클라이언트
        name: 컬렉션 이름
        """
        try: 
            return client.create_collection(name) 
        except chromadb.errors.UniqueConstraintError: 
            return client.get_collection(name)

    def load_database(self) -> None:
        """
        데이터베이스 로드
        기존 데이터베이스가 있으면 로드하고, 없으면 새로 생성
        """
        if os.path.exists(self.db_path):
            with open(self.db_path, "rb") as f:
                collection_data = pickle.load(f)
                print("기존 DB 로딩...")
                self.add_to_chromadb(collection_data["documents"], collection_data["embeddings"])
        else:
            self.data = self.load_data()
            documents = []
            embeddings = []
            for key, value in self.data.items()[:10]:
                text = make_document(key, value)
                embedding = self.text_to_embedding(text)
    
                documents.append(text)
                embeddings.append(embedding)

            print("새로운 DB 생성...")
            self.add_to_chromadb(documents, embeddings)

            # DB 저장하기
            with open(self.db_path, "wb") as f:
                pickle.dump({"documents": documents, "embeddings": embeddings}, f)

    def text_to_embedding(self, text: str) -> List[float]:
        """
        텍스트 임베딩 생성
        text: 입력 텍스트
        """
        return openai.Embedding.create(
            input=text,
            model=settings.llm.EMBEDDING_MODEL
        )["data"][0]["embedding"]

    def get_relevant_context(self, query: str) -> List[str]:
        """
        RAG - 관련 컨텍스트 찾기
        query: 사용자 쿼리
        """
        query_embedding = self.text_to_embedding(query)
        result = self.chroma_db.query(query_embeddings=[query_embedding], n_results=1)
        return [doc for doc in result["documents"]]

# DB 인스턴스 생성 및 데이터베이스 로드
db = DB()
db.load_database()
