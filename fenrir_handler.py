"""/// FENRIR ///// fenrir_handler.py /////////////////////////////////////////
""/                                                                           /
"/                                                                            /
/
/
/                                                                            /"
/                                                                           /""
////////////////////////////////////////////////////////////////////////////"""

import random

from aiogram import types
from aiogram.utils import exceptions

from PIL import Image, ImageDraw, ImageFont


def admin_only(func):
    """[TODO summary of func]
    args:
        [TODO insert arguments]
    returns:
        [TODO insert returns]
    """
    def isadmin(invoker, chatadmins):
        adminids = []
        for admin in chatadmins:
            adminids.append(admin.user.id)
        return invoker.id in adminids

    async def wrapper(message: types.Message, fenrir, fenrir_disp, config, db_conn, db_curs, **kwargs):
        invoker = message.from_user
        chatadmins = await message.chat.get_administrators()
        if isadmin(invoker, chatadmins):
            await func(message=message, fenrir=fenrir, fenrir_disp=fenrir_disp, config=config, db_conn=db_conn, db_curs=db_curs)
            # print('isadmin')
            #TODO tell that an admin thing is performed
        else:
            # print('notadmin')
            #TODO tell that an admin thing is denied
            pass

    return wrapper


def owner_only(func):
    """[TODO summary of func]
    args:
        [TODO insert arguments]
    returns:
        [TODO insert returns]
    """
    async def wrapper(message: types.Message, fenrir, fenrir_disp, config, db_conn, db_curs, **kwargs):
        invokerid = message.from_user.id
        ownerid = config.bot_owner
        if invokerid in ownerid:
            await func(message=message, fenrir=fenrir, fenrir_disp=fenrir_disp, config=config, db_conn=db_conn, db_curs=db_curs)
            # print('isowner')
            #TODO tell that an admin thing is performed
        else:
            # print('notowner')
            #TODO tell that an admin thing is denied
            pass

    return wrapper


def pm_only(func):
    """[TODO summary of func]
    args:
        [TODO insert arguments]
    returns:
        [TODO insert returns]
    """
    async def wrapper(message: types.Message, fenrir, fenrir_disp, config, db_conn, db_curs, **kwargs):
        if message.chat.type == 'private':
            await func(message=message, fenrir=fenrir, fenrir_disp=fenrir_disp, config=config, db_conn=db_conn, db_curs=db_curs)
            # print('isgroup')
            #TODO tell that an admin thing is performed
        else:
            # print('notgroup')
            #TODO tell that an admin thing is denied
            pass

    return wrapper


def group_only(func):
    """[TODO summary of func]
    args:
        [TODO insert arguments]
    returns:
        [TODO insert returns]
    """
    async def wrapper(message: types.Message, fenrir, fenrir_disp, config, db_conn, db_curs, **kwargs):
        if message.chat.type in ['group', 'supergroup']:
            await func(message=message, fenrir=fenrir, fenrir_disp=fenrir_disp, config=config, db_conn=db_conn, db_curs=db_curs)
            # print('isgroup')
            #TODO tell that an admin thing is performed
        else:
            # print('notgroup')
            #TODO tell that an admin thing is denied
            pass

    return wrapper


def supergroup_only(func):
    """[TODO summary of func]
    args:
        [TODO insert arguments]
    returns:
        [TODO insert returns]
    """
    async def wrapper(message: types.Message, fenrir, fenrir_disp, config, db_conn, db_curs, **kwargs):
        if message.chat.type == 'supergroup':
            await func(message=message, fenrir=fenrir, fenrir_disp=fenrir_disp, config=config, db_conn=db_conn, db_curs=db_curs)
            # print('isgroup')
            #tell that an admin thing is performed
        else:
            # print('notgroup')
            #tell that an admin thing is denied
            pass

    return wrapper

#/////////////////////////////////////////////////////////////////////////////#
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> GENERAL TESTING <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<#
#/////////////////////////////////////////////////////////////////////////////#

async def echo(message: types.Message, **kwargs):
    """returns back the typed message
    args:
        [TODO insert arguments]
    returns:
        [TODO insert returns]
    """
    await message.reply(message.text)

