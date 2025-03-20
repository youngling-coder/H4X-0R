import logging
import sys

from ruaccent import RUAccent
from TeraTTS import TTS

from settings import h4x0r_settings


def setup_ruaccent():
    accentizer = RUAccent()
    accentizer.load(
        omograph_model_size="turbo3.1",
        use_dictionary=True,
        workdir=h4x0r_settings.SECRET_RUACCENT_MODEL_FOLDER,
    )

    return accentizer


def setup_model():
    try:
        tts = TTS(
            "TeraTTS/glados2-g2p-vits",
            save_path=h4x0r_settings.SECRET_TTS_MODEL_FOLDER,
            add_time_to_end=0,
            tokenizer_load_dict=False,
        )

        return tts

    except Exception as e:
        logging.error(f"An error occurred while model downloading: {e}")
        sys.exit()


tts_model = setup_model()
accentizer = setup_ruaccent()
