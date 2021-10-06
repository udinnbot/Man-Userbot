import asyncio

from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

import userbot.modules.sql_helper.antiflood_sql as sql
from userbot import CMD_HELP
from userbot.events import register
from userbot.utils.tools import is_admin

CHAT_FLOOD = sql.__load_flood_settings()
# warn mode for anti flood
ANTI_FLOOD_WARN_MODE = ChatBannedRights(
    until_date=None, view_messages=None, send_messages=True
)


@register(incoming=True, disable_edited=True, disable_errors=True)
async def _(event):
    if not CHAT_FLOOD:
        return
    admin_c = await is_admin(event.client, event.chat_id, event.client.uid)
    if not admin_c:
        return
    if str(event.chat_id) not in CHAT_FLOOD:
        return
    should_ban = sql.update_flood(event.chat_id, event.message.sender_id)
    if not should_ban:
        return
    try:
        await event.client(
            EditBannedRequest(
                event.chat_id, event.message.sender_id, ANTI_FLOOD_WARN_MODE
            )
        )
    except Exception as e:
        no_admin_privilege_message = await event.client.send_message(
            entity=event.chat_id,
            message=f"**Automatic AntiFlooder**\x1f[Jamet](tg://user?id={event.message.sender_id}) Membanjiri obrolan.\x1f`{e}`",
            reply_to=event.message.id,
        )

        await asyncio.sleep(4)
        await no_admin_privilege_message.edit(
            "**Ini SPAM tidak berguna kawan. Hentikan ini, Mari kita parming**"
        )
    else:
        await event.client.send_message(
            entity=event.chat_id,
            message=f"""**Automatic AntiFlooder**
[User](tg://user?id={event.message.sender_id}) Membanjiri obrolan.
**Aksi:** Saya membisukan dia""",
            reply_to=event.message.id,
        )


@register(outgoing=True, pattern=r"^\.setflood(?:\s|$)([\s\S]*)")
async def _(event):
    input_str = event.pattern_match.group(1)
    event = await event.edit("`Processing...`")
    await asyncio.sleep(2)
    try:
        sql.set_flood(event.chat_id, input_str)
        sql.__load_flood_settings()
        await event.edit(
            f"**Antiflood diperbarui menjadi** `{input_str}` **dalam obrolan saat ini**"
        )
    except Exception as e:
        await event.edit(str(e))


CMD_HELP.update(
    {
        "antiflood": "**Plugin : **`antiflood`\
        \n\n  •  **Syntax :** `.setflood` [jumlah pesan]\
        \n  •  **Function : **memperingatkan pengguna jika dia melakukan spam pada obrolan dan jika Anda adalah admin maka itu akan membisukan dia dalam grup itu.\
        \n\n  •  **NOTE :** Untuk mematikan setflood, atur jumlah pesan menjadi 0 » `.setflood 0`\
    "
    }
)