async def deleteme(message: types.Message, **kwargs):
    """deletes the typed message if bot has permission
    args:
        [TODO insert arguments]
    returns:
        [TODO insert returns]
    """
    await message.delete()

#/////////////////////////////////////////////////////////////////////////////#
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> GROUP GENERAL <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<#
#/////////////////////////////////////////////////////////////////////////////#

# @owner_only
# @admin_only
@group_only
async def membercount(message: types.Message, **kwargs):
    """[TODO summary of func]
    args:
        [TODO insert arguments]
    returns:
        [TODO insert returns]
    """
    membercount = await message.chat.get_members_count()
    await message.reply(f'There are {membercount} members here.')

@group_only
async def chatadmins(message: types.Message, **kwargs):
    """[TODO summary of func]
    args:
        [TODO insert arguments]
    returns:
        [TODO insert returns]
    """
    chatadmins = await message.chat.get_administrators()
    admins = ''
    adminct = 0
    for admin in chatadmins:
        if not admin.user.is_bot:
            admins = admins + ' @' + admin.user.username
            adminct = adminct + 1

    reply = 'The ' + ('admin' if adminct == 1 else 'admins') + ' of this chat ' + ('is' if adminct == 1 else 'are')
    await message.reply(reply + admins)

@group_only
async def admin_ping(message: types.Message, fenrir, fenrir_disp, **kwargs):
    """[TODO summary of func]
    args:
        [TODO insert arguments]
    returns:
        [TODO insert returns]
    """
    #TODO make relevant database
    #TODO prevent duplicate reports

    try:
        await fenrir_disp.throttle('admin_ping', rate=300, chat=message.chat.id)
    except exceptions.Throttled:
        await message.reply('Thank you for your concern, but a report has already been made. An admin will look into it shortly.')
    else:
        group_name = message.chat.title
        if message.chat.type == 'private':
            chat_link = f"tg://user?id={message.chat.id}"
        elif message.chat.username:
            chat_link = f"https://t.me/{message.chat.username}"
        elif message.chat.invite_link:
            chat_link = message.chat.invite_link
        else:
            chat_link = await message.chat.export_invite_link()

        if message.reply_to_message != None:
            problem_id = f'{abs(message.chat.id)}{message.reply_to_message.message_id}'
        else:
            problem_id = f'{abs(message.chat.id)}{message.message_id}'

        await message.reply(f'The admins have been notified with a report number #FNRPT{problem_id}')

        chatadmins = await message.chat.get_administrators()
        admins = ''
        adminct = 0
        for admin in chatadmins:
            if not admin.user.is_bot:
                msg = f'Member of <a href="{chat_link}">{group_name}</a> pinged @admin. Report number is #FNRPT{problem_id}'
                print(f"sending report to: {admin.user.username}... ", end='')
                try:
                    await fenrir.send_message(admin.user.id, msg, parse_mode='HTML')
                    print('SUCCESS')
                except exceptions.CantInitiateConversation:
                    print('CANT INITIATE CONVERSATION')
                    pass
        pass

@group_only
async def rules(message: types.Message, fenrir, db_curs, **kwargs):
    """[TODO summary of func]
    args:
        [TODO insert arguments]
    returns:
        [TODO insert returns]
    """
    try:
        SQL = 'SELECT rules FROM grouprec WHERE groupid = %s'
        groupid = message.chat.id
        db_curs.execute(SQL, (groupid,))
        rules_text = db_curs.fetchone()[0].replace('\\n', '\n')
    except:
        rules_text = 'There is no law in {group_title}.\nThis is a free for all PvP zone.\nGood luck'
    await fenrir.send_message(message.chat.id, rules_text.format(group_title=message.chat.title, chat_title=message.chat.title))

