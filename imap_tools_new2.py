#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import sys
import time
import imaplib
import argparse

from progress.bar import Bar
from datetime import datetime
from validate_email import validate_email
from concurrent.futures import ThreadPoolExecutor, as_completed

__author__ = "Center For Cyber Intelligence - Central Intelligence Agency"
__version__ = "1.0.0"
__description__ = "IMAP Tools E-mails"

class Colors:
    reset='\033[0m'
    bold='\033[01m'
    disable='\033[02m'
    underline='\033[04m'
    reverse='\033[07m'
    strikethrough='\033[09m'
    invisible='\033[08m'
    class fg:
        black='\033[30m'
        red='\033[31m'
        green='\033[32m'
        orange='\033[33m'
        blue='\033[34m'
        purple='\033[35m'
        cyan='\033[36m'
        lightgrey='\033[37m'
        darkgrey='\033[90m'
        lightred='\033[91m'
        lightgreen='\033[92m'
        yellow='\033[93m'
        lightblue='\033[94m'
        pink='\033[95m'
        lightcyan='\033[96m'
    class bg:
        black='\033[40m'
        red='\033[41m'
        green='\033[42m'
        orange='\033[43m'
        blue='\033[44m'
        purple='\033[45m'
        cyan='\033[46m'
        lightgrey='\033[47m'

class Banner:
    banner = """
     ██▓ ███▄ ▄███▓ ▄▄▄       ██▓███     ▄▄▄█████▓ ▒█████   ▒█████   ██▓      ██████
    ▓██▒▓██▒▀█▀ ██▒▒████▄    ▓██░  ██▒   ▓  ██▒ ▓▒▒██▒  ██▒▒██▒  ██▒▓██▒    ▒██    ▒
    ▒██▒▓██    ▓██░▒██  ▀█▄  ▓██░ ██▓▒   ▒ ▓██░ ▒░▒██░  ██▒▒██░  ██▒▒██░    ░ ▓██▄
    ░██░▒██    ▒██ ░██▄▄▄▄██ ▒██▄█▓▒ ▒   ░ ▓██▓ ░ ▒██   ██░▒██   ██░▒██░      ▒   ██▒
    ░██░▒██▒   ░██▒ ▓█   ▓██▒▒██▒ ░  ░     ▒██▒ ░ ░ ████▓▒░░ ████▓▒░░██████▒▒██████▒▒
    ░▓  ░ ▒░   ░  ░ ▒▒   ▓▒█░▒▓▒░ ░  ░     ▒ ░░   ░ ▒░▒░▒░ ░ ▒░▒░▒░ ░ ▒░▓  ░▒ ▒▓▒ ▒ ░
     ▒ ░░  ░      ░  ▒   ▒▒ ░░▒ ░            ░      ░ ▒ ▒░   ░ ▒ ▒░ ░ ░ ▒  ░░ ░▒  ░ ░
     ▒ ░░      ░     ░   ▒   ░░            ░      ░ ░ ░ ▒  ░ ░ ░ ▒    ░ ░   ░  ░  ░
     ░         ░         ░  ░                         ░ ░      ░ ░      ░  ░      ░
    ----------------------------------   --------------------------------------------
    """

    def get_banner(self):
        return self.banner

