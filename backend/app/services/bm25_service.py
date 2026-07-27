from rank_bm25 import BM25Okapi


class BM25Service:

    bm25 = None
    documents = []
    metadatas = []

    @staticmethod
    def build(documents, metadatas):

        BM25Service.documents = documents
        BM25Service.metadatas = metadatas

        tokenized = [
            doc.lower().split()
            for doc in documents
        ]

        BM25Service.bm25 = BM25Okapi(tokenized)

    @staticmethod
    def search(query, top_k=10):

        if BM25Service.bm25 is None:
            return []

        scores = BM25Service.bm25.get_scores(
            query.lower().split()
        )

        ranked = sorted(
            zip(
                BM25Service.documents,
                BM25Service.metadatas,
                scores
            ),
            key=lambda x: x[2],
            reverse=True
        )

        return ranked[:top_k]