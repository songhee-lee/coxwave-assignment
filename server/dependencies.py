from fastapi import Depends

# db/chromadb
from chromadb import PersistentClient
from server.db.chromadb.config import ChromaDBSettings
from server.db.chromadb.services.database import ChromaDB

# llm/openai
from server.llm.openai.config import OpenAISettings
from server.llm.openai.services.embedding import EmbeddingService
from server.llm.openai.utils.tokenizer import OpenAITokenizer
from server.llm.openai.services.gpt import OpenAILLM

# modules/chat
from server.modules.chat.config import ChatSettings


def get_openai_settings() :
    return OpenAISettings()

def get_embedding_service(openai_settings: OpenAISettings = Depends(get_openai_settings)) :
    openai_tokenizer = OpenAITokenizer(settings=openai_settings)
    return EmbeddingService(
        api_key=openai_settings.OPENAI_API_KEY, 
        settings=openai_settings,
        tokenizer=openai_tokenizer
    )

def get_llm_service(openai_settings: OpenAISettings = Depends(get_openai_settings)) :
    return OpenAILLM(
        api_key=openai_settings.OPENAI_API_KEY, 
        settings=openai_settings
    )

def get_chromadb_service(embedding_service : EmbeddingService = Depends(get_embedding_service)) :
    chromadb_settings = ChromaDBSettings()
    return ChromaDB(
        settings=chromadb_settings, 
        client=PersistentClient(path=chromadb_settings.CHROMADB_PATH),
        embedding_service=embedding_service
    )

def get_chat_settings() :
    return ChatSettings()