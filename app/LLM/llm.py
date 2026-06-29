import os
import os

from functools import lru_cache

from dotenv import load_dotenv
from google import genai

from app.utils.logger import logger

load_dotenv()


@lru_cache(maxsize=1)
def get_llm():

    logger.info("Initializing Gemini client...")

    return genai.Client(
        api_key=os.getenv("GEMINI_API_KEY")
    )


def generate_response(prompt: str):

    client = get_llm()

    logger.info("Sending request to Gemini...")

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    logger.info("Received response from Gemini")

    return response.text

