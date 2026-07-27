import re


class ContextCompressionService:

    @staticmethod
    def compress(question, documents, top_sentences=5):

        question_words = set(
            question.lower().split()
        )

        scored = []

        for doc in documents:

            sentences = re.split(
                r'(?<=[.!?])\s+',
                doc
            )

            for sentence in sentences:

                words = set(sentence.lower().split())

                score = len(
                    question_words.intersection(words)
                )

                if score > 0:

                    scored.append(
                        (sentence.strip(), score)
                    )

        scored.sort(
            key=lambda x: x[1],
            reverse=True
        )

        compressed = []

        used = set()

        for sentence, score in scored:

            if sentence not in used:

                compressed.append(sentence)

                used.add(sentence)

            if len(compressed) >= top_sentences:
                break

        return "\n".join(compressed)