import json
from pathlib import Path
import subprocess
import sys
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from info import Config, Txt

config_path = Path(__file__).parent / "config.json"


@Client.on_message(filters.private & filters.user(Config.SUDO) & filters.command('add_account'))
async def add_account(bot: Client, cmd: Message):
    try:
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as file:
                config = json.load(file)

        else:
            return await cmd.reply_text(text="уσυ ∂ι∂η'т мαкє α ¢σηƒιg уєт !\n\n ƒιяѕтℓу мαкє ¢σηƒιg ву υѕιηg /config", reply_to_message_id=cmd.id)

        try:
            session = await bot.ask(text=Txt.SEND_SESSION_MSG, chat_id=cmd.chat.id, filters=filters.text, timeout=60)
        except:
            await bot.send_message(cmd.from_user.id, "єяяσя!!\n\nяєqυєѕт тιмє∂ συт.\nяєѕтαят ву υѕιηg /config", reply_to_message_id=session.id)
            return

        ms = await cmd.reply_text('**ρℓєαѕє ωαιт...**', reply_to_message_id=cmd.id)

        for acocunt in config['accounts']:
            if acocunt['Session_String'] == session.text:
                return await ms.edit(text=f"**{acocunt['OwnerName']} α¢¢συηт αℓяєα∂у єχιѕт ιη ¢σηƒιg уσυ ¢αη'т α∂∂ ѕαмє α¢¢συηт мυℓтιρℓє тιмєѕ **\n\n Error !")

        with open(config_path, 'r', encoding='utf-8') as file:
            config = json.load(file)

         # Run a shell command and capture its output
        try:

            process = subprocess.Popen(
                ["python", f"login.py",
                    f"{config['Target']}", f"{session.text}"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except Exception as err:
            await bot.send_message(cmd.chat.id, text=f"<b>єяяσя :</b>\n<pre>{err}</pre>")

        # Use communicate() to interact with the process
        stdout, stderr = process.communicate()

        # Get the return code
        return_code = process.wait()

        # Check the return code to see if the command was successful
        if return_code == 0:
            # Print the output of the command
            print("Command output:")
            # Assuming output is a bytes object
            output_bytes = stdout
            # Decode bytes to string and replace "\r\n" with newlines
            output_string = output_bytes.decode('utf-8').replace('\r\n', '\n')
            print(output_string)
            AccountHolder = json.loads(output_string)

        else:
            # Print the error message if the command failed
            print("Command failed with error:")
            print(stderr)
            return await ms.edit('**ѕσмєтнιηg ωєηт ωяσηg кιη∂ℓу ¢нє¢к уσυя ιηρυтѕ Whether уσυ нανє ƒιℓℓє∂ ¢σяяє¢тℓу or ησт !**')

        try:
            NewConfig = {
                "Target": config['Target'],
                "accounts": list(config['accounts'])
            }

            new_account = {
                "Session_String": session.text,
                "OwnerUid": AccountHolder['id'],
                "OwnerName": AccountHolder['first_name']
            }
            NewConfig["accounts"].append(new_account)

            with open(config_path, 'w', encoding='utf-8') as file:
                json.dump(NewConfig, file, indent=4)

        except Exception as e:
            print(e)

        await ms.edit(text="**α¢¢ α∂∂є∂ ѕυ¢¢єѕѕƒυℓℓу**\n\n¢ℓι¢к тнє вυттση вєℓσω тσ νιєω αℓℓ тнє α¢¢συηтѕ уσυ нανє α∂∂є∂ .", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text='α¢¢συηтѕ уσυ α∂∂є∂', callback_data='account_config')]]))

    except Exception as e:
        print('Error on line {}'.format(
            sys.exc_info()[-1].tb_lineno), type(e).__name__, e)


@Client.on_message(filters.private & filters.user(Config.SUDO) & filters.command('target'))
async def target(bot: Client, cmd: Message):

    try:
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as file:
                config = json.load(file)

        else:
            return await cmd.reply_text(text="уσυ ∂ι∂η'т мαкє α ¢σηƒιg уєт !\n\n ƒιяѕтℓу мαкє ¢σηƒιg ву υѕιηg /config", reply_to_message_id=cmd.id)

        Info = await bot.get_chat(config['Target'])

        btn = [
            [InlineKeyboardButton(text='¢нαηgє тαяgєт',
                                  callback_data='chgtarget')]
        ]

        text = f"Channel Name :- <code> {Info.title} </code>\n¢нαηηєℓ υѕєяηαмє :- <code> @{Info.username} </code>\n¢нαηηяℓ ι∂ :- <code> {Info.id} </code>"

        await cmd.reply_text(text=text, reply_to_message_id=cmd.id, reply_markup=InlineKeyboardMarkup(btn))
    except Exception as e:
        print('Error on line {}'.format(
            sys.exc_info()[-1].tb_lineno), type(e).__name__, e)


@Client.on_message(filters.private & filters.user(Config.SUDO) & filters.command('del_config'))
async def delete_config(bot: Client, cmd: Message):

    btn = [
        [InlineKeyboardButton(text='Yes', callback_data='delconfig-yes')],
        [InlineKeyboardButton(text='No', callback_data='delconfig-no')]
    ]

    await cmd.reply_text(text="**⚠️ Are you Sure ?**\n\nYou want to delete the Config.", reply_to_message_id=cmd.id, reply_markup=InlineKeyboardMarkup(btn))
