import requests


class HyDEService:

    OLLAMA_URL = "http://localhost:11434/api/generate"

    MODEL = "llama3.2:3b"

    @staticmethod
    def generate(question: str):

        prompt = f"""
You are an expert assistant.

Write a detailed paragraph that would answer the following question.

Do NOT say "I don't know."

Do NOT mention this is hypothetical.

Question:
{question}

Answer:
"""

        payload = {
            "model": HyDEService.MODEL,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(
            HyDEService.OLLAMA_URL,
            json=payload
        )

        return response.json()["response"].strip()