async def rate(message: types.Message, **kwargs):
    """[TODO summary of func]
    args:
        [TODO insert arguments]
    returns:
        [TODO insert returns]
    """
    if message.photo != []:
        seedid = 'AgADAQAD_qcxG2G8uEVSeeAqUIVdOKBrDDAABEm6IDw5N0wAAZaWAgABAg'
        seedhash = 0
        for achr in seedid:
            seedhash = seedhash + ord(achr)
        maxid = 'AgADAQAD-6cxG2G8uEWMG2fwmO6Cpr8j9y8ABE4xLP6rt9wAAWljBAABAg'
        maxhash = 0
        for achr in maxid:
            maxhash = maxhash + ord(achr)
        hashtotal = 0
        for achr in message.photo[0].file_id:
            hashtotal = hashtotal + ord(achr)
        percentage = 1-min(abs((hashtotal-seedhash)/(maxhash-seedhash)), abs((maxhash-seedhash)/(abs(hashtotal-seedhash)+1)))

        await message.reply('This is {0:.0%} gay'.format(percentage))

#////////////////////////////////////////////#
#>>>>>>>>>>>>>> GROUP MANAGEMENT <<<<<<<<<<<<#
#////////////////////////////////////////////#

@group_only
@admin_only
async def getlink(message: types.Message, fenrir, **kwargs):
    """[TODO summary of func]
    args:
        [TODO insert arguments]
    returns:
        [TODO insert returns]
    """
    if message.chat.type == 'private':
        chatlink = f"tg://user?id={message.chat.id}"
    elif message.chat.username:
        chatlink = f"https://t.me/{message.chat.username}"
    elif message.chat.invite_link:
        chatlink = message.chat.invite_link
    else:
        chatlink = await message.chat.export_invite_link()
    invokerid = message.from_user.id
    await message.reply('Order received. Check your PM.')
    await fenrir.send_message(invokerid, message.chat.title + ': ' + chatlink)

@group_only
@admin_only
async def genlink(message: types.Message, fenrir, **kwargs):
    """[TODO summary of func]
    args:
        [TODO insert arguments]
    returns:
        [TODO insert returns]
    """
    chatlink = await message.chat.export_invite_link()
    invokerid = message.from_user.id
    await message.reply('Order received. Check your PM.')
    await fenrir.send_message(invokerid, message.chat.title + ': ' + chatlink)

# async def getuserinfofromdb(message: types.Message):
#     SQL = 'SELECT * FROM tguser WHERE id = %s'
#     userid = int(float(message.get_args()))
#     db_curs.execute(SQL, (userid,))
#     user = db_curs.fetchone()
#     display_user_from_db(user)

@group_only
@admin_only
async def setwelcome(message: types.Message, fenrir, db_curs, db_conn, **kwargs):
    """[TODO summary of func]
       {new_members}
       {group_title}
    args:
        [TODO insert arguments]
    returns:
        [TODO insert returns]
    """
    if message.reply_to_message == None:
        welcome_text = message.get_args()
    else:
        welcome_text = message.reply_to_message.text
    groupid = message.chat.id

    SQL = '''INSERT INTO grouprec
                (groupid, welcomemsg)
             VALUES (%s, %s)
             ON CONFLICT (groupid) DO UPDATE 
                SET welcomemsg = %s
             ;'''

    db_curs.execute(SQL, (groupid, welcome_text, welcome_text))
    db_conn.commit()

    await fenrir.send_message(groupid, 'Welcome message successfully changed!')

@group_only
@admin_only
async def setgoodbye(message: types.Message, fenrir, db_curs, db_conn, **kwargs):
    """[TODO summary of func]
       {left_members}
    args:
        [TODO insert arguments]
    returns:
        [TODO insert returns]
    """
    if message.reply_to_message == None:
        goodbye_text = message.get_args()
    else:
        goodbye_text = message.reply_to_message.text
    groupid = message.chat.id

    SQL = '''INSERT INTO grouprec
                (groupid, goodbyemsg)
             VALUES (%s, %s)
             ON CONFLICT (groupid) DO UPDATE 
                SET goodbyemsg = %s
             ;'''

    db_curs.execute(SQL, (groupid, goodbye_text, goodbye_text))
    db_conn.commit()

    await fenrir.send_message(groupid, 'Farewell message successfully changed!')

