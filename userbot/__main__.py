import glob
import sys
from pathlib import Path

import telethon.utils
from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest

from userbot import ALIVE_NAME, ALIVE_LOGO, API_KEY, API_HASH, BOT_TOKEN, BOT_USERNAME, BOT_VER, BOTLOG_CHATID, LOGS, UPSTREAM_REPO_BRANCH, bot, tgbot
MAN_PIC = ALIVE_LOGO or "https://telegra.ph/file/9dc4e335feaaf6a214818.jpg"


# let's get the bot ready
async def manuserbot(bot_token):
    try:
        await bot.start(bot_token)
        bot.me = await bot.get_me()
        bot.uid = telethon.utils.get_peer_id(bot.me)
    except Exception as e:
        LOGS.error(f"STRING_SESSION - {str(e)}")
        sys.exit()


# Man-Userbot Starter
if len(sys.argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.tgbot = None
    try:
        if BOT_USERNAME is not None:
            LOGS.info("Sedang Memeriksa BOT_USERNAME")
            bot.tgbot = TelegramClient(
                "BOT_TOKEN", api_id=API_KEY, api_hash=API_HASH
            ).start(bot_token=BOT_TOKEN)
            LOGS.info("Pemeriksaan Selesai. Melanjutkan ke Langkah berikutnya")
            LOGS.info("🔰 Starting Man-UserBot 🔰")
            bot.loop.run_until_complete(manuserbot(BOT_USERNAME))
        else:
            bot.start()
    except Exception as e:
        LOGS.error(f"BOT_TOKEN - {str(e)}")
        sys.exit()


# let the party begin...
LOGS.info("Starting Bot Mode !")
tgbot.start()
LOGS.info(
    f"Jika {ALIVE_NAME} Membutuhkan Bantuan, Silahkan Gabung ke Grup https://t.me/SharingUserbot")
LOGS.info(
    f"Man-Userbot ⚙️ V{BOT_VER} [🔥 BERHASIL DIAKTIFKAN! 🔥]")


# that's life...
async def man_is_on():
    try:
        if BOTLOG_CHATID != 0:
            await bot.send_file(
                BOTLOG_CHATID,
                MAN_PIC,
                caption=f"🔥 **Man-Userbot Berhasil Di Aktifkan**\n\n**➥ Userbot Version -** `{BOT_VER}`@`{UPSTREAM_REPO_BRANCH}`\n➥ **Ketik** `.ping` **atau** `.alive` **untuk Check BOT**\n➥ **Join @SharingUserbot Untuk Bantuan BOT**",
            )
    except Exception as e:
        LOGS.info(str(e))


# Join Channel after deploying 🤐😅
    try:
        await bot(JoinChannelRequest("@Lunatic0de"))
    except BaseException:
        pass


bot.loop.create_task(man_is_on())

if len(sys.argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.tgbot = None
    bot.run_until_disconnected()
