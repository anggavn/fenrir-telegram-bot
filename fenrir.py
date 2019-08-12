#!/usr/bin/env python3.7
"""/// FENRIR v1.12 ///////////////////////////////////////////////////////////
""/                                                                           /
"/                                                                            /
/
/
/                                                                            /"
/                                                                           /""
////////////////////////////////////////////////////////////////////////////"""

import asyncio
import datetime
# import uvloop
# asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
from inspect import signature
from io import BytesIO
import logging
import os
import re   #regex

from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import exceptions
from aiogram.utils import executor


from fenrir_config import Config
import fenrir_handler

#////////////////////////////////////////////////#
#////////////////////////////////////////////////#

# States
# class Form(StatesGroup):
#     name = State()  # Will be represented in storage as 'Form:name'
#     age = State()  # Will be represented in storage as 'Form:age'
#     gender = State() # Will be represented in storage as 'Form:gender'

#////////////////////////////////////////////////#
#////////////////////////////////////////////////#


logging.basicConfig(level=logging.INFO)

os.system('cls' if os.name == 'nt' else 'clear')    #clear screen
print('// Starting bot. Please wait. . .')

config = Config(config_filename='config.toml', \
                ori_config_filename='default_config.toml')  #load config
db_conn = config.db_conn
db_curs = config.db_curs
loop = asyncio.get_event_loop()
storage = MemoryStorage()
#TODO check for default config
# try:
#     fenrir = Bot(token=config.bot_token, validate_token=true)
#     # if fails, raises: aiogram.utils.exceptions.ValidationError
# except exceptions.ValidationError:
#     pass
fenrir = Bot(token=config.bot_token, loop=loop)
fenrir_disp = Dispatcher(fenrir, storage=storage)

#load bot profile data
get_bot_info = loop.create_task(fenrir.get_me())
bot_user = loop.run_until_complete(get_bot_info)
fenrir_id = bot_user.id
fenrir_is_bot = bot_user.is_bot
fenrir_first_name = bot_user.first_name
fenrir_last_name = bot_user.last_name
fenrir_username = bot_user.username
fenrir_language_code = bot_user.language_code


#////////////////////////////////////////////////#
#////////////////////////////////////////////////#


def display_info_msg(message: types.Message):
    """[TODO summary of func]
    args:
        [TODO insert arguments]
    returns:
        [TODO insert returns]
    """
    print('>>>>>>>>>>>>>>>>>>>> MSG START <<<<<<<<<<<<<<<<<<<<')
    print('msg_id:', message.message_id)
    print('')
    print('msg.from_user.id             :', message.from_user.id)
    print('msg.from_user.is_bot         :', message.from_user.is_bot)
    print('msg.from_user.first_name     :', message.from_user.first_name)
    print('msg.from_user.last_name      :', message.from_user.last_name)
    print('msg.from_user.username       :', message.from_user.username)
    print('msg.from_user.language_code  :', message.from_user.language_code)
    print('')
    print('msg.chat.id       :', message.chat.id)              #integer
    print('msg.chat.type     :', message.chat.type)          #string
    print('msg.chat.title    :', message.chat.title)        #chat title
    print('msg.chat.username :', message.chat.username)  #chat username
    print('')
    print('msg.date:', message.date)
    print('msg.text:', message.text)
    print('>>>>>>>>>>>>>>>>>>>>   MSG END <<<<<<<<<<<<<<<<<<<<\n')

def display_info_cmd(message: types.Message):
    """[TODO summary of func]
    args:
        [TODO insert arguments]
    returns:
        [TODO insert returns]
    """
    print('>>>>>>>>>>>>>>>>>>>> CMD START <<<<<<<<<<<<<<<<<<<<')
    print('msg_id:', message.message_id)
    print('')
    print('msg.from_user.id             :', message.from_user.id)
    print('msg.from_user.is_bot         :', message.from_user.is_bot)
    print('msg.from_user.first_name     :', message.from_user.first_name)
    print('msg.from_user.last_name      :', message.from_user.last_name)
    print('msg.from_user.username       :', message.from_user.username)
    print('msg.from_user.language_code  :', message.from_user.language_code)
    print('')
    print('msg.chat.id       :', message.chat.id)              #integer
    print('msg.chat.type     :', message.chat.type)          #string
    print('msg.chat.title    :', message.chat.title)        #chat title
    print('msg.chat.username :', message.chat.username)  #chat username
    print('')
    print('msg.iscmd  :', message.is_command())
    print('msg.cmdarg :', message.get_full_command())
    print('msg.cmd    :', message.get_command())
    print('msg.arg    :', message.get_args())
    print('')
    print('msg.date:', message.date)
    print('msg.text:', message.text)
    print('>>>>>>>>>>>>>>>>>>>>   CMD END <<<<<<<<<<<<<<<<<<<<\n')

