import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env
load_dotenv()

# Configure Gemini API
genai.configure(
    api_key=os.getenv("GOOGLE_API_KEY")
)


class LLMService:

    # Gemini model
    model = genai.GenerativeModel("gemini-2.5-flash")

    @staticmethod
    def generate_answer(question: str, context: str):

        prompt = f"""
You are a professional AI assistant using Retrieval-Augmented Generation (RAG).

Your task is to answer ONLY using the provided document context.

Rules:
- Read ALL retrieved document chunks before answering.
- Combine information from multiple chunks.
- Write complete, natural sentences.
- If multiple skills, technologies, or facts are present, include all relevant ones.
- Do not hallucinate.
- If the answer isn't found, reply:
  "I couldn't find that information in the uploaded documents."

====================
DOCUMENT CONTEXT
====================

{context}

====================
QUESTION
====================

{question}

====================
FINAL ANSWER
====================
"""

        try:
            response = LLMService.model.generate_content(prompt)

            if response and response.text:
                return response.text.strip()

            return "I couldn't generate an answer."

        except Exception as e:
            print("Gemini Error:", e)
            return f"Error generating answer: {str(e)}"