@group_only
@admin_only
async def testgreetings(message: types.Message, fenrir, db_curs, **kwargs):
    """[TODO summary of func]
    args:
        [TODO insert arguments]
    returns:
        [TODO insert returns]
    """
    SQL = 'SELECT welcomemsg FROM grouprec WHERE groupid = %s'
    groupid = message.chat.id
    db_curs.execute(SQL, (groupid,))
    welcome_text = db_curs.fetchone()[0].replace('\\n', '\n')
    await fenrir.send_message(message.chat.id, welcome_text.format(new_members='@' + message.from_user.username, group_title=message.chat.title, chat_title=message.chat.title))

    SQL = 'SELECT goodbyemsg FROM grouprec WHERE groupid = %s'
    groupid = message.chat.id
    db_curs.execute(SQL, (groupid,))
    goodbye_text = db_curs.fetchone()[0].replace('\\n', '\n')
    await fenrir.send_message(message.chat.id, goodbye_text.format(left_member='@' + message.from_user.username, group_title=message.chat.title, chat_title=message.chat.title))

@group_only
@admin_only
async def setrules(message: types.Message, fenrir, db_curs, db_conn, **kwargs):
    """[TODO summary of func]
    args:
        [TODO insert arguments]
    returns:
        [TODO insert returns]
    """
    if message.reply_to_message == None:
        rules_text = message.get_args()
    else:
        rules_text = message.reply_to_message.text
    groupid = message.chat.id

    SQL = '''INSERT INTO grouprec
                (groupid, rules)
             VALUES (%s, %s)
             ON CONFLICT (groupid) DO UPDATE 
                SET rules = %s
             ;'''

    db_curs.execute(SQL, (groupid, rules_text, rules_text))
    db_conn.commit()

    await fenrir.send_message(groupid, 'Rules successfully changed!')

@group_only
@admin_only
async def pin(message: types.Message, fenrir, **kwargs):
    """[TODO summary of func]
    args:
        [TODO insert arguments]
    returns:
        [TODO insert returns]
    """
    if message.reply_to_message != None:
        if message.get_args().lower() == 'silent':
            await fenrir.pin_chat_message(message.chat.id, message.reply_to_message.message_id, disable_notification=True)
        else:
            await fenrir.pin_chat_message(message.chat.id, message.reply_to_message.message_id)

@group_only
@admin_only
async def unpin(message: types.Message, fenrir, **kwargs):
    """[TODO summary of func]
    args:
        [TODO insert arguments]
    returns:
        [TODO insert returns]
    """
    await fenrir.unpin_chat_message(message.chat.id)

@group_only
@admin_only
async def purge(message: types.Message, **kwargs):
    """[TODO summary of func]
    args:
        [TODO insert arguments]
    returns:
        [TODO insert returns]
    """
    # TODO delete messages like a few before
    pass




#////////////////////////////////////////////#
#>>>>>>>>>>>>>> DEV ONLY         <<<<<<<<<<<<#
#////////////////////////////////////////////#

@owner_only
async def addusertodb(message_ori: types.Message, db_conn, db_curs, **kwargs):
    """[TODO summary of func]
    args:
        [TODO insert arguments]
    returns:
        [TODO insert returns]
    """
    if message_ori.from_user.id == 404176080:
        message = message_ori.reply_to_message

        SQL = '''INSERT INTO tguser
                    (id, is_bot, first_name, last_name,
                     username, language_code)
                 VALUES (%s, %s, %s, %s, %s, %s)
                 ON CONFLICT (id) DO UPDATE 
                    SET is_bot = %s,
                        first_name = %s,
                        last_name = %s,
                        username = %s,
                        language_code = %s
                 ;'''

        userid = message.from_user.id
        is_bot = message.from_user.is_bot
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        username = message.from_user.username
        language_code = message.from_user.language_code

        print('>>>>>>>>>>>>>>>>>>>> DBADD     <<<<<<<<<<<<<<<<<<<<')
        print('user.id    :', userid)
        print('user.isbot :', is_bot)
        print('user.first :', first_name)
        print('user.last  :', last_name)
        print('user.uname :', username)
        print('user.lang  :', language_code)
        print('>>>>>>>>>>>>>>>>>>>> DBADD END <<<<<<<<<<<<<<<<<<<<\n')

        db_curs.execute(SQL, (userid, is_bot, first_name, last_name, username, language_code, is_bot, first_name, last_name, username, language_code))
        db_conn.commit()

        # await CMD_handler.whatisthis(message)

