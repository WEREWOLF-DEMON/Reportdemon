import os
import sys
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from info import Config, Txt


@Client.on_message(filters.private & filters.command('start'))
async def handle_start(bot:Client, message:Message):

    Btn = [
        [InlineKeyboardButton(text='¢м∂ѕ', callback_data='help'), InlineKeyboardButton(text='ѕєяνєя-¢нαтѕ', callback_data='server')],
        [InlineKeyboardButton(text='¢нαηηєℓ', url='https://t.me/thecchub'), InlineKeyboardButton(text='вσт-αвσυт', callback_data='about')],
        [InlineKeyboardButton(text='σωηєя', url='https://t.me/its_Aryaan')]
        ]

    await message.reply_text(text=Txt.START_MSG.format(message.from_user.mention), reply_markup=InlineKeyboardMarkup(Btn))


#Restart to cancell all process 
@Client.on_message(filters.private & filters.command("restart") & filters.user(Config.SUDO))
async def restart_bot(b, m):
    await m.reply_text("яєѕтαятιη.....__")
    os.execl(sys.executable, sys.executable, *sys.argv)
