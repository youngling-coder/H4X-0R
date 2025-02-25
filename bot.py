import asyncio

from aiogram import Router, Bot
from aiogram import types
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties
import yt_dlp
from youtubesearchpython import VideosSearch

from func import escape_markdown, photo_to_pil_object
from settings import h4x0r_settings
from llm import respond_on_message, create_new_chat, get_chat


H4X0R_bot = Bot(
    token=h4x0r_settings.TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN),
)

router = Router()


async def run_blocking(coro):
    return await asyncio.to_thread(coro)


@router.callback_query()
async def download_selected_music(query: types.CallbackQuery):
    link = query.data
    msg_filler = await query.message.answer("🤖 Downloading ...")

    def sync_download():
        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
            "cookiefile": "cookies.txt",
            "outtmpl": f"{h4x0r_settings.MUSIC_FOLDER}/%(title)s.%(ext)s",
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(link, download=True)

    try:
        info = await run_blocking(sync_download)
        filename = info["requested_downloads"][0]["filepath"]
        audio = types.FSInputFile(filename)
        await query.message.answer_audio(audio=audio, caption="✨ _[Hector Music](https://t.me/h4x0r\\_hector\\_music\\_bot)_ ✨", parse_mode=ParseMode.MARKDOWN_V2)

    except Exception as e:
        await query.message.answer(f"❌ An error occurred while downloading!")
        print(e)
    finally:
        await query.message.chat.delete_message(msg_filler.message_id)


@router.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:

    username = (
        message.from_user.username
        if message.from_user.username
        else message.from_user.id
    )
    full_name = f"{message.chat.first_name} {message.chat.last_name}"

    if username == h4x0r_settings.OWNER_USERNAME:
        chat = get_chat(title=username)

        if not chat:
            chat = create_new_chat(title=username)

        response = await respond_on_message(
            message="Introduce yourself to your owner in a brief form and tell about yourself.",
            chat_name=username,
            chat_object=chat,
        )

        await message.reply(
            escape_markdown(response),
            parse_mode=ParseMode.MARKDOWN,
        )


@router.message(lambda message: message.text if not message.text else message.text.lower().startswith("music"))
async def music_handler(message: types.Message):

    query = message.text.lower().replace("music", "").lstrip()

    if query:

        search = VideosSearch(query, limit=10)
        results = search.result()

        if not results:
            await message.reply("❌ Music not found!")
            return
        
        results = results["result"]

        tracklist_markup = types.InlineKeyboardMarkup(inline_keyboard=[[]])

        for audio in results:
            tracklist_markup.inline_keyboard.append([types.InlineKeyboardButton(text=audio["title"], callback_data=audio["link"])])


        await message.reply("✅ Search results:", reply_markup=tracklist_markup)


@router.message()
async def message_handler(message: types.Message) -> None:

    is_content_appropriate = lambda message: message.text or message.caption or message.photo
    is_group = lambda message: message.chat.type in ("group", "supergroup")
    is_activated = lambda message:  message and list(filter(lambda x: message.lower().startswith(x), 
                                               ("hector", "гектор", "железяка", "байтоголовый", "битоголовый", "бот")))

    print(is_activated(message.caption), is_activated(message.text))

    if is_content_appropriate(message) and is_group(message) and \
    (is_activated(message.caption) or is_activated(message.text)):
        
        title = message.chat.id
        chat = get_chat(title=title)

        if not chat:

            chat = create_new_chat(title=title)

        final_message = [
            f"message by: {message.from_user.username} ({message.from_user.first_name} {message.from_user.last_name})\n\n"
        ]

        if message.photo:
            if message.caption:
                final_message[0] += message.caption
            image = await photo_to_pil_object(message.photo[-1])

            final_message.append(image)

        else:
            final_message[0] += message.text

        response = await respond_on_message(
            message=final_message, chat_name=str(message.chat.id), chat_object=chat
        )

        await message.reply(
            escape_markdown(response)
        )