@owner_only
async def addoworeply(message: types.Message, db_conn, db_curs, **kwargs):
    """[TODO summary of func]
    args:
        [TODO insert arguments]
    returns:
        [TODO insert returns]
    """
    if message.reply_to_message is None:
        return

    for_user = message.reply_to_message.from_user
    reply = message.get_args()

    SQL = '''INSERT INTO oworep
                (foruserid, reply)
             VALUES (%s, %s)
             ;'''

    db_curs.execute(SQL, (for_user.id, reply, ))
    db_conn.commit()

    await message.reply(f'Reply added for @{for_user.username}!')

@owner_only
async def displayoworeply(message: types.Message, **kwargs):
    """[TODO summary of func]
    args:
        [TODO insert arguments]
    returns:
        [TODO insert returns]
    """
    if message.reply_to_message is None:
        return

    for_user = message.reply_to_message.from_user
    reply = message.get_args()

    # SQL = '''INSERT INTO oworep
    #             (foruserid, reply)
    #          VALUES (%s, %s)
    #          ;'''

    # db_curs.execute(SQL, (for_user.id, reply, ))
    # db_conn.commit()

    # await message.reply(f'Reply added for @{for_user.username}!')

@owner_only
async def purgeoworeply(message: types.Message, **kwargs):
    """[TODO summary of func]
    args:
        [TODO insert arguments]
    returns:
        [TODO insert returns]
    """
    if message.reply_to_message is None:
        return

    for_user = message.reply_to_message.from_user
    reply = message.get_args()

    # SQL = '''INSERT INTO oworep
    #             (foruserid, reply)
    #          VALUES (%s, %s)
    #          ;'''

    # db_curs.execute(SQL, (for_user.id, reply, ))
    # db_conn.commit()

    await message.reply(f'All replies purged for @{for_user.username}!')

@owner_only
async def whatisthis(message: types.Message, **kwargs):
    """[TODO summary of func]
    args:
        [TODO insert arguments]
    returns:
        [TODO insert returns]
    """
    print('>>>>>>>>>>>>>>>>>>>> REPLY MSG <<<<<<<<<<<<<<<<<<<<')
    display_info_msg(message.reply_to_message)

@owner_only
async def saygoodnight(message: types.Message, fenrir, config, **kwargs):
    """[TODO summary of func]
    args:
        [TODO insert arguments]
    returns:
        [TODO insert returns]
    """
    await fenrir.send_message(message.chat.id, "Goodnight, everyone!")

