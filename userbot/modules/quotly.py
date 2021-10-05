import random
from asyncio.exceptions import TimeoutError

import requests
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import CMD_HELP, bot
from userbot.events import register


@register(outgoing=True, pattern=r"^\.q")
async def quotess(qotli):
    if qotli.fwd_from:
        return
    if not qotli.reply_to_msg_id:
        return await qotli.edit("```Mohon Balas Ke Pesan```")
    reply_message = await qotli.get_reply_message()
    if not reply_message.text:
        return await qotli.edit("```Mohon Balas Ke Pesan```")
    chat = "@QuotLyBot"
    if reply_message.sender.bot:
        return await qotli.edit("```Mohon Balas Ke Pesan```")
    await qotli.edit("```Sedang Memproses Sticker, Mohon Menunggu```")
    try:
        async with bot.conversation(chat) as conv:
            try:
                response = conv.wait_event(
                    events.NewMessage(incoming=True, from_users=1031952739)
                )
                msg = await bot.forward_messages(chat, reply_message)
                response = await response
                """ - don't spam notif - """
                await bot.send_read_acknowledge(conv.chat_id)
            except YouBlockedUserError:
                return await qotli.reply(
                    "**Harap Jangan Blockir** @QuotLyBot **Buka Blokir Lalu Coba Lagi**"
                )
            if response.text.startswith("Hi!"):
                await qotli.edit(
                    "**Mohon Menonaktifkan Pengaturan Privasi Forward Anda**"
                )
            else:
                await qotli.delete()
                await bot.forward_messages(qotli.chat_id, response.message)
                await bot.send_read_acknowledge(qotli.chat_id)
                """ - cleanup chat after completed - """
                await qotli.client.delete_messages(conv.chat_id, [msg.id, response.id])
    except TimeoutError:
        await qotli.edit()


CMD_HELP.update(
    {
        "quotly": "**Plugin : **`quotly`\
        \n\n  •  **Syntax :** `.q`\
        \n  •  **Function : **Membuat pesan mu menjadi sticker.\
    "
    }
)
