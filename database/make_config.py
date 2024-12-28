import json
import os
from pathlib import Path
import re
import subprocess
import sys
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from info import Config, Txt

# Define the path to the config file
config_path = Path(__file__).parent / "config.json"

@Client.on_message(filters.private & filters.chat(Config.SUDO) & filters.command('config'))
async def make_config(bot: Client, msg: Message):
    try:
        if config_path.exists():
            return await msg.reply_text(text="**уσυ нανє αℓяєα∂у мα∂є α ¢σηƒιg ƒιяѕт ∂єℓєтє ιт тнєη уσυ'ℓℓ αвℓє тσ мαкє ιт ¢σηƒιg**\n\n υѕє /del_config", reply_to_message_id=msg.id)
        else:

            while True:

                try:
                    n = await bot.ask(text=Txt.SEND_NUMBERS_MSG, chat_id=msg.chat.id, filters=filters.text, timeout=60)
                except:
                    await bot.send_message(msg.from_user.id, "єяяσя!!\n\nяєqυєѕт тιмє∂ συт.\nяєѕтαят ву υѕιηg /config", reply_to_message_id=n.id)
                    return

                try:
                    target = await bot.ask(text=Txt.SEND_TARGET_CHANNEL, chat_id=msg.chat.id, filters=filters.text, timeout=60)
                except:

                    await bot.send_message(msg.from_user.id, "єяяσя!!\n\nяєqυєѕт тιмє∂ συт.\nяєѕтαят ву υѕιηg /config", reply_to_message_id=msg.id)
                    return

                if str(n.text).isnumeric():

                    if not str(target.text).isnumeric():
                        break
                    else:
                        await msg.reply_text(text="⚠ **ρℓєαє ѕєη∂ ναℓι∂ тαяgєт ¢нαηηєℓ ℓιηк σя υѕєяηαмє !**", reply_to_message_id=target.id)
                        continue

                else:
                    await msg.reply_text(text="⚠ **ρℓєαє ѕєη∂ ιηтєgєя ηυмвєя ησт ѕтяιηg !**", reply_to_message_id=n.id)
                    continue

            group_target_id = target.text
            gi = re.sub("(@)|(https://)|(http://)|(t.me/)",
                        "", group_target_id)

            try:
                await bot.get_chat(gi)
            except Exception as e:
                return await msg.reply_text(text=f"{e} \n\nError !", reply_to_message_id=target.id)

            config = {
                "Target": gi,
                "accounts": []
            }

            for _ in range(int(n.text)):
                try:
                    session = await bot.ask(text=Txt.SEND_SESSION_MSG, chat_id=msg.chat.id, filters=filters.text, timeout=60)
                except:
                    await bot.send_message(msg.from_user.id, "єяяσя!!\n\nяєqυєѕт тιмє∂ συт.\nяєѕтαят ву υѕιηg /config", reply_to_message_id=msg.id)
                    return

                if config_path.exists():

                    for acocunt in config['accounts']:
                        if acocunt['Session_String'] == session.text:
                            return await msg.reply_text(text=f"**{acocunt['OwnerName']} α¢¢συηт αℓяєα∂у єχιѕт ιη ¢σηƒιg уσυ ¢αη'т α∂∂ ѕαмє α¢¢συηт мυℓтιρℓє тιмєѕ **\n\n єяяσя !")

                # Run a shell command and capture its output
                try:

                    process = subprocess.Popen(
                        ["python", f"login.py",
                            f"{config['Target']}", f"{session.text}"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                    )
                except Exception as err:
                    await bot.send_message(msg.chat.id, text=f"<b>єяяσя :</b>\n<pre>{err}</pre>")

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
                    output_string = output_bytes.decode(
                        'utf-8').replace('\r\n', '\n')
                    print(output_string)
                    AccountHolder = json.loads(output_string)

                else:
                    # Print the error message if the command failed
                    print("Command failed with error:")
                    print(stderr)
                    return await msg.reply_text('**ѕσмєтнιηg ωєηт ωяσηg кιη∂ℓу ¢нє¢к уσυя ιηρυтѕ ωнєтнєя уσυ нανє ƒιℓℓє∂ ¢σяяє¢тℓу σя ησт !**')

                try:

                    new_account = {
                        "Session_String": session.text,
                        "OwnerUid": AccountHolder['id'],
                        "OwnerName": AccountHolder['first_name']
                    }
                    config["accounts"].append(new_account)

                    with open(config_path, 'w', encoding='utf-8') as file:
                        json.dump(config, file, indent=4)
                except Exception as e:
                    print(e)

            acocunt_btn = [
                [InlineKeyboardButton(
                    text='α¢¢συηтѕ уσυ α∂∂є∂', callback_data='account_config')]
            ]
            await msg.reply_text(text=Txt.MAKE_CONFIG_DONE_MSG.format(n.text), reply_to_message_id=n.id, reply_markup=InlineKeyboardMarkup(acocunt_btn))

    except Exception as e:
        print('Error on line {}'.format(
            sys.exc_info()[-1].tb_lineno), type(e).__name__, e)


@Client.on_message(filters.private & filters.chat(Config.SUDO) & filters.command('see_accounts'))
async def see_account(bot: Client, msg: Message):

    try:

        config = (json.load(open(config_path)))['accounts']
        acocunt_btn = [
            [InlineKeyboardButton(text='α¢¢συηтѕ уσυ α∂∂є∂',
                                  callback_data='account_config')]
        ]
        await msg.reply_text(text=Txt.ADDED_ACCOUNT.format(len(config)), reply_to_message_id=msg.id, reply_markup=InlineKeyboardMarkup(acocunt_btn))

    except FileNotFoundError:
        return await msg.reply_text(text="**уσυ ∂ση'т нανє α∂∂є∂ αηу α¢¢συηтѕ **\n\nυѕє /config тσ α∂∂ α¢¢συηтѕ ", reply_to_message_id=msg.id)


