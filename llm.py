import logging
from typing import Optional

from func import truncate_history
from settings import h4x0r_settings
import google.generativeai as genai
from google.generativeai.generative_models import ChatSession
import crud, schemas


def get_instructions() -> str | None:

    instructions = None

    try:
        with open("instructions.md", "r") as instructions_file:
            instructions = instructions_file.read()

    except Exception as e:
        logging.error(f"An error occurred while reading H4X-0R instrucions: {e}")

    finally:
        return instructions


genai.configure(api_key=h4x0r_settings.SECRET_GOOGLE_API)

model = genai.GenerativeModel(model_name=h4x0r_settings.LLM_NAME)


async def get_chat_session(chat_id: int) -> ChatSession:

    history = await crud.get_chat_history(chat_id)

    if history:
        chat = model.start_chat(history=history)
    else:
        chat = await create_new_chat(chat_id=chat_id)

    return chat


async def create_new_chat(chat_id: int) -> ChatSession:

    instructions = get_instructions()

    chat = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    instructions,
                ],
            }
        ]
    )

    await crud.create_chat(
        schemas.Chat(
            id=chat_id,
        )
    )

    return chat


async def respond_on_message(message: list, chat_object: ChatSession) -> str:
    try:
        response = await chat_object.send_message_async(content=message)

        if len(message) > 1:
            chat_object.history.pop(-2)

        truncate_history(chat_object)

        return response.text

    except Exception as e:
        logging.error(f"Error during chat interaction: {e}")
        return "Couldn't generate an answer. Please try again"