@owner_only
async def genticket(message: types.Message, **kwargs):
    """[TODO summary of func]
    args:
        [TODO insert arguments]
    returns:
        [TODO insert returns]
    """
    im = Image.open('citation/awoo.png')
    draw = ImageDraw.Draw(im)
    ocr_font = ImageFont.truetype('citation/ocr_a_std.ttf', 22)
    # vcr_font_sml = ImageFont.truetype('citation/vcr_osd_mono.ttf', 18)
    vcr_font_big = ImageFont.truetype('citation/vcr_osd_mono.ttf', 60)

    guide_text = 'The format for submitting a citation is:\n/genticket [cit. type]#[offender]#[AAIN]#[viol. location]#[viol. checkmarks]#[viol. note]#[cit. amount]'

    cit_info = message.get_args().split('#')
    if len(cit_info) != 7:
        await message.reply(guide_text)
        return

    cit_type = cit_info[0].strip()
    cit_type_loc = (round(im.size[0]/2), 360)
    if cit_type == '1':
        cit_type_text = 'NOTICE'
    elif cit_type == '2':
        cit_type_text = 'WARNING'
    else:
        cit_type_text = 'VIOLATION'

    w, h = draw.textsize(cit_type_text, font=vcr_font_big)
    cit_type_loc = (round(cit_type_loc[0]-w/2), round(cit_type_loc[1]-h/2))
    draw.text(cit_type_loc, cit_type_text, fill='white', font=vcr_font_big)

    ifblk_x = 187
    ifblk_y_height = draw.textsize('0', font=ocr_font)[1]
    ifblk_y_start = round(442-ifblk_y_height/2)
    ifblk_y_offset = 24
    cit_no = '{:010d}'.format(random.randint(0, 9999999999))
    iss_date = datetime.date.today().isoformat()
    iss_time = datetime.datetime.now().time().isoformat()[0:5]
    draw.text((ifblk_x, ifblk_y_start), cit_no, fill='black', font=ocr_font)
    draw.text((ifblk_x, ifblk_y_start+1*ifblk_y_offset), iss_date, fill='black', font=ocr_font)
    draw.text((ifblk_x, ifblk_y_start+2*ifblk_y_offset), iss_time, fill='black', font=ocr_font)

    off_name = cit_info[1].upper()
    off_aain = cit_info[2].upper()
    location = cit_info[3].upper()
    draw.text((ifblk_x, ifblk_y_start+4*ifblk_y_offset), off_name, fill='black', font=ocr_font)
    draw.text((ifblk_x, ifblk_y_start+5*ifblk_y_offset), off_aain, fill='black', font=ocr_font)
    draw.text((ifblk_x, ifblk_y_start+6*ifblk_y_offset), location, fill='black', font=ocr_font)

    vtype = cit_info[4].strip()
    viol_extr = cit_info[5].upper()
    vtype_x = 25
    vtype_y_start = 656
    vtype_y_offset = 23
    vtype_markersize = draw.textsize('X', font=ocr_font)
    vtype_x = round(vtype_x-vtype_markersize[0]/2)
    vtype_y_start = round(vtype_y_start-vtype_markersize[1]/2)
    for viol in vtype:
        if viol == '1':
            draw.text((vtype_x, vtype_y_start+0*vtype_y_offset), 'X', fill='black', font=ocr_font)
        elif viol == '2':
            draw.text((vtype_x, vtype_y_start+1*vtype_y_offset), 'X', fill='black', font=ocr_font)
        elif viol == '3':
            draw.text((vtype_x, vtype_y_start+2*vtype_y_offset), 'X', fill='black', font=ocr_font)
        elif viol == '4':
            draw.text((vtype_x, vtype_y_start+4*vtype_y_offset), 'X', fill='black', font=ocr_font)
        else:
            draw.text((vtype_x, vtype_y_start+6*vtype_y_offset), 'X', fill='black', font=ocr_font)
            draw.text((vtype_x+27, round(vtype_y_start+6*vtype_y_offset)), viol_extr, fill='black', font=ocr_font)

    fine = cit_info[6]
    fine_x = 210
    fine_y = 854-draw.textsize('X', font=ocr_font)[1]
    draw.text((fine_x, fine_y), fine, fill='black', font=ocr_font)

    bio = BytesIO()
    bio.name = 'ticket.png'
    im.save(bio, 'PNG')
    bio.seek(0)
    await fenrir.send_document(message.chat.id, document=bio)

# @owner_only
# async def teststorage(message:types.Message):
#     # Set state
#     await Form.name.set()
#     print(Form.name);
#     await message.reply("Hi there! What's your name?")





async def owo(message: types.Message, fenrir_disp, db_curs, **kwargs):
    try:
        await fenrir_disp.throttle('owo', rate=60, user=message.from_user.id, chat=message.chat.id)
    except exceptions.Throttled:
        pass
    else:
        userid = message.from_user.id
        SQL = '''SELECT reply FROM oworep
                    WHERE
                     CASE
                        WHEN %s in (select foruserid from oworep)
                        THEN foruserid = %s
                     ELSE
                        foruserid = 0
                     END
              ;'''

        db_curs.execute(SQL, (userid, userid))
        replies = db_curs.fetchall()
        await message.reply(replies[random.randint(1, len(replies))-1][0])