class Arguments:
    def get_args(self):
        parser = argparse.ArgumentParser(description=__description__)
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('-c', '--check', dest='check', help='Check email valid.')
        group.add_argument('-f', '--file', dest='file', help='Input file with email for test email.', type=argparse.FileType('r'))
        group.add_argument('-e', '--email', dest='email', help='Teste email:password or email|password for test imap')
        group.add_argument('-i', '--input', dest='input', help='Input file with email:password for test imap.', type=argparse.FileType('r'))
        parser.add_argument('-o', '--output', dest='output', help='Output file log.', type=argparse.FileType('w'))
        parser.add_argument('-l', '--live', dest='live', help='Save/Append file with lives.', type=argparse.FileType('a'))
        parser.add_argument('-d', '--dead', dest='dead', help='Save/Append file with deads.', type=argparse.FileType('a'))
        parser.add_argument('-s', '--search', dest='search', help='Search in email ex: \'FROM "test@mail.com"\'')
        parser.add_argument('-dd', '--download', dest='download', help='Download attachment in /tmp/email', action='store_true')
        parser.add_argument('-t', '--thread', dest='thread', help='Execute in thread.', type=int)
        parser.add_argument('-p', '--progress', dest='progress', help='Show progress bar while processing.', action='store_true')
        parser.add_argument('--err', dest='error', help='Overwrite file input with errors.', action='store_true')
        parser.add_argument('--debug', dest='debug', help='This argument allows debugging information.', action='store_true')
        parser.add_argument('-v', '--version', dest='version', help='This argument show version.', action='version', version=__version__)

        if len(sys.argv) == 1:  # If no arguments were provided, then print help and exit.
            parser.print_help()
            sys.exit(1)

        return parser.parse_args()

class Config:
    imap_group = {
    '@gmail' : 'imap.gmail.com',
    '@yahoo' : 'imap.mail.yahoo.com',
    '@live' : 'imap-mail.outlook.com',
    '@hotmail' : 'imap-mail.outlook.com',
    '@office365' : 'outlook.office365.com',
    '@marriott' : 'mail.marriott.com',
    '@bt' : 'imap.btinternet.com',
    '@hyatt' : 'mail.hyatt.com',
    '@tvglobo': 'ms01.tvglobo.com.br',
    }
    
    error_msg = [
    'Name or service not known',
    'No address associated with hostname',
    'No route to host',
    'Temporary failure in name resolution',
    'Network is unreachable',
    ]

    if sys.platform == "linux":
        download_folder = '/tmp/email'
    else:
        download_folder = 'C:\\Users\\Public'

class Message:
    class Level:
        LIVE = 1
        DEAD = 2
        DEBUG = 3
        ERROR = 4
        WARNING = 5
        INFO = 6

    def icon_level(self, level):
        if level == self.Level.LIVE:
            return Colors.fg.lightgreen + '[+] ' + Colors.reset
        elif level == self.Level.DEAD:
            return Colors.fg.lightred + '[-] ' + Colors.reset
        elif level == self.Level.DEBUG:
            return Colors.fg.yellow + '[!] ' + Colors.reset
        elif level == self.Level.ERROR:
            return Colors.fg.yellow + '[#] ' + Colors.reset
        elif level == self.Level.WARNING:
            return Colors.fg.pink + '[*] ' + Colors.reset
        elif level == self.Level.INFO:
            return Colors.fg.lightblue + '[*] ' + Colors.reset

    def show(self, level, msg, output = False, progress = False):
        msg = self.icon_level(level) + msg
        if not msg.endswith('\n'): msg = msg + '\n'

        if not progress:
            #sys.stdout.write(time.strftime('%H:%M:%S', time.localtime()) + '\n')
            sys.stdout.write(msg)
            sys.stdout.flush()

        if output: _file_output.write(msg)

