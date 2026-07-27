from app.database.database import Base, engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.document import router as document_router
from app.api.chat import router as chat_router
from app.api.files import router as files_router
from app.api.session import router as session_router
from app.database import models
from app.services.bm25_service import BM25Service
from app.services.vector_db_service import VectorDBService
#from app.api.auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="RAG Chatbot API",
    version="1.0.0"
)

#app.include_router(
#    auth_router,
#    prefix="/api/auth",
#    tags=["Authentication"]
#)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    document_router,
    prefix="/api/document",
    tags=["Document"]
)

app.include_router(
    session_router,
    prefix="/api/session",
    tags=["Session"]
)

app.include_router(
    chat_router,
    prefix="/api/chat",
    tags=["Chat"]
)

app.include_router(
    files_router,
    prefix="/api/files",
    tags=["Files"]
)

@app.on_event("startup")
def load_bm25():

    data = VectorDBService.collection.get(
        include=["documents", "metadatas"]
    )

    BM25Service.build(
        data["documents"],
        data["metadatas"]
    )

    print("BM25 Loaded")

@app.get("/")
def home():
    return {
        "message": "RAG Chatbot Backend Running"
    }

@app.get("/api/test")
def test():
    return {
        "status": "success",
        "message": "Backend Connected Successfully!"
    }