"""/// FENRIR ///// config.py /////////////////////////////////////////////////
""/                                                                           /
"/                                                                            /
/
/
/                                                                            /"
/                                                                           /""
////////////////////////////////////////////////////////////////////////////"""

import shutil

import psycopg2
import pytoml as toml
import requests


class Config():
    """handles configuration files loading and exporting

    [TODO longer class information]

    attr:
        [TODO insert attributes]
    """
    def __init__(self, config_filename, ori_config_filename):
        # self.config_filename = config_filename

        with open(config_filename, 'r') as config_file, \
             open(ori_config_filename, 'r') as ori_config_file:
            shutil.copy(config_filename, config_filename + '.bak')
            config_file.seek(0)
            cfg = toml.load(config_file)
            ori_cfg = toml.load(ori_config_file)


            if cfg['fenrir_version'] != ori_cfg['fenrir_version']:
                config_file.seek(0)
                new_cfg = config_file.read().splitlines()
                for lineidx, line in enumerate(new_cfg):
                    if new_cfg[lineidx].find('fenrir_version') != -1:
                        cmtidx = new_cfg[lineidx].find('#')  #preserving comments
                        if cmtidx != -1:
                            comment = new_cfg[lineidx][cmtidx:]
                        else:
                            comment = ''
                        new_cfg[lineidx] = toml.dumps({'fenrir_version': ori_cfg['fenrir_version']})[0:-1] + '    ' + comment
                    lineidx = lineidx + 1
                with open(config_filename, 'w') as new_config_file:
                    new_config_file.write('\n'.join(new_cfg))
                    print('// FENRIR v{} *NEWLY UPDATED*'.format(ori_cfg['fenrir_version']))
            else:
                print('// FENRIR v{}'.format(cfg['fenrir_version']))

            online_cfg = toml.loads(requests.get('https://raw.githubusercontent.com/AnTaRes27/fenrir-telegram-bot/master/default_config.toml').text)
            if ori_cfg['fenrir_version'] != online_cfg['fenrir_version']:
                print('// FENRIR v{} is available!'.format(online_cfg['fenrir_version']))

            #load credentials
            self.bot_token = cfg['credentials']['bot_token']
            self.db_name = cfg['credentials']['db_name']
            self.db_uname = cfg['credentials']['db_uname']
            self.db_pass = cfg['credentials']['db_pass']

            #initialise database
            self.db_conn = psycopg2.connect(dbname=self.db_name, \
                                            user=self.db_uname, \
                                            password=self.db_pass)
            self.db_curs = self.db_conn.cursor()
            if cfg['db_version'] != ori_cfg['db_version']:
                print('// NOTICE: DB out of date')
                print('//         client version is ' + cfg['db_version'])
                print('//         latest version is ' + ori_cfg['db_version'])
                print('// updating database . . .')
                self.build_database()
                config_file.seek(0)
                new_cfg = config_file.read().splitlines()
                lineidx = 0
                for line in new_cfg:
                    if new_cfg[lineidx].find('db_version') != -1:
                        cmtidx = new_cfg[lineidx].find('#')  #preserving comments
                        if cmtidx != -1:
                            comment = new_cfg[lineidx][cmtidx:]
                        else:
                            comment = ''
                        new_cfg[lineidx] = toml.dumps({'db_version': ori_cfg['db_version']})[0:-1] + '    ' + comment
                    lineidx = lineidx + 1
                with open(config_filename, 'w') as new_config_file:
                    new_config_file.write('\n'.join(new_cfg))
                print('// update success!')

            #load bot owner
            self.bot_owner = cfg['owner']['owner_id']
            # try:
            #     for foo in self.bot_owner:
            #         pass
            # except:
            #     #TODO change the config from int to list
            #     pass

            #load bind and ban list
            try:
                self.bot_mode = cfg['settings']['chat_id_mode']
            except:
                self.bot_mode = None
            self.bot_bind = cfg['settings']['chat_id_bind']
            self.bot_ban = cfg['settings']['chat_id_ban']

    def build_database(self):
        """[TODO summary of func]
        args:
            [TODO insert arguments]
        returns:
            [TODO insert returns]
        """
        SQL = '''CREATE TABLE IF NOT EXISTS tguser(
                 id integer primary key)
                 ;'''
        self.db_curs.execute(SQL)
        SQL = '''ALTER TABLE tguser
                 ADD COLUMN IF NOT EXISTS is_bot boolean not null,
                 ADD COLUMN IF NOT EXISTS first_name text,
                 ADD COLUMN IF NOT EXISTS last_name text,
                 ADD COLUMN IF NOT EXISTS username text,
                 ADD COLUMN IF NOT EXISTS language_code text
                 ;'''
        self.db_curs.execute(SQL)

        SQL = '''CREATE TABLE IF NOT EXISTS tggroup(
                 id bigint primary key)
                 ;'''
        self.db_curs.execute(SQL)
        SQL = '''ALTER TABLE tggroup
                 ADD COLUMN IF NOT EXISTS type text not null,
                 ADD COLUMN IF NOT EXISTS title text,
                 ADD COLUMN IF NOT EXISTS username text,
                 ADD COLUMN IF NOT EXISTS allmemberadmin boolean
                 ;'''
        self.db_curs.execute(SQL)

        SQL = '''CREATE TABLE IF NOT EXISTS oworep(
                 replyid serial)
                 ;'''
        self.db_curs.execute(SQL)
        SQL = '''ALTER TABLE oworep
                 ADD COLUMN IF NOT EXISTS foruserid integer not null,
                 ADD COLUMN IF NOT EXISTS reply text not null
                 ;'''
        self.db_curs.execute(SQL)

        SQL = '''CREATE TABLE IF NOT EXISTS callme(
                 userid integer,
                 name text)
                 ;'''
        self.db_curs.execute(SQL)
        SQL = '''ALTER TABLE callme
                 ADD COLUMN IF NOT EXISTS name text not null
                 ;'''
        self.db_curs.execute(SQL)

        SQL = '''CREATE TABLE IF NOT EXISTS grouprec(
                 groupid bigint primary key)
                 ;'''
        self.db_curs.execute(SQL)
        SQL = '''ALTER TABLE grouprec
                 ADD COLUMN IF NOT EXISTS welcomemsg text,
                 ADD COLUMN IF NOT EXISTS goodbyemsg text,
                 ADD COLUMN IF NOT EXISTS rules text
                 ;'''
        self.db_curs.execute(SQL)

        self.db_conn.commit()