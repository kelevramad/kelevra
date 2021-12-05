#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import sys
import time
import smtplib
import argparse

from progress.bar import Bar
from validate_email import validate_email
from concurrent.futures import ThreadPoolExecutor, as_completed

__author__ = "Center For Cyber Intelligence - Central Intelligence Agency"
__version__ = "1.0.0"
__description__ = "Test E-mails"

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
        __    _                               ______                _ __    
       / /   (_)___ ___  ____  ____ ______   / ____/___ ___  ____ _(_) /____
      / /   / / __ `__ \/ __ \/ __ `/ ___/  / __/ / __ `__ \/ __ `/ / / ___/
     / /___/ / / / / / / /_/ / /_/ / /     / /___/ / / / / / /_/ / / (__  ) 
    /_____/_/_/ /_/ /_/ .___/\__,_/_/     /_____/_/ /_/ /_/\__,_/_/_/____/  
                     /_/                                                    
    """

    def get_banner(self):
        return self.banner

class Arguments:
    def get_args(self):
        parser = argparse.ArgumentParser(description=__description__)
        parser.add_argument('-i', '--input', dest='input', help='Input file with email:password for test imap.', type=argparse.FileType('r'))
        parser.add_argument('-o', '--output', dest='output', help='Output file log.', type=argparse.FileType('w'))
        parser.add_argument('-l', '--live', dest='live', help='Save/Append file with lives.', type=argparse.FileType('a'))
        parser.add_argument('-d', '--dead', dest='dead', help='Save/Append file with deads.', type=argparse.FileType('a'))
        parser.add_argument('-t', '--thread', dest='thread', help='Execute in thread.', type=int)
        parser.add_argument('-p', '--progress', dest='progress', help='Show progress bar while processing.', action='store_true')
        parser.add_argument('--err', dest='error', help='Overwrite file input with errors.', action='store_true')
        parser.add_argument('--debug', dest='debug', help='This argument allows debugging information.', action='store_true')
        parser.add_argument('-v', '--version', dest='version', help='This argument show version.', action='version', version=__version__)

        if len(sys.argv) == 1:  # If no arguments were provided, then print help and exit.
            parser.print_help()
            sys.exit(1)

        return parser.parse_args()

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

class TestEmail:
    def test_email(self, row, lines, raw, output = False, debug = False, progress = False):
        message = Message()
        raw = raw.encode('ascii', 'ignore').decode('utf8')
        arr_raw = re.split(r'[:;|]', raw)
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        ret = {
        'row' : row,
        'lines' : lines,
        'raw' : raw,
        'level' : None,
        'msg' : None,
        }
        
        if len(arr_raw) <= 1:
            ret['level'] = message.Level.WARNING
            ret['msg'] = 'Warning: Fail split'
        else:
            if arr_raw[0].strip() is None or arr_raw[1].strip() is None or arr_raw[0].strip() == '' or arr_raw[1].strip() == '':
                ret['level'] = message.Level.DEAD
                ret['msg'] = 'Dead: Email or Password is null'
            elif re.fullmatch(regex, arr_raw[0].strip()):
                mail = arr_raw[0].strip().lower()
                password = arr_raw[1].strip()
                mail = self.sanitize_mail(mail, output, progress)
                ret['raw'] = mail+'|'+password
                ret['level'] = message.Level.LIVE
                ret['msg'] = 'Live: Email valid'
            elif re.fullmatch(regex, arr_raw[1].strip()):
                mail = arr_raw[1].strip().lower()
                password = arr_raw[0].strip()
                mail = self.sanitize_mail(mail, output, progress)
                ret['raw'] = mail+'|'+password
                ret['level'] = message.Level.LIVE
                ret['msg'] = 'Live: Email valid'
            else:
                ret['level'] = message.Level.DEAD
                ret['msg'] = 'Dead: Email not valid'

        msg = '{0}/{1} - {2} - {3}'.format(row, lines, ret['raw'], ret['msg'])
        message.show(ret['level'], msg, output, progress)

        return ret
        
    def sanitize_mail(self, mail, output, progress):
        domain_mail = {
        '@gmail' : '@gmail.com',
        '@uol' : '@uol.com.br',
        '@bol' : '@bol.com.br',
        '@terra' : '@terra.com.br',
        '@globo' : '@globo.com',
        }
        
        try:
            domain = re.search("@[\w]+", mail)
            if domain_mail[domain.group()]:
                arr_ret = mail.split('@')
                mail = arr_ret[0] + domain_mail[domain.group()]
        except Exception as e:
            pass

        return mail
    
def main():
    if sys.platform == "linux":
        os.system('clear')
    else:
        os.system('cls')

    # Global
    global _file_output

    # Initialize Vars
    t_lines = 0
    lines = []
    arr_ret = []

    # Initialize Class
    tstart = time.time()

    color = Colors()
    banner = Banner()
    message = Message()
    testEmail = TestEmail()
 
    print(banner.get_banner())

    args = Arguments().get_args()

       # Initialize Program
    if args.output:
        _file_output = open(args.output.name, 'w')

    if args.debug:
        message.show(message.Level.DEBUG, 'Mode Debug On', args.output)

    if args.input:
        message.show(message.Level.INFO, 'File Input: %s' %args.input.name, args.output)
        with open(args.input.name, encoding = 'ISO-8859-1') as file_input:
            lines = file_input.readlines()

        lines = list(dict.fromkeys(lines))
        message.show(message.Level.INFO, 'Remove Duplicate Lines...', args.output)

        t_lines = len(lines)
        message.show(message.Level.INFO, 'Total Lines: %s' %t_lines, args.output)

    if args.live:
        message.show(message.Level.INFO, 'File Live: %s' %args.live.name, args.output)

    if args.dead:
        message.show(message.Level.INFO, 'File Dead: %s' %args.dead.name, args.output)

    if args.output:
        message.show(message.Level.INFO, 'File Output: %s' %args.output.name, args.output)

    if args.thread and args.input:
        if args.thread > int(t_lines/2): args.thread = int(t_lines/2)
        if args.thread == 0: args.thread = 1
        message.show(message.Level.INFO, 'Thread: %s' %args.thread, args.output)

    if args.error and args.input:
        message.show(message.Level.INFO, 'Overwrite %s with errors' %args.input.name, args.output)

    if args.progress:
        bar = Bar(Colors.fg.lightblue + '[*]' + Colors.reset + ' Loading: %(percent).1f%%', fill='#', suffix='%(index)d/%(max)d - [Elapsed:%(elapsed_td)s, Avg:%(avg)1f, Eta:%(eta)ds]', max=t_lines)
        bar.update()
        
    if args.input:
        try:
            raw = ''
            if args.thread:
                with ThreadPoolExecutor(max_workers=args.thread) as executor:
                    futures = {}
                    for row, line in enumerate(lines, 1):
                        raw = line.strip()
                        try:
                            future = executor.submit(testEmail.test_email, row, t_lines, raw, args.output, args.debug, args.progress)
                            futures[future] = row
                        except Exception as e:
                            message.show(message.Level.ERROR, '{}/{} - {} - Error: {}'.format(row, t_lines, raw, e), args.output)
                        finally:
                            if args.progress: bar.next()

                    if args.progress:
                        bar.finish()
                        bar = Bar(Colors.fg.lightblue + '[*]' + Colors.reset + ' Progress: %(percent).1f%%', fill='#', suffix='%(index)d/%(max)d - [Elapsed:%(elapsed_td)s, Avg:%(avg)1f, Eta:%(eta)ds]', max=t_lines)
                        bar.update()
                        
                    for future in as_completed(futures):
                        arr_ret.append(future.result())
                        if args.progress: bar.next()
            else:
                if args.progress:
                    bar.finish()
                    bar = Bar(Colors.fg.lightblue + '[*]' + Colors.reset + ' Progress: %(percent).1f%%', fill='#', suffix='%(index)d/%(max)d - [Elapsed:%(elapsed_td)s, Avg:%(avg)1f, Eta:%(eta)ds]', max=t_lines)
                    bar.update()

                for row, line in enumerate(lines, 1):
                    raw = line.strip()
                    ret = testEmail.test_email(row, t_lines, raw, args.output, args.debug, args.progress)
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
        if args.error and args.input: file_error = open(args.input.name, 'w')

        for ret in arr_ret:
            if ret['level'] is message.Level.LIVE: t_live+=1
            elif ret['level'] is message.Level.DEAD: t_dead+=1
            elif ret['level'] is message.Level.ERROR: t_error+=1

            if args.live and ret['level'] is message.Level.LIVE:
                file_live.write(ret['raw']+'\n')
            elif args.dead and ret['level'] is message.Level.DEAD:
                file_dead.write(ret['raw']+'\n')
            elif args.error and args.input and ret['level'] is message.Level.ERROR:
                file_error.write(ret['raw']+'\n')

        if args.live: file_live.close()
        if args.dead: file_dead.close()
        if args.error and args.input: file_error.close()

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
