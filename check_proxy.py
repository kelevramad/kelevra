#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import sys
import time
import random
import urllib3
import argparse
import requests

from progress.bar import Bar
from proxy_checker import ProxyChecker
from concurrent.futures import ThreadPoolExecutor, as_completed

__author__ = "Center For Cyber Intelligence - Central Intelligence Agency"
__version__ = "1.0.0"
__description__ = "Check Proxy"


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
  /$$$$$$  /$$                           /$$             /$$$$$$$
 /$$__  $$| $$                          | $$            | $$__  $$
| $$  \__/| $$$$$$$   /$$$$$$   /$$$$$$$| $$   /$$      | $$  \ $$ /$$$$$$   /$$$$$$  /$$   /$$ /$$   /$$
| $$      | $$__  $$ /$$__  $$ /$$_____/| $$  /$$/      | $$$$$$$//$$__  $$ /$$__  $$|  $$ /$$/| $$  | $$
| $$      | $$  \ $$| $$$$$$$$| $$      | $$$$$$/       | $$____/| $$  \__/| $$  \ $$ \  $$$$/ | $$  | $$
| $$    $$| $$  | $$| $$_____/| $$      | $$_  $$       | $$     | $$      | $$  | $$  >$$  $$ | $$  | $$
|  $$$$$$/| $$  | $$|  $$$$$$$|  $$$$$$$| $$ \  $$      | $$     | $$      |  $$$$$$/ /$$/\  $$|  $$$$$$$
 \______/ |__/  |__/ \_______/ \_______/|__/  \__/      |__/     |__/       \______/ |__/  \__/ \____  $$
                                                                                                /$$  | $$
                                                                                               |  $$$$$$/
                                                                                                \______/     """

    def __init__(self):
        pass

    def get_banner(self):
        return self.banner

class Arguments:
    def get_args(self):
        parser = argparse.ArgumentParser(description=__description__)
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('-p', '--proxy', dest='proxy', help='Teste proxy TYPE|IP:PORT ex: socks4|100.100.100.100:8080.')
        group.add_argument('-i', '--input', dest='input', help='Input file with TYPE|IP:PORT ex: https|100.100.100.100:8080.', type=argparse.FileType('r'))
        parser.add_argument('-u', '--url', dest='url', help='URL to test.')
        parser.add_argument('-l', '--live', dest='live', help='Save/Append file with lives.', type=argparse.FileType('a'))
        parser.add_argument('-d', '--dead', dest='dead', help='Save/Append file with deads.', type=argparse.FileType('a'))
        parser.add_argument('-o', '--output', dest='output', help='Output file log.', type=argparse.FileType('w'))
        parser.add_argument('-t', '--thread', dest='thread', help='Execute in thread.', type=int)
        parser.add_argument('--timeout', dest='timeout', help='Timeout connection requests.', type=int)
        parser.add_argument('--progress', dest='progress', help='Show progress bar while processing.', action='store_true')
        parser.add_argument('-e', '--err', dest='error', help='Overwrite file input with errors.', action='store_true')
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

    def __init__(self):
        pass

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
            sys.stdout.write(msg)
            sys.stdout.flush()

        if output: _file_output.write(msg)

class Checker:
    def __init__(self):
        pass

    def proxy_obs(self, row, lines, raw, timeout, url, output = False, debug = False):
        ret = {
        'row' : row,
        'lines' : lines,
        'raw' : raw,
        'level' : None,
        'msg' : None,
        }

        message = Message()

        arr_raw = []
        arr_raw = raw.split('|')
        arr_raw[0] = arr_raw[0].lower()

        if len(arr_raw) < 2:
            ret['level'] = message.Level.DEAD
            ret['msg'] = 'Fail split'
        elif arr_raw[0] not in ['http','https','socks4','socks5']:
            ret['level'] = message.Level.DEAD
            ret['msg'] = 'Error: Type not allowed'
        elif not re.findall(r'[0-9]+(?:\.[0-9]+){3}:[0-9]+', arr_raw[1]):
            ret['level'] = message.Level.DEAD
            ret['msg'] = 'Error: IP:PORT not valid'
        else:
            #proxies = {'http' : arr_raw[1], 'https' : arr_raw[1], 'socks4' : arr_raw[1], 'socks5' : arr_raw[1],}
            #proxies = {'http' : 'http://' + arr_raw[1]}
            proxies = dict(http = arr_raw[0] + '://' + arr_raw[1], https = arr_raw[0] + '://' + arr_raw[1])
            try:
                r = requests.get(url, proxies=proxies, timeout=timeout)
                if url == 'https://api.ipify.org?format=json':
                    #print r_json['ip']
                    #print arr_raw[1].split(':')[0]
                    r_json = r.json()
                    ret['level'] = message.Level.LIVE
                    ret['msg'] = 'Live - Match {}'.format(True if r_json['ip'] == arr_raw[1].split(':')[0] else False)
                else:
                    ret['level'] = message.Level.LIVE
                    ret['msg'] = 'Live'
            except requests.exceptions.ConnectionError as e:
                ret['level'] = message.Level.ERROR
                if debug:
                    ret['msg'] = 'Error - ConnectionError: %s' %e
                else:
                    ret['msg'] = 'Error: Show all errors by debug'
            except requests.exceptions.ConnectTimeout as e:
                ret['level'] = message.Level.ERROR
                if debug:
                    ret['msg'] = 'Error - ConnectTimeout: %s' %e
                else:
                    ret['msg'] = 'Error: Show all errors by debug'
            except requests.exceptions.HTTPError as e:
                ret['level'] = message.Level.ERROR
                if debug:
                    ret['msg'] = 'Error - HTTPError: %s' %e
                else:
                    ret['msg'] = 'Error: Show all errors by debug'
            except requests.exceptions.Timeout as e:
                ret['level'] = message.Level.ERROR
                if debug:
                    ret['msg'] = 'Error - Timeout: %s' %e
                else:
                    ret['msg'] = 'Error: Show all errors by debug'
            except urllib3.exceptions.ProxySchemeUnknown as e:
                ret['level'] = message.Level.ERROR
                if debug:
                    ret['msg'] = 'Error - ProxySchemeUnknown: %s' %e
                else:
                    ret['msg'] = 'Error: Show all errors by debug'
            except Exception as e:
                ret['level'] = message.Level.ERROR
                if debug:
                    ret['msg'] = 'Error - Exception: %s' %e
                else:
                    ret['msg'] = 'Error: Show all errors by debug'

        msg = '{0}/{1} - {2} - {3}'.format(row, lines, raw, ret['msg'])
        message.show(ret['level'], msg, output)

        return ret

    def proxy(self, row, lines, raw, timeout, url, output = False, debug = False, progress = False):
        ret = {
        'row' : row,
        'lines' : lines,
        'raw' : raw,
        'level' : None,
        'msg' : None,
        'protocols' : None,
        'anonymity' : None,
        'timeout' : None,
        'country' : None,
        'country_code' : None,
        }
        
        message = Message()
        
        try:
            checker = ProxyChecker()
            result = checker.check_proxy(raw)
            if result:
                ret['protocols'] = result['protocols']
                ret['anonymity'] = result['anonymity']
                ret['timeout'] = result['timeout']
                ret['country'] = result['country']
                ret['country_code'] = result['country_code']
                ret['level'] = message.Level.LIVE
                ret['msg'] = 'Live - {}/{} - {} - {} - timeout: {}'.format(ret['country_code'], ret['country'], ret['anonymity'], ret['protocols'], ret['timeout'])
            else:
                ret['level'] = message.Level.DEAD
                ret['msg'] = 'Dead: Failed test'
        except Exception as e:
            ret['level'] = message.Level.ERROR
            if debug:
                ret['msg'] = 'Error - Exception: %s' %e
            else:
                ret['msg'] = 'Error: Show all errors by debug'

        msg = '{0}/{1} - {2} - {3}'.format(row, lines, raw, ret['msg'])
        message.show(ret['level'], msg, output, progress)

        return ret

def main():
    if sys.platform == "linux":
        os.system('clear')
    else:
        os.system('cls')

    # Global
    global _file_output

    # Initialize Vars
    lines = 0
    arr_ret = []
    tstart = time.time()

    # Initialize Class
    color = Colors()
    banner = Banner()
    message = Message()
    checker = Checker()

    print(banner.get_banner())

    args = Arguments().get_args()

    # Initialize Program
    if args.output:
        _file_output = open(args.output.name, 'w')

    if args.debug:
        message.show(message.Level.DEBUG, 'Mode Debug On', args.output)

    if args.input:
        message.show(message.Level.INFO, 'File Input: %s' %args.input.name, args.output)
        lines = sum(1 for line in open(args.input.name))
        message.show(message.Level.INFO, 'Total Lines: %s' %str(lines), args.output)

    if args.url:
        message.show(message.Level.INFO, 'URL: %s' %args.url, args.output)
    else:
        args.url = 'https://api.ipify.org?format=json'

    if args.live:
        message.show(message.Level.INFO, 'File Live: %s' %args.live.name, args.output)

    if args.dead:
        message.show(message.Level.INFO, 'File Dead: %s' %args.dead.name, args.output)

    if args.output:
        message.show(message.Level.INFO, 'File Output: %s' %args.output.name, args.output)

    if args.thread and args.input:
        if args.thread > int(lines/4): args.thread = int(lines/4)
        if args.thread == 0: args.thread = 1
        message.show(message.Level.INFO, 'Thread: %s' %args.thread, args.output)

    if args.error and args.input:
        message.show(message.Level.INFO, 'Overwrite %s with errors' %args.input.name, args.output)

    if args.progress:
        bar = Bar(Colors.fg.lightblue + '[*]' + Colors.reset + ' Loading: %(percent).1f%%', fill='#', suffix='%(index)d/%(max)d - [Elapsed:%(elapsed_td)s, Avg:%(avg)1f, Eta:%(eta)ds]', max=lines)
        bar.update()

    if args.timeout:
        message.show(message.Level.INFO, 'Timeout: %s' %args.timeout, args.output)
        timeout = args.timeout
    else:
        timeout = (3.05,27)

    if args.proxy:
        ret = checker.proxy(1, 1, args.proxy, timeout, args.url, args.output, args.debug, args.progress)
        arr_ret.append(ret)
    elif args.input:
        try:
            raw = ''
            if args.thread:
                with ThreadPoolExecutor(max_workers=args.thread) as executor:
                    futures = {}
                    for row, line in enumerate(args.input, 1):
                        raw = line.strip()
                        try:
                            future = executor.submit(checker.proxy, row, lines, raw, timeout, args.url, args.output, args.debug, args.progress)
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

                for row, line in enumerate(args.input, 1):
                    raw = line.strip()
                    ret = checker.proxy(row, lines, raw, timeout, args.url, args.output, args.debug, args.progress)
                    arr_ret.append(ret)
                    if args.progress: bar.next()
        except KeyboardInterrupt:
            message.show(message.Level.DEBUG, 'Keyboard Interrupt...', args.output)
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
        if args.live or args.dead:
            message.show(message.Level.INFO, 'Save All files', args.output)

        if args.live: file_live = open(args.live.name, 'a')
        if args.dead: file_dead = open(args.dead.name, 'a')
        if args.error and args.input: file_error = open(args.input.name, 'w')

        for ret in arr_ret:
            if ret['level'] is message.Level.LIVE: t_live+=1
            elif ret['level'] is message.Level.DEAD: t_dead+=1
            elif ret['level'] is message.Level.ERROR: t_error+=1

            if args.live and ret['level'] is message.Level.LIVE:
                for protocol in ret['protocols']:
                    file_live.write(protocol+' '+ret['raw']+'\n')
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
