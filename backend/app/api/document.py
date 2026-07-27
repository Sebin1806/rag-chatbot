from fastapi import APIRouter, UploadFile, File
import os
import shutil

from app.services.document_loader import DocumentLoader
from app.services.chunk_service import ChunkService
from app.services.embedding_service import EmbeddingService
from app.services.vector_db_service import VectorDBService

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    allowed_extensions = [
        ".pdf",
        ".docx",
        ".txt",
        ".md",
        ".html",
        ".htm",
        ".pptx",
        ".xlsx",
        ".xls",
        ".csv"
    ]

    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in allowed_extensions:
        return {
            "success": False,
            "message": f"Unsupported file type: {extension}"
        }

    # -----------------------------
    # Save uploaded file
    # -----------------------------
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # ====================================================
    # PDF Processing (with page numbers)
    # ====================================================

    if extension == ".pdf":

        pages = DocumentLoader.load(file_path)

        all_chunks = []
        all_embeddings = []
        all_metadatas = []

        for page in pages:

            page_chunks = ChunkService.chunk_text(page["text"])

            if len(page_chunks) == 0:
                continue

            page_embeddings = EmbeddingService.create_embeddings(page_chunks)

            all_chunks.extend(page_chunks)
            all_embeddings.extend(page_embeddings)

            for chunk_index in range(len(page_chunks)):

                all_metadatas.append({
                    "page": page["page"],
                    "chunk": chunk_index
                })

        if len(all_chunks) == 0:
            return {
                "success": False,
                "message": "No readable text found in the PDF."
            }
        print("\n===== METADATA TO STORE =====")
        print(all_metadatas[:10])   # Print the first 10 metadata entries
        print("=============================\n")
        VectorDBService.clear_database()
        VectorDBService.store(
            chunks=all_chunks,
            embeddings=all_embeddings,
            filename=file.filename,
            metadatas=all_metadatas
        )
        from app.services.bm25_service import BM25Service
        all_docs = VectorDBService.collection.get(
            include=["documents", "metadatas"]
        )

        BM25Service.build(
            all_docs["documents"],
            all_docs["metadatas"]
        )

        return {
            "success": True,
            "message": "PDF processed successfully.",
            "filename": file.filename,
            "pages": len(pages),
            "total_chunks": len(all_chunks)
        }

    # ====================================================
    # Other Document Types
    # ====================================================

    text = DocumentLoader.load(file_path)

    if not text or not text.strip():
        return {
            "success": False,
            "message": "No readable text found in the document."
        }

    chunks = ChunkService.chunk_text(text)

    if len(chunks) == 0:
        return {
            "success": False,
            "message": "Unable to create text chunks."
        }

    embeddings = EmbeddingService.create_embeddings(chunks)

    if len(embeddings) == 0:
        return {
            "success": False,
            "message": "Embedding generation failed."
        }

    VectorDBService.store(
        chunks=chunks,
        embeddings=embeddings,
        filename=file.filename
    )

    return {
        "success": True,
        "message": "Document processed successfully.",
        "filename": file.filename,
        "file_type": extension,
        "total_characters": len(text),
        "total_chunks": len(chunks)
    }


@router.delete("/{filename}")
async def delete_document(filename: str):

    file_path = os.path.join(
        UPLOAD_DIR,
        filename
    )

    if os.path.exists(file_path):
        os.remove(file_path)

    VectorDBService.delete_document(filename)

    return {
        "message": "Document deleted successfully"
    }