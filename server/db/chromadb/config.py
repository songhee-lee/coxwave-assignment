import os
from typing import Dict, Any, Type

from dotenv import load_dotenv
load_dotenv()


class NaverStoreFAQSettings :
    NAVER_STORE_FAQ_COLLECTION_NAME : str = os.getenv("NAVER_STORE_FAQ_COLLECTION_NAME")
    
    FILE_PATH : str
    COLLECTION_PATH : str

    def __init__(self, db_data_path, db_collection_path, **kwargs) :
        super().__init__(**kwargs)
        self.FILE_PATH = f"{db_data_path}/{self.NAVER_STORE_FAQ_COLLECTION_NAME}.pkl"
        self.COLLECTION_PATH = f"{db_collection_path}/{self.NAVER_STORE_FAQ_COLLECTION_NAME}.pkl"

class ChromaDBSettings :
    CHROMADB_PATH : str = os.getenv("CHROMADB_PATH")
    DB_DATA_PATH : str = os.getenv("DB_DATA_PATH")
    DB_COLLECTION_PATH : str = os.getenv("DB_COLLECTION_PATH")

    NAVER_STORE_FAQ : NaverStoreFAQSettings
    
    def __init__(self, **kwargs) :
        super().__init__(**kwargs)
        self.NAVER_STORE_FAQ = NaverStoreFAQSettings(self.DB_DATA_PATH, self.DB_COLLECTION_PATH)
        self.collections = self._initialize_collections()
    
    def _initialize_collections(self) -> Dict[str, Any] :
        collections = {}
        for attr_name, attr_type in self.__annotations__.items():
            if "DB" in attr_name :   # 예외 처리
                continue
            collections[attr_name.lower()] = getattr(self, attr_name)

        return collections

    def get_collection_info(self, collection_name : str) -> Dict[str, Any] :
        return self.collections.get(collection_name.lower(), None)