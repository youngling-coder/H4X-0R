import pickle
import os
from settings import h4x0r_settings
from llm import get_instructions
from google.ai.generativelanguage_v1beta.types.content import Content, Part


instructions_obj = Content({"role": "user", "parts": [Part(text=get_instructions())]})


def update_instructions():
    try:
        for pickle_file in os.listdir(h4x0r_settings.DUMP_FILES_PATH):

            obj = None
            full_path = os.path.join(h4x0r_settings.DUMP_FILES_PATH, pickle_file)

            with open(full_path, "rb") as f:
                obj = pickle.load(f)

            with open(full_path, "wb") as f:
                obj.pop(0)
                obj.insert(0, instructions_obj)
                pickle.dump(obj, f)

    except Exception as e:
        print(f"Error: {e}")

    else:
        print("Done!")


update_instructions()
