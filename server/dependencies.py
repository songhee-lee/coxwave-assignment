# db/chromadb
from chromadb import PersistentClient
from fastapi import Depends

from server.db.chromadb.config import ChromaDBSettings
from server.db.chromadb.services.database import ChromaDB

# llm/openai
from server.llm.openai.config import OpenAISettings
from server.llm.openai.services.embedding import EmbeddingService
from server.llm.openai.services.gpt import OpenAILLM
from server.llm.openai.utils.tokenizer import OpenAITokenizer

# modules/chat
from server.modules.chat.config import ChatSettings

# log
from server.core.logging.config import setup_logging

logger = setup_logging(__name__)

def get_openai_settings():
    try :
        return OpenAISettings()
    except Exception as e :
        logger.error("Error when get openai settings.")
    

def get_embedding_service(
    openai_settings: OpenAISettings = Depends(get_openai_settings),
):
    try :
        openai_tokenizer = OpenAITokenizer(settings=openai_settings)
        return EmbeddingService(
            api_key=openai_settings.OPENAI_API_KEY,
            settings=openai_settings,
            tokenizer=openai_tokenizer,
        )
    except Exception as e :
        logger.error("Error when get embedding services.")

def get_llm_service(openai_settings: OpenAISettings = Depends(get_openai_settings)):
    try :
        return OpenAILLM(api_key=openai_settings.OPENAI_API_KEY, settings=openai_settings)
    except Exception as e :
        logger.error("Error when get llm services.")

def get_chromadb_service(
    embedding_service: EmbeddingService = Depends(get_embedding_service),
):
    try :
        chromadb_settings = ChromaDBSettings()
        return ChromaDB(
            settings=chromadb_settings,
            client=PersistentClient(path=chromadb_settings.CHROMADB_PATH),
            embedding_service=embedding_service,
        )
    except Exception as e :
        logger.error("Error when get chromadb services.")


def get_chat_settings():
    try :
        return ChatSettings()
    except Exception as e :
        logger.error("Error when get chat settings.")
