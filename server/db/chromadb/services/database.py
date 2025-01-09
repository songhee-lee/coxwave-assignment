import os
import pickle
import chromadb
from typing import List

from server.library.naver_store_faq import make_document
from server.db.chromadb.config import chromadb_settings
from server.llm.openai.services.embedding import text_to_embedding

class DataBase :
    """
    ChromaDB 데이터베이스 클래스
    """
    def load_data(self, file_path) :
        if os.path.exists(file_path) :
            with open(file_path, "rb") as f :
                return pickle.load(f)
        return False

    def add_to_chromadb(self, documents: List[str], embeddings: List[List[float]], ids: List[str]) -> None:
        """
        ChromaDB에 데이터 추가
        documents: 문서 리스트
        embeddings: 문서 임베딩 리스트
        """
        self.collection.add(
            documents=documents, 
            embeddings=embeddings,
            ids=ids
        )

    def load_database(self, collection_name : str) :
        """
        기본 세팅 초기화
        """

        # ChromaDB 클라이언트 설정
        print(chromadb_settings.CHROMADB_PATH)
        client = chromadb.PersistentClient(path=chromadb_settings.CHROMADB_PATH)
        try :
            self.collection = client.get_collection(collection_name)
            print(f"Load {collection_name}...")
        
        except Exception :
            print(f"Create {collection_name}...")
            self.collection = client.create_collection(collection_name)
            collection_info = chromadb_settings.get_collection_info(collection_name)

            # 기존에 저장된 collection이 있는지 확인하기
            collection_data = self.load_data(collection_info.COLLECTION_PATH)
            if collection_data :
                print("기존 DB 로딩...")
                self.add_to_chromadb(collection_data["documents"], collection_data["embeddings"], collection_data["ids"]) 
            
            # 새로운 collection에 임베딩 데이터 추가하기
            print(f"Load the data from '{collection_info.FILE_PATH}'")
            
            # 파일 경로에서 데이터 불러오기
            data = self.load_data(collection_info.FILE_PATH)
            
            documents = []
            embeddings = []
            ids = []
            
            dir_path = f"{chromadb_settings.CHROMADB_PATH}/document"
            if not os.path.exists(dir_path) :
                os.mkdir(dir_path)
                print(f"Make dir '{dir_path}'")
                
            for idx, (key, value) in enumerate(data.items()):
                # document file 확인하기 (기존 임베딩)
                file_path = f"{chromadb_settings.CHROMADB_PATH}/document/document_{idx}.pkl"
                    
                doc = self.load_data(file_path)
                if doc :
                    text = doc["text"]
                    embedding = doc["embedding"]
                # 새롭게 임베딩 진행
                else :
                    text = make_document(key, value)
                    embedding = text_to_embedding(text)

                    with open(file_path, "wb") as f :
                        pickle.dump({"text" : text, "embedding" : embedding}, f)

                documents.append(text)
                embeddings.append(embedding)
                ids.append(str(idx))

            print("새로운 DB 생성...")
            self.add_to_chromadb(documents, embeddings, ids)

            # DB 저장하기
            with open(collection_info.COLLECTION_PATH, "wb") as f:
                pickle.dump({"documents" : documents, "embeddings" : embeddings, "ids":ids}, f)

    def get_relevant_context(self, collection_name, query: str) -> List[str]:
        """
        RAG - 관련 컨텍스트 찾기
        query: 사용자 쿼리
        """
        self.load_database(collection_name)

        query_embedding = text_to_embedding(query)
        result = self.collection.query(query_embeddings=[query_embedding], n_results=1)
        print(result)
        return [doc[0] for doc in result["documents"]]

# DB 인스턴스 생성 및 데이터베이스 로드
chroma_db = DataBase()