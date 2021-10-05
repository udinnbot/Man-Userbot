# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot start point """

import sys
from importlib import import_module

from telethon.errors.rpcerrorlist import PhoneNumberInvalidError

from userbot import ALIVE_NAME, ALIVE_LOGO, BOT_VER, BOTLOG_CHATID, LOGS, UPSTREAM_REPO_BRANCH, bot
from userbot.modules import ALL_MODULES

MAN_PIC = ALIVE_LOGO or "https://telegra.ph/file/9dc4e335feaaf6a214818.jpg"

INVALID_PH = (
    "\nERROR: Nomor Telepon yang kamu masukkan SALAH."
    "\nTips: Gunakan Kode Negara beserta nomornya atau periksa nomor telepon Anda dan coba lagi."
)

try:
    bot.start()
except PhoneNumberInvalidError:
    print(INVALID_PH)
    sys.exit(1)

for module_name in ALL_MODULES:
    imported_module = import_module("userbot.modules." + module_name)

LOGS.info(
    f"Jika {ALIVE_NAME} Membutuhkan Bantuan, Silahkan Gabung ke Grup https://t.me/SharingUserbot")

LOGS.info(
    f"Man-Userbot ⚙️ V{BOT_VER} [🔥 BERHASIL DIAKTIFKAN! 🔥]")

# that's life...
async def man_userbot_on():
    try:
        if BOTLOG_CHATID != 0:
            await bot.send_file(
                BOTLOG_CHATID,
                MAN_PIC,
                caption=f"🔥 **Man-Userbot Berhasil Di Aktifkan**\n\n**➥ Userbot Version -** `{BOT_VER}`@`{UPSTREAM_REPO_BRANCH}`\n\n➥ **Ketik** `.ping` **atau** `.alive` **untuk Check BOT**\n➥ **Join @SharingUserbot Untuk Bantuan BOT**",
            )
    except Exception as e:
        LOGS.info(str(e))


# Join Channel
    try:
        await bot(JoinChannelRequest("@Lunatic0de"))
    except BaseException:
        pass


bot.loop.create_task(man_userbot_on())

if len(sys.argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.run_until_disconnected()
