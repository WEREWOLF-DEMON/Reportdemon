import json
import os
import subprocess
from pathlib import Path
import sys
from pyrogram import Client, filters
from pyrogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from pyrogram.errors import MessageIdInvalid
from info import Config, Txt


config_path = Path(__file__).parent / "config.json"


async def Report_Function(No):

    listofchoise = ['Report child abuse', 'Report copyrighted content', 'Report impersonation', 'Report irrelevant geogroup',
                    'Report illegal durg', 'Report Violence', 'Report for personal detail', 'Reason Pornography', 'Report spam"']
    message = listofchoise[int(No) - 1]

    # Run a shell command and capture its output
    process = subprocess.Popen(
        ["python", f"report.py",
            f"{message}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Use communicate() to interact with the process
    stdout, stderr = process.communicate()

    # Get the return code
    return_code = process.wait()

    # Check the return code to see if the command was successful
    if return_code == 0:
        # Print the output of the command
        print("Command output:")
        print(stdout)
        return [stdout, True]

    else:
        # Print the error message if the command failed
        print("Command failed with error:")
        print(stderr)
        return f"<b>ѕσмєтнιηg ωєηт ωяσηg кιη∂ℓу ¢нє¢к уσυя ιηρυтѕ ωнєтнєя уσυ нανє ƒιℓℓє∂ ¢σяяє¢тℓу σя ησт !</b>\n\n <code> {stderr} </code> \n ERROR"


async def CHOICE_OPTION(bot, msg, number):

    if not config_path.exists():
        return await msg.reply_text(text="**уσυ ∂ση'т нανє αηу ¢σηƒιg ƒιяѕт мαкє тнє ¢σηƒιg тнєη уσυ'ℓℓ αвℓє тσ яєρσят**\n\n υѕє /config", reply_to_message_id=msg.id, reply_markup=ReplyKeyboardRemove())

    with open(config_path, 'r', encoding='utf-8') as file:
        config = json.load(file)

    try:
        if Path('report.txt').exists():
            return await msg.reply_text(text="**αℓяєα∂у σηє ρяσ¢єѕѕ ιѕ σηgσιηg ρℓєαѕє ωαιт υηтιℓ ιт'ѕ ƒιηιѕнє∂**", reply_to_message_id=msg.id)

        no_of_reports = await bot.ask(text=Txt.SEND_NO_OF_REPORT_MSG.format(config['Target']), chat_id=msg.chat.id, filters=filters.text, timeout=30, reply_markup=ReplyKeyboardRemove())
    except:
        await bot.send_message(msg.from_user.id, "єяяσя!!\n\nяєqυєѕт тιмє∂ συт.\nяєѕтαят ρℓєαѕє υѕє ¢м∂ → /report")
        return

    ms = await bot.send_message(chat_id=msg.chat.id, text=f"**ρℓєαѕє ωαιт**\n\nнανє ραтιєη¢є", reply_to_message_id=msg.id, reply_markup=ReplyKeyboardRemove())
    if str(no_of_reports.text).isnumeric():

        try:
            i = 0
            while i < int(no_of_reports.text):
                result = await Report_Function(number)

                if result[1]:
                    # Assuming output is a bytes object
                    output_bytes = result[0]
                    # Decode bytes to string and replace "\r\n" with newlines
                    output_string = output_bytes.decode(
                        'utf-8').replace('\r\n', '\n')

                    with open('report.txt', 'a+') as file:
                        file.write(output_string)

                    i += 1
                    continue

                else:
                    await bot.send_message(chat_id=msg.chat.id, text=f"{result}", reply_to_message_id=msg.id)
        except Exception as e:
            print('Error on line {}'.format(
                sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
            return await msg.reply_text(text=f"**{e}**\n\n ERROR !")

    else:
        await msg.reply_text(text='**ρℓєαѕє єηтєя ναℓι∂ ιηтєgєя ηυмвєя !**\n\n тяу αgαιη :- /report')
        return

    await ms.delete()
    await msg.reply_text(text=f"вσт ѕυ¢¢єѕѕƒυℓℓу яєρσятє∂ тσ @{config['Target']} 😪\n\n{no_of_reports.text} Times")
    file = open('report.txt', 'a')
    file.write(
        f"\n\n@{config['Target']} ¢нαηηєℓ σя gяσυρ ιѕ яєρσятє∂ {no_of_reports.text} тιмєѕ 😪")
    file.close()
    await bot.send_document(chat_id=msg.chat.id, document='report.txt', reply_to_message_id=msg.id)
    os.remove('report.txt')


@Client.on_message(filters.private & filters.user(Config.OWNER) & filters.command('report'))
async def handle_report(bot: Client, cmd: Message):

    CHOICE = [
        [("1"), ("2")], [("3"), ("4")], [("5"), ("6")], [("7"), ("8")], [("9")]
    ]

    await bot.send_message(chat_id=cmd.from_user.id, text=Txt.REPORT_CHOICE, reply_to_message_id=cmd.id, reply_markup=ReplyKeyboardMarkup(CHOICE, resize_keyboard=True))


@Client.on_message(filters.regex("1"))
async def one(bot: Client, msg: Message):

    await CHOICE_OPTION(bot, msg, 1)


@Client.on_message(filters.regex("2"))
async def two(bot: Client, msg: Message):
    await CHOICE_OPTION(bot, msg, 2)


@Client.on_message(filters.regex("3"))
async def three(bot: Client, msg: Message):
    await CHOICE_OPTION(bot, msg, 3)


@Client.on_message(filters.regex("4"))
async def four(bot: Client, msg: Message):
    await CHOICE_OPTION(bot, msg, 4)


@Client.on_message(filters.regex("5"))
async def five(bot: Client, msg: Message):
    await CHOICE_OPTION(bot, msg, 5)


@Client.on_message(filters.regex("6"))
async def six(bot: Client, msg: Message):
    await CHOICE_OPTION(bot, msg, 6)


@Client.on_message(filters.regex("7"))
async def seven(bot: Client, msg: Message):
    await CHOICE_OPTION(bot, msg, 7)


@Client.on_message(filters.regex("8"))
async def eight(bot: Client, msg: Message):
    await CHOICE_OPTION(bot, msg, 8)


@Client.on_message(filters.regex("9"))
async def nine(bot: Client, msg: Message):
    await CHOICE_OPTION(bot, msg, 9)
