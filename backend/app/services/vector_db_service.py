import os
import shutil
import uuid

import chromadb


class VectorDBService:

    client = chromadb.PersistentClient(
        path="./chroma_db"
    )

    collection = client.get_or_create_collection(
        name="technical_documents"
    )

    @staticmethod
    def store(
        chunks,
        embeddings,
        filename,
        metadatas=None
    ):

        ids = []
        final_metadatas = []

        if hasattr(embeddings, "tolist"):
            embeddings = embeddings.tolist()

        for i in range(len(chunks)):

            ids.append(str(uuid.uuid4()))

            metadata = {
                "filename": filename,
                "chunk": i
            }

            if metadatas:
                metadata.update(metadatas[i])

            final_metadatas.append(metadata)

        VectorDBService.collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=final_metadatas
        )

    @staticmethod
    def search(query_embedding, top_k=10):

        if hasattr(query_embedding, "tolist"):
            query_embedding = query_embedding.tolist()

        # Initial semantic search
        results = VectorDBService.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=[
                "documents",
                "metadatas",
                "distances"
            ]
        )
        return results



    @staticmethod
    def list_documents():

        data = VectorDBService.collection.get(
            include=["metadatas"]
        )

        documents = set()

        for metadata in data["metadatas"]:

            if metadata and "filename" in metadata:
                documents.add(metadata["filename"])

        return sorted(documents)

    @staticmethod
    def delete_document(filename):

        data = VectorDBService.collection.get(
            where={
                "filename": filename
            }
        )

        if data["ids"]:
            VectorDBService.collection.delete(
                ids=data["ids"]
            )

        file_path = os.path.join(
            "uploads",
            filename
        )

        if os.path.exists(file_path):
            os.remove(file_path)

    @staticmethod
    def get_chunk(filename, page, chunk):

        results = VectorDBService.collection.get(
            where={
                "$and": [
                    {"filename": filename},
                    {"page": page},
                    {"chunk": chunk}
                ]
            },
            include=["documents"]
        )

        if results["documents"]:
            return results["documents"][0]

        return None        

    @staticmethod
    def clear_database():

        shutil.rmtree(
            "./chroma_db",
            ignore_errors=True
        )

        shutil.rmtree(
            "./uploads",
            ignore_errors=True
        )

        os.makedirs(
            "./uploads",
            exist_ok=True
        )

        VectorDBService.client = chromadb.PersistentClient(
            path="./chroma_db"
        )

        VectorDBService.collection = (
            VectorDBService.client.get_or_create_collection(
                name="technical_documents"
            )
        )