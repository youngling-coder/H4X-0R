import logging
from typing import Optional

from func import truncate_history
from settings import h4x0r_settings
import google.generativeai as genai
from google.generativeai.generative_models import ChatSession
import crud


def get_instructions() -> str | None:

    instructions = None

    try:
        with open("instructions.md", "r") as instructions_file:
            instructions = instructions_file.read()

    except Exception as e:
        logging.error(f"An error occurred while reading H4X-0R instrucions: {e}")

    finally:
        return instructions


genai.configure(api_key=h4x0r_settings.GOOGLE_API)

model = genai.GenerativeModel(model_name=h4x0r_settings.LLM_NAME)


def get_chat(chat_id: str) -> Optional[ChatSession]:
    try:
        history = crud.get_chat_history(chat_id)

        if history:
            chat = model.start_chat(history=history)

            return chat
    except Exception as e:
        logging.error(f"Couldn't read chat object with title {chat_id}: {e}")

    return


def create_new_chat(chat_id: str) -> ChatSession:

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

    crud.create_chat(chat_id=chat_id)
    crud.create_message(chat_id=chat_id, content=instructions, role="user")

    return chat


async def respond_on_message(
    message: list, chat_id: str, chat_object: ChatSession
) -> str:
    try:
        response = await chat_object.send_message_async(content=message)

        if len(message) > 1:
            chat_object.history.pop(-2)

        truncate_history(chat_object)

        crud.create_message(chat_id, content=message[0], role="user")
        crud.create_message(chat_id, content=response.text, role="model")

        return response.text

    except Exception as e:
        logging.error(f"Error during chat interaction: {e}")
        return "Couldn't generate an answer. Please try again"