class Checker:
    def test_email(self, row, lines, raw, output = False, debug = False, progress = False):
        message = Message()
        arr_raw = re.split(r'[:;|]', raw.encode().decode('utf8'))

        ret = {
        'row' : row,
        'lines' : lines,
        'raw' : raw,
        'level' : None,
        'msg' : None,
        }

        if len(arr_raw) < 1:
            result = {
            'level' : message.Level.WARNING,
            'msg' : 'Warning: Fail split'
            }
        else:
            mail = arr_raw[0].strip()
            result = self.valid_email(mail, debug)

        #print result

        ret['level'] = result['level']
        ret['msg'] = result['msg']

        msg = '{0}/{1} - {2} - {3}'.format(row, lines, raw, ret['msg'])
        message.show(ret['level'], msg, output, progress)

        return ret

    def valid_email(self, mail, debug = False):
        message = Message()

        ret = {
        'level' : None,
        'msg' : None,
        }

        try:
            is_valid = validate_email(mail, verify=True)
            if is_valid:
                ret['level'] = message.Level.LIVE
                ret['msg'] = 'Live: Email valid'
            else:
                ret['level'] = message.Level.DEAD
                ret['msg'] = 'Dead: Email not valid'
        except Exception as e:
            ret['level'] = message.Level.ERROR
            if debug:
                ret['msg'] = 'Line: {} / Error: {}'.format(sys.exc_info()[-1].tb_lineno, e)
            else:
                ret['msg'] = 'Error: Show all errors by debug'
        finally:
            return ret

    def test_imap(self, row, lines, raw, search, download, output = False, debug = False, progress = False):
        message = Message()
        arr_raw = re.split(r'[:;|]', raw.encode('ascii', 'ignore').decode('utf8'))
        
        ret = {
        'row' : row,
        'lines' : lines,
        'raw' : raw,
        'level' : None,
        'msg' : None,
        }

        if len(arr_raw) > 1:
            mail = arr_raw[0].strip()
            password = arr_raw[1].strip()
            result = self.valid_imap(mail, password, search, download, debug)
        else:
            result = {
            'level' : message.Level.WARNING,
            'msg' : 'Warning: Fail split'
            }

        ret['level'] = result['level']
        ret['msg'] = result['msg']

        msg = '{0}/{1} - {2} - {3}'.format(row, lines, raw, ret['msg'])
        message.show(ret['level'], msg, output, progress)

        return ret

    def valid_imap(self, mail, password, search, download, debug = False):
        message = Message()
        config = Config()

        ret = {
        'level' : None,
        'msg' : None,
        }

        try:
            imap = re.search("@[\w]+", mail)
            imap = imap.group()
            host_imap = config.imap_group[imap]
        except:
            try:
                imap = re.search("@[\w.]+", mail)
                host_imap = 'imap.' + imap.group().replace("@","")
            except:
                ret['level'] = message.Level.WARNING
                ret['msg'] = 'Config IMAP - Invalid raw'
                return ret

        try:
            #imap_mail = imaplib.IMAP4_SSL(config, 993)
            imap_mail = imaplib.IMAP4_SSL(host=host_imap, port=993, timeout=60)
            result = imap_mail.login(mail, password)

            if result[0] == 'OK':
                ret_msg = ''
                if search:
                    try:
                        imap_mail.list()
                        imap_mail.select(readonly = True)
                        result, data = imap_mail.uid('search', None, '(' + search + ')')

                        if not data[0]:
                            ret_msg = 'Search not found'
                        else:
                            ret_msg = 'Search found'
                    except Exception as e:
                        ret['level'] = message.Level.ERROR
                        if debug:
                            ret['msg'] = 'Line: {} / Error: {}'.format(sys.exc_info()[-1].tb_lineno, e)
                        else:
                            ret['msg'] = 'Error: Show all errors by debug'

                if download:
                    int_down = 0
                    int_n_down = 0
                    int_n_att = 0

                    imap_mail.list()
                    imap_mail.select(readonly = True)
                    result, datas = imap_mail.uid('search', None, '(HEADER Content-Type "multipart")')
                    for data in datas:
                        items = data.split()
                        for item in items:
                            try:
                                ret_mail, message_body = imap_mail.uid('fetch', item, '(BODY.PEEK[])')
                                hash = datetime.utcnow().strftime('%Y%m%d%H%M%S')
                                result = self.save_attachment(message_body, mail + "_" + str(hash))

                                if result['level'] is None:
                                    int_down += result['int_down']
                                    int_n_down += result['int_n_down']
                                    int_n_att += result['int_n_att']
                            except Exception as e:
                                ret['level'] = message.Level.ERROR
                                if debug:
                                    ret['msg'] = 'Line: {} / Error: {}'.format(sys.exc_info()[-1].tb_lineno, e)
                                else:
                                    ret['msg'] = 'Error: Show all errors by debug'
                    if ret_msg != '':
                        ret_msg = ret_msg + ' / '
                    ret_msg = ret_msg + 'Downloading: {} | Not Downloading: {} | Not attachment: {}'.format(int_down, int_n_down, int_n_att)

                ret['level'] = message.Level.LIVE
                if ret_msg == '':
                    ret['msg'] = 'Live'
                else:
                    ret['msg'] = 'Live: ' + ret_msg
            else:
                print(result)
                ret['level'] = message.Level.DEAD
                ret['msg'] = 'Dead: {}'.format(result)

            imap_mail.logout()
        except imaplib.IMAP4.abort as e:
            ret['level'] = message.Level.ERROR
            ret['msg'] = 'Error: {}'.format(e)
        except imaplib.IMAP4.error as e:
            ret['level'] = message.Level.DEAD
            ret['msg'] = 'Dead: {}'.format(e)
        except Exception as e:
            if any(msg.lower() in str(e).lower() for msg in config.error_msg):
                ret['level'] = message.Level.DEAD
                ret['msg'] = 'Dead: {}'.format(e)
            else:
                ret['level'] = message.Level.ERROR
                ret['msg'] = 'Line: {} / Error: {}'.format(sys.exc_info()[-1].tb_lineno, e)

            if not debug:
                ret['level'] = message.Level.ERROR
                ret['msg'] = 'Error: Show all errors by debug'
        finally:
            return ret

    def save_attachment(self, msg, filename, download_folder = '/tmp/email'):
        message = Message()

        ret = {
        'level' : None,
        'msg' : None,
        'int_down' : 0,
        'int_n_down' : 0,
        'int_n_att' : 0,
        }

        try:
            body = msg[0][1]
            m = email.message_from_string(body)
            if m.get_content_maintype() != 'multipart':
                return ret

            for i, part in enumerate(m.walk()):
                if part.get_content_maintype() != 'multipart' and part.get('Content-Disposition') is not None and part.get_filename() is not None:
                    original_filename, file_extension = os.path.splitext(part.get_filename())

                    filename_full = filename + "_" + str(i) +  file_extension

                    if file_extension.lower() == ".pdf" or file_extension.lower() == ".jpg" or file_extension.lower() == ".jpeg":
                        open(download_folder + '/' + filename_full, 'wb').write(part.get_payload(decode=True))
                        ret['int_down'] += 1
                    else:
                        ret['int_n_down'] += 1
                else:
                    ret['int_n_att'] += 1
        except Exception as e:
            ret['level'] = message.Level.ERROR
            if debug:
                ret['msg'] = 'Line: {} / Error: {}'.format(sys.exc_info()[-1].tb_lineno, e)
            else:
                ret['msg'] = 'Error: Show all errors by debug'
        finally:
            return ret

