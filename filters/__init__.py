from aiogram.filters import Filter
from aiogram import types
from blacklist import BLACKLIST_TELEGRAM_IDS


class WhoIsFilter(Filter):
    entries = ("гектор кто", "гектор кого")
    
    @staticmethod
    def delete_entries(text: str):
        for entry in WhoIsFilter.entries:
            text = text.replace(entry, "")

        return text
    

    async def __call__(self, message: types.Message) -> bool:

        if message.text:

            for entry in self.entries:

                if message.text.lower().startswith(entry):
                    return True

        elif message.caption:

            for entry in self.entries:

                if message.caption.lower().startswith(entry):
                    return True

        return False


class BlackListFilter(Filter):
    async def __call__(self, message: types.Message) -> bool:

        return message.from_user.id not in BLACKLIST_TELEGRAM_IDS