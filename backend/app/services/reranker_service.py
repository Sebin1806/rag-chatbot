from sentence_transformers import CrossEncoder


class RerankerService:

    # Lightweight and fast reranker
    model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    @staticmethod
    def rerank(question, documents, top_k=5):

        if not documents:
            return []

        pairs = []

        for doc in documents:
            pairs.append([question, doc])

        scores = RerankerService.model.predict(pairs)

        ranked = list(zip(documents, scores))

        ranked.sort(key=lambda x: x[1], reverse=True)

        return ranked[:top_k]