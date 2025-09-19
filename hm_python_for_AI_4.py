import os
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import google.genai as genai
import textwrap

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY)


class RateLimitError(Exception):
    pass


@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=1, max=16),
    retry=retry_if_exception_type((RateLimitError, TimeoutError))
)
def safe_generate(prompt: str):
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        return response

    except Exception as e:
        msg = str(e).lower()
        if "429" in msg or "rate limit" in msg or "quota" in msg:
            print(f"Лимит API: {e}, пробую снова...")
            raise RateLimitError(msg)
        elif "deadline exceeded" in msg or "timeout" in msg or "connection" in msg:
            print(f"Таймаут/ошибка соединения: {e}, пробую снова...")
            raise TimeoutError(msg)
        else:
            print(f"Неизвестная ошибка: {e}")
            raise


if __name__ == "__main__":
    try:
        result = safe_generate("Why? just why?")
        resp = result.candidates[0].content.parts[0].text
        for fragment in textwrap.wrap(resp, width=80):
            print(fragment)

    except Exception as e:
        print("Ошибка после всех попыток:", repr(e))
