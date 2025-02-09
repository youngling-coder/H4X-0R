import google.generativeai as genai
from dotenv import load_dotenv
import os


load_dotenv(".env")


try:
    with open("instructions.md", "r") as instructions_file:
        INSTRUCTIONS = instructions_file.read()

except Exception as e:
    print(f"An error occurred while reading H4X-0R instrucions: {e}")


genai.configure(api_key=os.getenv("GOOGLE_API"))


model = genai.GenerativeModel(model_name="gemini-2.0-flash")
chat = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [
                INSTRUCTIONS,
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


async def respond_on_message(message: str) -> str:
    try:
        response = await chat.send_message_async(content=message)
        return response.text
    except Exception as e:
        print(f"Error during chat interaction: {e}")
        return "Couldn't generate an answer. Please try again"
