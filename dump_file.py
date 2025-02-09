import os
import pickle
import logging
from typing import Any

from settings import h4x0r_settings


def read_dump_file(filename: str):

    filename = f"{filename}.pkl"
    dump_file_path = os.path.join(h4x0r_settings.DUMP_FILES_PATH, filename)

    if os.path.exists(dump_file_path):
        with open(dump_file_path, "rb") as chat_file:
            obj = pickle.load(chat_file)
            return obj

    return


def write_dump_file(filename: str, obj: Any) -> None:

    dump_files_folder_exists = os.path.exists(h4x0r_settings.DUMP_FILES_PATH)

    if not dump_files_folder_exists:
        try:
            os.mkdir(h4x0r_settings.DUMP_FILES_PATH)
            dump_files_folder_exists = True

        except Exception as e:
            logging.error(f"Couldn't initialize H4X-0R_CHATS folder: {e}")

    if dump_files_folder_exists:
        filename = f"{filename}.pkl"
        dump_file_path = os.path.join(h4x0r_settings.DUMP_FILES_PATH, filename)

        try:
            with open(dump_file_path, "wb") as chat_file:
                pickle.dump(obj, chat_file)
        except Exception as e:
            logging.error(f"Couldn't create/update {filename} dump file: {e}")
