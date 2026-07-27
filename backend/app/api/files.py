from fastapi import APIRouter

from app.services.vector_db_service import VectorDBService

router = APIRouter()


@router.get("/")
def get_documents():

    return {
        "documents": VectorDBService.list_documents()
    }


@router.delete("/{filename}")
def delete_document(filename: str):

    VectorDBService.delete_document(filename)

    return {
        "message": f"{filename} deleted successfully."
    }


@router.delete("/")
def clear_all():

    VectorDBService.clear_database()

    return {
        "message": "All documents deleted."
    }