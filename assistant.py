from telethon import TelegramClient, events

from settings import h4x0r_settings
from llm import respond_on_message, get_chat, create_new_chat

client = TelegramClient("session", h4x0r_settings.APP_ID, h4x0r_settings.API_HASH)


@client.on(events.NewMessage(incoming=True))
async def handle_new_message(event):
    sender = await event.get_sender()

    if h4x0r_settings.IS_ENABLED:

        if event.is_private and (not event.sender.bot):

            username = sender.username if sender.username else sender.id
            full_name = f"{sender.first_name} {sender.last_name}"

            chat = get_chat(title=event.chat_id)

            if not chat:
                me = await client.get_me()
                me_full_name = f"{me.first_name} {me.last_name}"
                chat = create_new_chat(
                    title=event.chat_id,
                    type_="private",
                    participants={
                        me.username if me.username else me.id: me_full_name,
                        username: full_name,
                    },
                )

            message = event.raw_text

            response = await respond_on_message(
                message=message, chat_name=event.chat_id, chat_object=chat
            )

            await client.send_message(username, response, parse_mode="md")

            await client.send_read_acknowledge(
                event.chat_id, clear_mentions=True, clear_reactions=True
            )