def main():
    if sys.platform == "linux":
        os.system('clear')
    else:
        os.system('cls')

    # Global
    global _file_output

    # Initialize Vars
    lines = 1
    file_name = ''
    arr_ret = []

    # Initialize Class
    tstart = time.time()

    color = Colors()
    banner = Banner()
    message = Message()
    checker = Checker()
    config = Config()
 
    print(banner.get_banner())

    args = Arguments().get_args()

    # Initialize Program
    if args.output:
        _file_output = open(args.output.name, 'w')

    if args.debug:
        message.show(message.Level.DEBUG, 'Mode Debug On', args.output)

    if args.file:
        message.show(message.Level.INFO, 'File Valid Email: %s' %args.file.name, args.output)
        lines = sum(1 for line in open(args.file.name))
        message.show(message.Level.INFO, 'Total Lines: %s' %str(lines), args.output)

    if args.input:
        message.show(message.Level.INFO, 'File Input: %s' %args.input.name, args.output)
        lines = sum(1 for line in open(args.input.name))
        message.show(message.Level.INFO, 'Total Lines: %s' %str(lines), args.output)

    if args.live:
        message.show(message.Level.INFO, 'File Live: %s' %args.live.name, args.output)

    if args.dead:
        message.show(message.Level.INFO, 'File Dead: %s' %args.dead.name, args.output)

    if args.output:
        message.show(message.Level.INFO, 'File Output: %s' %args.output.name, args.output)

    if args.thread and (args.file or args.input):
        if args.thread > int(lines/2): args.thread = int(lines/2)
        if args.thread == 0: args.thread = 1
        message.show(message.Level.INFO, 'Thread: %s' %args.thread, args.output)
            
    if args.search:
        message.show(message.Level.INFO, 'Search: %s' %args.search, args.output)

    if args.download:
        if not os.path.exists(config.download_folder): os.mkdir(config.download_folder)
        message.show(message.Level.INFO, 'Download Attachment: %s' %config.download_folder, args.output)

    if args.error and (args.file or args.input):
        if args.file: file_name = args.file.name
        elif args.input: file_name = args.input.name
        message.show(message.Level.INFO, 'Overwrite %s with errors' %file_name, args.output)

    if args.progress:
        bar = Bar(Colors.fg.lightblue + '[*]' + Colors.reset + ' Loading: %(percent).1f%%', fill='#', suffix='%(index)d/%(max)d - [Elapsed:%(elapsed_td)s, Avg:%(avg)1f, Eta:%(eta)ds]', max=lines)
        bar.update()

    if args.check:
        ret = checker.test_email(1, 1, args.check, args.output, args.debug, args.progress)
        arr_ret.append(ret)
        if args.progress: bar.next()
    elif args.file:
        try:
            raw = ''
            if args.thread:
                with ThreadPoolExecutor(max_workers=args.thread) as executor:
                    futures = {}
                    for row, line in enumerate(args.file, 1):
                        raw = line.strip()
                        try:
                            future = executor.submit(checker.test_email, row, lines, raw, args.output, args.debug, args.progress)
                            futures[future] = row
                        except Exception as e:
                            message.show(message.Level.ERROR, '{}/{} - {} - Error: {}'.format(row, lines, raw, e), args.output)
                        finally:
                            if args.progress: bar.next()

                    if args.progress:
                        bar.finish()
                        bar = Bar(Colors.fg.lightblue + '[*]' + Colors.reset + ' Progress: %(percent).1f%%', fill='#', suffix='%(index)d/%(max)d - [Elapsed:%(elapsed_td)s, Avg:%(avg)1f, Eta:%(eta)ds]', max=lines)
                        bar.update()

                    for future in as_completed(futures):
                        arr_ret.append(future.result())
                        if args.progress: bar.next()
            else:
                if args.progress:
                    bar.finish()
                    bar = Bar(Colors.fg.lightblue + '[*]' + Colors.reset + ' Progress: %(percent).1f%%', fill='#', suffix='%(index)d/%(max)d - [Elapsed:%(elapsed_td)s, Avg:%(avg)1f, Eta:%(eta)ds]', max=lines)
                    bar.update()

                for row, line in enumerate(args.file, 1):
                    raw = line.strip()
                    ret = checker.test_email(row, lines, raw, args.output, args.debug, args.progress)
                    arr_ret.append(ret)
                    if args.progress: bar.next()
        except KeyboardInterrupt:
            message.show(message.Level.DEBUG, 'Keyboard Interrupt...')
        except Exception as e:
            ret = {
                'raw' : raw,
                'level' : message.Level.ERROR,
                'msg' : 'Raw: {} - Line: {} - Error: {}'.format(raw, sys.exc_info()[-1].tb_lineno, sys.exc_info()),
            }
            message.show(ret['level'], ret['msg'], args.output)
            arr_ret.append(ret)
    elif args.email:
        ret = checker.test_imap(1, 1, args.email, args.search, args.download, args.output, args.debug, args.progress)
        arr_ret.append(ret)
        if args.progress: bar.next()
    elif args.input:
        try:
            if args.thread:
                with ThreadPoolExecutor(max_workers=args.thread) as executor:
                    futures = {}
                    for row, line in enumerate(args.input, 1):
                        raw = line.strip()
                        try:
                            future = executor.submit(checker.test_imap, row, lines, raw, args.search, args.download, args.output, args.debug, args.progress)
                            futures[future] = row
                        except Exception as e:
                            if not args.progress:
                                message.show(message.Level.ERROR, '{}/{} - {} - Error: {}'.format(row, lines, raw, e), args.output)
                        finally:
                            if args.progress: bar.next()

                    if args.progress:
                        bar.finish()
                        bar = Bar(Colors.fg.lightblue + '[*]' + Colors.reset + f' Progress: %(percent).1f%%', fill='#', suffix='%(index)d/%(max)d - [Elapsed:%(elapsed_td)s, Avg:%(avg)1f, Eta:%(eta)ds]', max=lines)
                        bar.update()

                    for future in as_completed(futures):
                        arr_ret.append(future.result())
                        if args.progress: bar.next()
            else:
                if args.progress:
                    bar.finish()
                    bar = Bar(Colors.fg.lightblue + '[*]' + Colors.reset + ' Progress: %(percent).1f%%', fill='#', suffix='%(index)d/%(max)d - [Elapsed:%(elapsed_td)s, Avg:%(avg)1f, Eta:%(eta)ds]', max=lines)
                    bar.update()

                for row, line in enumerate(args.input, 1):
                    raw = line.strip()
                    ret = checker.test_imap(row, lines, raw, args.search, args.download, args.output, args.debug, args.progress)
                    arr_ret.append(ret)
                    if args.progress: bar.next()
        except KeyboardInterrupt:
                message.show(message.Level.DEBUG, 'Keyboard Interrupt...')
        except Exception as e:
            ret = {
                'raw' : raw,
                'level' : message.Level.ERROR,
                'msg' : 'Raw: {} - Line: {} - Error: {}'.format(raw, sys.exc_info()[-1].tb_lineno, sys.exc_info()),
            }
            message.show(ret['level'], ret['msg'], args.output)
            arr_ret.append(ret)

    if args.progress: bar.finish()

    t_live, t_dead, t_error = 0, 0, 0

    if len(arr_ret) > 0:
        if args.live or args.dead or args.error:
            message.show(message.Level.INFO, 'Save All files', args.output)

        if args.live: file_live = open(args.live.name, 'a')
        if args.dead: file_dead = open(args.dead.name, 'a')
        if args.error and (args.file or args.input): file_error = open(file_name, 'w')

        for ret in arr_ret:
            if ret['level'] is message.Level.LIVE: t_live+=1
            elif ret['level'] is message.Level.DEAD: t_dead+=1
            elif ret['level'] is message.Level.ERROR: t_error+=1

            if args.live and ret['level'] is message.Level.LIVE:
                file_live.write(ret['raw']+'\n')
            elif args.dead and ret['level'] is message.Level.DEAD:
                file_dead.write(ret['raw']+'\n')
            elif args.error and (args.file or args.input) and ret['level'] is message.Level.ERROR:
                file_error.write(ret['raw']+'\n')

        if args.live: file_live.close()
        if args.dead: file_dead.close()
        if args.error and (args.file or args.input): file_error.close()

    message.show(message.Level.INFO, 'Total Live: {0}'.format(t_live), args.output)
    message.show(message.Level.INFO, 'Total Dead: {0}'.format(t_dead), args.output)
    message.show(message.Level.INFO, 'Total Error: {0}'.format(t_error), args.output)

    tend = time.time()
    hours, rem = divmod(tend-tstart, 3600)
    minutes, seconds = divmod(rem, 60)
    message.show(message.Level.INFO, 'Time Elapsed: {:0>2}:{:0>2}:{:05.2f}'.format(int(hours),int(minutes),seconds), args.output)

    if args.output: _file_output.close()

if __name__ == '__main__':
    main()
