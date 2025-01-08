from fastapi import FastAPI
import uvicorn

from server.router import chat

app = FastAPI(
    title="RAG Chatbot",
    debug=True
)

app.include_router(chat.router, prefix="/api")

if __name__ == "__main__":
    # uvicorn을 통해 FastAPI 애플리케이션 실행
    uvicorn.run("server.main:app", host="127.0.0.1", port=8000, reload=True)