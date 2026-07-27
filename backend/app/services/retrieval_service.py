from app.services.embedding_service import EmbeddingService
from app.services.vector_db_service import VectorDBService
from app.services.reranker_service import RerankerService
from app.services.multi_query_service import MultiQueryService
from app.services.context_compression_service import ContextCompressionService
from app.services.bm25_service import BM25Service
from app.services.hyde_service import HyDEService


class RetrievalService:

    @staticmethod
    def retrieve(question: str):

        # --------------------------------------------------
        # STEP 1 : Multi Query Generation
        # --------------------------------------------------

        queries = MultiQueryService.generate_queries(question)

        print("\n========== MULTI QUERY ==========\n")

        for q in queries:
            print(q)

        print("\n=================================\n")

        all_documents = []
        all_metadatas = []
        all_distances = []

        seen = set()

        # --------------------------------------------------
        # STEP 2 : HyDE + Dense Retrieval
        # --------------------------------------------------

        for q in queries:

            print("\n========== HYDE ==========\n")

            hyde_document = HyDEService.generate(q)

            print(hyde_document)

            print("\n==========================\n")

            query_embedding = EmbeddingService.model.encode(
                hyde_document
            )

            results = VectorDBService.search(
                query_embedding=query_embedding,
                top_k=20
            )

            docs = results["documents"][0]
            metas = results["metadatas"][0]
            dists = results["distances"][0]

            for doc, meta, dist in zip(docs, metas, dists):

                key = (
                    meta.get("filename"),
                    meta.get("page"),
                    meta.get("chunk")
                )

                if key not in seen:

                    seen.add(key)

                    all_documents.append(doc)
                    all_metadatas.append(meta)
                    all_distances.append(dist)

        # --------------------------------------------------
        # STEP 3 : BM25 Retrieval
        # --------------------------------------------------

        bm25_docs = BM25Service.search(
            question,
            top_k=10
        )

        for item in bm25_docs:

            doc = item["document"]
            meta = item["metadata"]

            key = (
                meta.get("filename"),
                meta.get("page"),
                meta.get("chunk")
            )

            if key not in seen:

                seen.add(key)

                all_documents.append(doc)
                all_metadatas.append(meta)
                all_distances.append(999)

        documents = all_documents
        metadatas = all_metadatas

        # --------------------------------------------------
        # STEP 4 : Hybrid Search Results
        # --------------------------------------------------

        print("\n========== HYBRID SEARCH RESULTS ==========\n")

        for doc, meta in zip(documents, metadatas):

            print(
                f"Chunk {meta.get('chunk')} "
                f"(Page {meta.get('page')})"
            )

            print(doc[:200])
            print()

        print("===========================================\n")

        if len(documents) == 0:

            return {
                "context": [],
                "sources": []
            }

        # --------------------------------------------------
        # STEP 5 : Reranking
        # --------------------------------------------------

        ranked = RerankerService.rerank(
            question,
            documents,
            top_k=5
        )

        print("\n========== RERANKED ==========\n")

        for doc, score in ranked:

            idx = documents.index(doc)

            meta = metadatas[idx]

            print(
                f"Chunk {meta.get('chunk')} "
                f"Score={score:.3f}"
            )

        print("==============================\n")

        # --------------------------------------------------
        # STEP 6 : Best Chunk
        # --------------------------------------------------

        best_document, best_score = ranked[0]

        best_index = documents.index(best_document)

        best_metadata = metadatas[best_index]

        filename = best_metadata["filename"]
        page = best_metadata.get("page", 1)
        chunk = best_metadata.get("chunk", 0)

        # --------------------------------------------------
        # STEP 7 : Neighbor Retrieval
        # --------------------------------------------------

        neighbour_docs = []

        for neighbour_chunk in [chunk - 1, chunk, chunk + 1]:

            if neighbour_chunk < 0:
                continue

            doc = VectorDBService.get_chunk(
                filename=filename,
                page=page,
                chunk=neighbour_chunk
            )

            if doc:
                neighbour_docs.append(doc)

        # --------------------------------------------------
        # STEP 8 : Context Compression
        # --------------------------------------------------

        compressed_context = ContextCompressionService.compress(
            question,
            neighbour_docs,
            top_sentences=6
        )

        print("\n========== CONTEXT COMPRESSION ==========\n")

        print(compressed_context)

        print("\n=========================================\n")

        context = [
            compressed_context
        ]

        sources = [{
            "filename": filename,
            "page": page,
            "chunk": chunk,
            "score": round(float(best_score), 3)
        }]

        # --------------------------------------------------
        # STEP 9 : Final Context
        # --------------------------------------------------

        print("\n===== STREAM RETRIEVAL =====")

        print({
            "context": context,
            "sources": sources
        })

        print("============================\n")

        return {
            "context": context,
            "sources": sources
        }