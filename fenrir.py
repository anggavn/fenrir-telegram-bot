import asyncio
# import uvloop
# asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
import logging
import os
import re   #regex

from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.utils import exceptions
from aiogram.utils import executor

import pytoml as toml


class Config(object):
    def __init__(self, config_filename):
        self.config_filename = config_filename

        with open(config_filename, 'r') as config_file:
            cf = toml.load(config_file)
            #load credentials
            self.bot_token = cf['credentials']['bot_token']


logging.basicConfig(level=logging.INFO)


#startup
os.system('cls' if os.name == 'nt' else 'clear')
print('// Starting bot. Please wait. . .')

config = Config('config.toml')


loop = asyncio.get_event_loop()
storage = MemoryStorage()
fenrir = Bot(token=config.bot_token, loop=loop)
# try:
#     fenrir = Bot(token=config.bot_token, validate_token=true)
#     # if fails, raises: aiogram.utils.exceptions.ValidationError
# except exceptions.ValidationError:
#     pass
fenrir_disp = Dispatcher(fenrir, storage=storage)

# bot_info = @fenrir_disp.get_me()
# print(bot_info)



@fenrir_disp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.reply("[COMMAND 'START' INVOKED]")

@fenrir_disp.message_handler(commands=['get_me'])
async def cmd_get_me(message: types.Message):
    bot_info = await fenrir.get_me()
    print(bot_info)
    await message.reply(bot_info)

@fenrir_disp.message_handler(commands=['echo'])
async def cmd_echo(message: types.Message):
    print(message.is_command())
    print(message.get_args())
    await fenrir.send_message(message.chat.id, message.text)
    # await fenrir.send_message(message.get_args())

# @fenrir_disp.message_handler()
# @fenrir_disp.edited_message_handler()
# async def msg_edited(message: types.Message):
#     await fenrir.send_message(message.chat.id, message.text)

@fenrir_disp.message_handler()
async def rep_ugay(message: types.Message):
    txt = message.text.lower()
    rgx = "^(you|you\'re|ur|youre|your)\ (gay|homo)$"

    if re.match(rgx, txt) is not None:
        await message.reply("no u")

@fenrir_disp.message_handler(commands=['flood'])
async def cmd_flood(message: types.Message):
    try:
        await fenrir_disp.throttle('flood', rate=2)
    except exceptions.Throttled:
        await message.reply('throttled')
    else:
        await message.reply('unthrottled')

@fenrir_disp.message_handler(commands=['msg'])
async def cmd_msg(message: types.Message):
    print(message.message_id)
    print('')
    print(message.from_user.id)
    print(message.from_user.is_bot)
    print(message.from_user.first_name)
    print(message.from_user.last_name)
    print(message.from_user.username)
    print(message.from_user.language_code)
    print('')
    print(message.date)
    print(message.chat)
    print(message.text)


if __name__ == '__main__':
    executor.start_polling(fenrir_disp, loop=loop)


    # Also you can use another execution method
    # try:
    #     loop.run_until_complete(main())
    # except KeyboardInterrupt:
    #     loop.stop()