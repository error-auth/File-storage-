from pyrogram import __version__
from bot import Bot
from config import OWNER_ID
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "about":
        await query.message.edit_text(
            text=(
                "┏━━━━━━━━━━━━━━━━━┓\n"
                "ㅤㅤ   ㅤ  [sᴛᴇʀɴʀɪᴛᴛᴇʀ](https://t.me/official_str)ㅤㅤㅤㅤㅤ\n"
                "┗━━━━━━━━━━━━━━━━━┛\n\n"
                "╔──────\n"
                "╟ Owner: [Aryan Kadam](https://t.me/aryan_kadam)\n"
                "╚──────\n"
                "╔──────\n"
                "╟ [Anime Plaza STR](https://t.me/animeplaza_str)\n"
                "╚──────\n"
                "╔──────\n"
                "╟ [Ongoing Anime](https://t.me/ongoing_str)\n"
                "╚──────\n"
                "╔──────\n"
                "╟ Dev: [ɢӈߋʂτ](https://t.me/corpsealone)\n"
                "╚──────"
            ),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Join Anime Plaza", url='https://t.me/animeplaza_str')],
                    [InlineKeyboardButton("Join our group chat", url='https://t.me/OtakusMotel_STR')],
                    [InlineKeyboardButton("🔒 Close", callback_data="close")]
                ]
            ),
            parse_mode='Markdown'
        )
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