def display_user_from_db(user):
    """[TODO summary of func]
    args:
        [TODO insert arguments]
    returns:
        [TODO insert returns]
    """
    print('>>>>>>>>>>>>>>>>>>>> USR START <<<<<<<<<<<<<<<<<<<<')
    print('user.id    :', user[0])
    print('user.isbot :', user[1])
    print('user.first :', user[2])
    print('user.last  :', user[3])
    print('user.uname :', user[4])
    print('user.lang  :', user[5])
    print('>>>>>>>>>>>>>>>>>>>>   USR END <<<<<<<<<<<<<<<<<<<<\n')

def display_info_photo(message: types.Message):
    """[TODO summary of func]
    args:
        [TODO insert arguments]
    returns:
        [TODO insert returns]
    """
    print('>>>>>>>>>>>>>>>>>>>> PHT START <<<<<<<<<<<<<<<<<<<<')
    print('msg_id:', message.message_id)
    print('')
    print('msg.fromuser.id    :', message.from_user.id)
    print('msg.fromuser.isbot :', message.from_user.is_bot)
    print('msg.fromuser.first :', message.from_user.first_name)
    print('msg.fromuser.last  :', message.from_user.last_name)
    print('msg.fromuser.uname :', message.from_user.username)
    print('msg.fromuser.lang  :', message.from_user.language_code)
    print('')
    print('msg.chat.id       :', message.chat.id)              #integer
    print('msg.chat.type     :', message.chat.type)          #string
    print('msg.chat.title    :', message.chat.title)        #chat title
    print('msg.chat.username :', message.chat.username)  #chat username
    print('')
    print('msg.date   :', message.date)
    print('msg.caption:', message.caption)
    for pht in message.photo:
        print('')
        print('pht.id       :', pht.file_id)     #string
        print('pht.width    :', pht.width)    #integer
        print('pht.height   :', pht.height)  #integer
        print('pht.filesize :', pht.file_size)     #integer
    print('>>>>>>>>>>>>>>>>>>>>   PHT END <<<<<<<<<<<<<<<<<<<<\n')


#text handler
@fenrir_disp.message_handler(content_types=types.message.ContentType.TEXT)
async def cmd_msg_handler(message: types.Message):
    """[TODO summary of func]
    args:
        [TODO insert arguments]
    returns:
        [TODO insert returns]
    """
    if config.bot_mode == 'bind':
        pass
    else:
        if message.chat.id in config.bot_ban:
            return

    if message.is_command():
        command = message.get_command()[1:].lower()
        if command.find('@') == -1:
            is_forbot = True
        elif command[command.find('@')+1:] == fenrir_username.lower():
            is_forbot = True
            command = command[0:command.find('@')]
        else:
            is_forbot = False

        if is_forbot:
            display_info_cmd(message)
            if message.reply_to_message is not None and message.reply_to_message.photo != []:
                print('>>>>>>>>>>>>>>>>>>>> REPLY MSG <<<<<<<<<<<<<<<<<<<<')
                display_info_photo(message.reply_to_message)
                message.message_id = message.reply_to_message.message_id
                message.photo = message.reply_to_message.photo
                if hasattr(fenrir_handler, command):
                    await getattr(fenrir_handler, command)(message=message, fenrir=fenrir, fenrir_disp=fenrir_disp, db_conn=db_conn, db_curs=db_curs, config=config)
            else:
                if hasattr(fenrir_handler, command):
                    await getattr(fenrir_handler, command)(message=message, fenrir=fenrir, fenrir_disp=fenrir_disp, db_conn=db_conn, db_curs=db_curs, config=config)
    elif re.match(r'(\W|\A)@admin\b', message.text, re.I): #calling admin
        display_info_msg(message)
        await getattr(fenrir_handler, 'admin_ping')(message=message, fenrir=fenrir, fenrir_disp=fenrir_disp, db_conn=db_conn, db_curs=db_curs, config=config)
    else: #not command
        display_info_msg(message)
        txt = message.text.lower()
        if hasattr(fenrir_handler, txt):
            await getattr(fenrir_handler, txt)(message=message, fenrir=fenrir, fenrir_disp=fenrir_disp, db_conn=db_conn, db_curs=db_curs, config=config)


