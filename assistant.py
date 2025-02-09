from telethon import TelegramClient, events

from settings import h4x0r_settings
from llm import respond_on_message


client = TelegramClient("session", h4x0r_settings.APP_ID, h4x0r_settings.API_HASH)


@client.on(events.NewMessage(incoming=True))
async def handle_new_message(event):

    sender = await event.get_sender()
    username = sender.username

    if h4x0r_settings.IS_ENABLED:

        if event.is_private and (not event.sender.bot):

            message = f"Message from: {sender.first_name} {sender.last_name}\n\n" + event.raw_text

            response = await respond_on_message(message=message)

            await client.send_message(username, response, parse_mode="md")

            await client.send_read_acknowledge(
                event.chat_id, clear_mentions=True, clear_reactions=True
            )
