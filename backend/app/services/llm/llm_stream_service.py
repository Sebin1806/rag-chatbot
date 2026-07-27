import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(
    api_key=os.getenv("GOOGLE_API_KEY")
)


class LLMStreamService:

    model = genai.GenerativeModel("gemini-2.5-flash")

    @staticmethod
    def stream_answer(prompt: str):

        try:

            response = LLMStreamService.model.generate_content(
                prompt,
                stream=True
            )

            for chunk in response:

                if hasattr(chunk,"text") and chunk.text:
                    print(chunk.text,end="",flush=True)

                    yield chunk.text

        except Exception as e:

            yield f"\nError: {e}"