@fenrir_disp.message_handler(content_types=types.message.ContentType.PHOTO or types.message.ContentType.DOCUMENT)
async def photo_handler(message: types.Message):
    """[TODO summary of func]
    args:
        [TODO insert arguments]
    returns:
        [TODO insert returns]
    """
    display_info_photo(message)
    if message.caption is not None:
        message.text = message.caption
        await cmd_msg_handler(message)

@fenrir_handler.group_only
@fenrir_disp.message_handler(content_types=types.message.ContentType.NEW_CHAT_MEMBERS or types.message.ContentType.LEFT_CHAT_MEMBER)
async def greeter_handler(message: types.Message):
    """[TODO summary of func]
    args:
        [TODO insert arguments]
    returns:
        [TODO insert returns]
    """
    new_chat_users = message.new_chat_members
    if new_chat_users != []:
        new_chat_usernames = ''
        newct = 0
        for new_chat_user in new_chat_users:
            if not new_chat_user.is_bot:
                if new_chat_user.username != '':
                    new_chat_usernames = new_chat_usernames + ' @' + new_chat_user.username
                else:
                    new_chat_usernames = new_chat_usernames + '[' + new_chat_user.first_name + '](' + new_chat_user.id + ')'
                newct = newct + 1
        if new_chat_usernames != '':
            try:
                SQL = 'SELECT welcomemsg FROM grouprec WHERE groupid = %s'
                groupid = message.chat.id
                db_curs.execute(SQL, (groupid,))
                welcome_text = db_curs.fetchone()[0].replace('\\n', '\n')
            except:
                welcome_text = repr('Hi there, {new_members}! Welcome to {group_title}.\nEnjoy your stay')
            await fenrir.send_message(message.chat.id, welcome_text.format(new_members=new_chat_usernames, group_title=message.chat.title, chat_title=message.chat.title), parse_mode='Markdown')

    left_chat_user = message.left_chat_member
    if left_chat_user is not None:
        try:
            SQL = 'SELECT goodbyemsg FROM grouprec WHERE groupid = %s'
            groupid = message.chat.id
            db_curs.execute(SQL, (groupid,))
            goodbye_text = db_curs.fetchone()[0].replace('\\n', '\n')
        except:
            goodbye_text = repr('So long, {left_member}! We\'ll probably miss you!')
        await fenrir.send_message(message.chat.id, goodbye_text.format(left_member='@' + (left_chat_user.username if left_chat_user.username is not None else left_chat_user.first_name), group_title=message.chat.title, chat_title=message.chat.title))

# @group_only
# @fenrir_disp.message_handler(content_types = types.message.ContentType.TEXT)
# async def greeter_handler_tester(message:types.Message):
#     new_chat_users = []
#     new_chat_users.append(message.from_user)
#     # if message.chat.id == -254633737: #group testing
#     if new_chat_users != []:
#         new_chat_usernames = ''
#         newct = 0
#         for new_chat_user in new_chat_users:
#             # if not new_chat_user.is_bot:
#                 new_chat_usernames = new_chat_usernames + ' @' + new_chat_user.username
#                 newct = newct + 1
#         if new_chat_usernames != '':
#             # welcome_text = f'Hi there, {new_chat_usernames}! Welcome to {message.chat.title}.\nEnjoy your stay';
#             SQL = 'SELECT welcomemsg FROM grouprec WHERE groupid = %s'
#             groupid = message.chat.id
#             db_curs.execute(SQL, (groupid,))
#             welcome_text = db_curs.fetchone()[0].replace('\\n', '\n')
#             await fenrir.send_message(message.chat.id, welcome_text.format(new_members=new_chat_usernames, group_title=message.chat.title, chat_title=message.chat.title))

#     left_chat_user = message.from_user
#     # if message.chat.id == -254633737:   #group testing
#     if left_chat_user != None:
#         # goodbye_text = f'So long, @{left_chat_user.username}! We\'ll probably miss you!'
#         # await fenrir.send_message(message.chat.id, goodbye_text)
#         SQL = 'SELECT goodbyemsg FROM grouprec WHERE groupid = %s'
#         groupid = message.chat.id
#         db_curs.execute(SQL, (groupid,))
#         goodbye_text = db_curs.fetchone()[0].replace('\\n', '\n')
#         await fenrir.send_message(message.chat.id, goodbye_text.format(left_member='@' + left_chat_user.username, group_title=message.chat.title, chat_title=message.chat.title))



#////////////////////////////////////////////////#
#////////////////////////////////////////////////#



if __name__ == '__main__':
    executor.start_polling(fenrir_disp, loop=loop)


    # Also you can use another execution method
    # try:
    #     loop.run_until_complete(main())
    # except KeyboardInterrupt:
    #     loop.stop()
