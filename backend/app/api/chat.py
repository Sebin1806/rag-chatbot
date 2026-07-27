from fastapi import APIRouter
from pydantic import BaseModel
from app.database.database import SessionLocal
from app.database.crud import update_session_title
#from fastapi import Depends
#from app.utils.auth import get_current_user
from app.services.retrieval_service import RetrievalService
from app.services.llm.llm_service import LLMService
from app.services.memory_service import MemoryService
from fastapi.responses import StreamingResponse
from app.services.llm.llm_stream_service import LLMStreamService

router = APIRouter()


class ChatRequest(BaseModel):
    session_id: str
    question: str


@router.post("/")
async def chat(request: ChatRequest):

    # Load previous conversation
    history = MemoryService.get_history(request.session_id)

    # Retrieve document context
    retrieved = RetrievalService.retrieve(request.question)

    context = "\n\n".join(retrieved["context"])
    # No relevant context found
    if len(retrieved["context"]) == 0:

        return {
            "question": request.question,
            "answer": "I couldn't find that information in the uploaded documents.",
            "sources": []
        }

    # Build conversation history
    history_text = ""

    for message in history:
        history_text += (
            f"{message['role'].capitalize()}: "
            f"{message['content']}\n"
        )

    prompt = f"""
You are an AI assistant that answers ONLY using the provided document context.

IMPORTANT RULES:

1. Use ONLY the information from Document Context.
2. Never use your own knowledge.
3. Never guess.
4. Never invent facts.
5. If the answer is missing from the document context, reply exactly:

I couldn't find that information in the uploaded documents.

Conversation History:
{history_text}

Document Context:
{context}

Question:
{request.question}

Answer:
"""

    answer = LLMService.generate_answer(
        request.question,
        prompt
    )
    db = SessionLocal()

    update_session_title(
        db,
        request.session_id,
        request.question[:40]
    )

    db.close()

    # Save new conversation
    MemoryService.add_message(
        request.session_id,
        "user",
        request.question
    )

    MemoryService.add_message(
        request.session_id,
        "assistant",
        answer
    )
    print("\n===== RETRIEVAL DEBUG =====")
    print(retrieved)
    print("===========================\n")
    return {
        "question": request.question,
        "answer": answer,
        "sources": retrieved["sources"]
    }

@router.post("/stream")
async def stream_chat(request: ChatRequest):

    # Load previous conversation
    history = MemoryService.get_history(request.session_id)

    # Retrieve document context
    retrieved = RetrievalService.retrieve(request.question)
    print("\n===== STREAM RETRIEVAL =====")
    print(retrieved)
    print("============================\n")
    context = "\n\n".join(retrieved["context"])

    # Build conversation history
    history_text = ""

    for message in history:
        history_text += (
            f"{message['role'].capitalize()}: "
            f"{message['content']}\n"
        )

    prompt = f"""
You are a helpful AI assistant.

Conversation History:
{history_text}

Document Context:
{context}

Current Question:
{request.question}

Answer using both the conversation history and the document context.
If the answer is not found, clearly say so.
"""

    def generate():

        full_answer = ""

        for token in LLMStreamService.stream_answer(
            prompt
        ):

            full_answer += token

            yield f"data: {token} \n\n"

        # Save conversation after streaming finishes
        MemoryService.add_message(
            request.session_id,
            "user",
            request.question
        )

        MemoryService.add_message(
            request.session_id,
            "assistant",
            full_answer
        )

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )