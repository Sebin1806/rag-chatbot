class MultiQueryService:

    @staticmethod
    def generate_queries(question: str):

        question = question.strip()

        queries = [
            question,
            f"Explain {question}",
            f"Describe {question}",
            f"Information about {question}",
            f"Details of {question}"
        ]

        # Remove duplicates while preserving order
        seen = set()
        final_queries = []

        for q in queries:
            q = q.strip()

            if q.lower() not in seen:
                final_queries.append(q)
                seen.add(q.lower())

        return final_queries