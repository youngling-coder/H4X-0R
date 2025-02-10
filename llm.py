import logging
import sys
from typing import Optional

from func import truncate_history
from settings import h4x0r_settings
import google.generativeai as genai
from google.generativeai.generative_models import ChatSession

from dump_file import write_dump_file, read_dump_file

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


def get_chat(title: str) -> Optional[ChatSession]:
    try:
        history = read_dump_file(title)
        if history:
            chat = model.start_chat(history=history)

            return chat
    except Exception as e:
        logging.error(f"Couldn't read chat object with title {title}: {e}")

    return


def create_new_chat(title: str, type_: str, participants: dict) -> ChatSession:

    instructions = get_instructions()
    instructions += f"""
### This chat type is a: {type_}
### This chat is with users: {", ".join([username for username in participants.keys()])}
### You should call him/her: {", ".join([participants[username] for username in participants.keys()])}
(If the user's full name is not provided, you can but NOT required to politely ask for user's name)
"""
    

    chat = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    instructions,
                ],
            },
            {
                "role": "model",
                "parts": [
                    "I got you!",
                ],
            },
        ]
    )

    write_dump_file(title, chat.history)

    return chat


async def respond_on_message(
    message: list, chat_name: str, chat_object: ChatSession
) -> str:
    try:
        response = await chat_object.send_message_async(content=message)

        if len(message) > 1:
            chat_object.history.pop(-2)
        
        truncate_history(chat_object)
        
        write_dump_file(chat_name, chat_object.history)
        return f"🤖: {response.text}"

    except Exception as e:
        logging.error(f"Error during chat interaction: {e}")
        return "Couldn't generate an answer. Please try again"
