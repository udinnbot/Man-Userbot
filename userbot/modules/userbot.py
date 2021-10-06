# Copyright (C) 2021 KenHV
# Ported by @mrismanaziz
# FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de

from sqlalchemy.exc import IntegrityError

from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern=r"^\.userbotoff (.*)")
async def _(event):
    """Adds given chat to blacklist."""
    try:
        from userbot.modules.sql_helper.nouserbot_sql import add_nouserbot
    except IntegrityError:
        return await event.edit("**Running on Non-SQL mode!**")

    try:
        chat_id = int(event.pattern_match.group(1))
    except ValueError:
        chat_id = event.pattern_match.group(1)

    try:
        chat_id = await event.client.get_peer_id(chat_id)
    except Exception:
        return await event.edit("**ERROR: Username/ID yang diberikan Tidak Valid.**")

    try:
        add_nouserbot(str(chat_id))
    except IntegrityError:
        return await event.edit(
            "**Obrolan yang diberikan sudah masuk ke list tanpa userbot.**"
        )

    await event.edit("**Blacklisted given chat!**")


@register(outgoing=True, pattern=r"^\.userboton (.*)")
async def _(event):
    """Unblacklists given chat."""
    try:
        from userbot.modules.sql_helper.nouserbot_sql import (
            del_nouserbot,
            get_nouserbot,
        )
    except IntegrityError:
        return await event.edit("**Running on Non-SQL mode!**")

    chat_id = event.pattern_match.group(1)
    try:
        chat_id = str(await event.client.get_peer_id(chat_id))
    except Exception:
        pass

    if chat_id == "all":
        from userbot.modules.sql_helper.nouserbot_sql import del_nouserbot_all

        del_nouserbot_all()
        return await event.edit("**Menghapus Semua Userbot Yang diMatikan**")

    id_exists = False
    for i in get_nouserbot():
        if chat_id == i.chat_id:
            id_exists = True

    if not id_exists:
        return await event.edit("**Obrolan ini tidak masuk list tanpa userbot.**")

    del_nouserbot(chat_id)
    await event.edit("**Obrolan yang diberikan tidak masuk list tanpa userbot**")


@register(outgoing=True, pattern=r"^\.nouserbotlist$")
async def _(event):
    try:
        from userbot.modules.sql_helper.nouserbot_sql import get_nouserbot
    except IntegrityError:
        return await event.edit("**Running on Non-SQL mode!**")

    chat_list = get_nouserbot()
    if not chat_list:
        return await event.edit(
            "**Anda belum memasukkan obrolan apa pun ke tanpa userbot!**"
        )

    msg = "**List Userbot diMatikan diObrolan:**\n\n"

    for i in chat_list:
        try:
            chat = await event.client.get_entity(int(i.chat_id))
            chat = f"{chat.title} | `{i.chat_id}`"
        except (TypeError, ValueError):
            chat = f"__Tidak Dapat Mengambil info Obrolan__ | `{i.chat_id}`"

        msg += f"• {chat}\n"

    await event.edit(msg)


CMD_HELP.update(
    {
        "userbot": "**Plugin : **`userbot`\
        \n\n  •  **Syntax :** `.userbotoff` <username/id>\
        \n  •  **Function : **Untuk Mematikan userbot di obrolan yang diberikan.\
        \n\n  •  **Syntax :** `.userboton` <username/id>\
        \n  •  **Function : **Untuk Menghapus Dari Daftar Userbot Yang diMematikan.\
        \n\n  •  **Syntax :** `.userbotoff` all\
        \n  •  **Function : **Untuk Menghapus Semua Userbot Yang diMematikan.\
        \n\n  •  **Syntax :** `.unouserbotlist`\
        \n  •  **Function : **Untuk Menampilkan List dimana saja Userbot yang kita Matikan.\
    "
    }
)
