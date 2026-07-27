from app.services.llm.llm_service import LLMService

answer = LLMService.generate_answer(
    "What is Python?",
    "Python is a programming language created by Guido van Rossum."
)

print(answer)