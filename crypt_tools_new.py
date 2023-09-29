#!/usr/bin/python
# coding: utf-8

import os
import sys
import time
import zlib
import json
import base64
import random
import hashlib
import argparse
import animation
import threading
import itertools


from Crypto import Random
from Crypto.Cipher import AES

__author__ = "Center For Cyber Intelligence - Central Intelligence Agency"
__description__ = "Crypt Tools"
__version__ = __description__ + " 1.0.0"

BLOCK_SIZE = 16

class Arguments:
    def __init__(self):
        pass

    def get_args(self):
    	parser = argparse.ArgumentParser(description=__description__)
    	parser.add_argument('-m', '--mode', dest='mode', help='Option crypt or decrypt [default: crypt]', default='crypt', choices=['crypt','decrypt'])
    	group = parser.add_mutually_exclusive_group(required=True)
    	group.add_argument('-t', '--text', dest='text', help='Plain-text for crypt/decrypt')
    	group.add_argument('-i', '--input', dest='input', help='Input file for crypt/decrypt.', type=argparse.FileType('r'), nargs='*')
    	parser.add_argument('-o', '--output', dest='output', help='Output file for crypt/decrypt.', type=argparse.FileType('w'))
    	parser.add_argument('-p', '--password', dest='password', help='Password for crypt.', required=True)
    	parser.add_argument('-c', '--compress', dest='compress', help='Compress file before crypt/decompress after decrypt.', action='store_true')
    	parser.add_argument('-d', '--debug', dest='debug', help='This argument allows debugging information.', action='store_true')
    	parser.add_argument('-v', '--version', dest='version', help='This argument show version.', action='version', version=__version__)

    	if len(sys.argv) == 1:  # If no arguments were provided, then print help and exit.
    		parser.print_help()
    		sys.exit(1)

    	return parser.parse_args()

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
    banner = ["""
      /$$$$$$                                  /$$           /$$$$$$$$                  /$$
     /$$__  $$                                | $$          |__  $$__/                 | $$
    | $$  \__/  /$$$$$$  /$$   /$$  /$$$$$$  /$$$$$$           | $$  /$$$$$$   /$$$$$$ | $$  /$$$$$$$
    | $$       /$$__  $$| $$  | $$ /$$__  $$|_  $$_/           | $$ /$$__  $$ /$$__  $$| $$ /$$_____/
    | $$      | $$  \__/| $$  | $$| $$  \ $$  | $$             | $$| $$  \ $$| $$  \ $$| $$|  $$$$$$
    | $$    $$| $$      | $$  | $$| $$  | $$  | $$ /$$         | $$| $$  | $$| $$  | $$| $$ \____  $$
    |  $$$$$$/| $$      |  $$$$$$$| $$$$$$$/  |  $$$$/         | $$|  $$$$$$/|  $$$$$$/| $$ /$$$$$$$/
     \______/ |__/       \____  $$| $$____/    \___/           |__/ \______/  \______/ |__/|_______/
                         /$$  | $$| $$
                        |  $$$$$$/| $$
                         \______/ |__/
    ""","""
       ÛÛÛÛÛÛÛÛÛ                                  ÛÛÛÛÛ       ÛÛÛÛÛÛÛÛÛÛÛ                   ÛÛÛÛ
      ÛÛÛ°°°°°ÛÛÛ                                °°ÛÛÛ       °Û°°°ÛÛÛ°°°Û                  °°ÛÛÛ
     ÛÛÛ     °°°  ÛÛÛÛÛÛÛÛ  ÛÛÛÛÛ ÛÛÛÛ ÛÛÛÛÛÛÛÛ  ÛÛÛÛÛÛÛ     °   °ÛÛÛ  °   ÛÛÛÛÛÛ   ÛÛÛÛÛÛ  °ÛÛÛ   ÛÛÛÛÛ
    °ÛÛÛ         °°ÛÛÛ°°ÛÛÛ°°ÛÛÛ °ÛÛÛ °°ÛÛÛ°°ÛÛÛ°°°ÛÛÛ°          °ÛÛÛ     ÛÛÛ°°ÛÛÛ ÛÛÛ°°ÛÛÛ °ÛÛÛ  ÛÛÛ°°
    °ÛÛÛ          °ÛÛÛ °°°  °ÛÛÛ °ÛÛÛ  °ÛÛÛ °ÛÛÛ  °ÛÛÛ           °ÛÛÛ    °ÛÛÛ °ÛÛÛ°ÛÛÛ °ÛÛÛ °ÛÛÛ °°ÛÛÛÛÛ
    °°ÛÛÛ     ÛÛÛ °ÛÛÛ      °ÛÛÛ °ÛÛÛ  °ÛÛÛ °ÛÛÛ  °ÛÛÛ ÛÛÛ       °ÛÛÛ    °ÛÛÛ °ÛÛÛ°ÛÛÛ °ÛÛÛ °ÛÛÛ  °°°°ÛÛÛ
     °°ÛÛÛÛÛÛÛÛÛ  ÛÛÛÛÛ     °°ÛÛÛÛÛÛÛ  °ÛÛÛÛÛÛÛ   °°ÛÛÛÛÛ        ÛÛÛÛÛ   °°ÛÛÛÛÛÛ °°ÛÛÛÛÛÛ  ÛÛÛÛÛ ÛÛÛÛÛÛ
      °°°°°°°°°  °°°°°       °°°°°ÛÛÛ  °ÛÛÛ°°°     °°°°°        °°°°°     °°°°°°   °°°°°°  °°°°° °°°°°°
                             ÛÛÛ °ÛÛÛ  °ÛÛÛ
                            °°ÛÛÛÛÛÛ   ÛÛÛÛÛ
                             °°°°°°   °°°°°
    ""","""

      ,ad8888ba,                                               888888888888                    88
     d8"'    `"8b                                     ,d            88                         88
    d8'                                               88            88                         88
    88            8b,dPPYba, 8b       d8 8b,dPPYba, MM88MMM         88  ,adPPYba,   ,adPPYba,  88 ,adPPYba,
    88            88P'   "Y8 `8b     d8' 88P'    "8a  88            88 a8"     "8a a8"     "8a 88 I8[    ""
    Y8,           88          `8b   d8'  88       d8  88            88 8b       d8 8b       d8 88  `"Y8ba,
     Y8a.    .a8P 88           `8b,d8'   88b,   ,a8"  88,           88 "8a,   ,a8" "8a,   ,a8" 88 aa    ]8I
      `"Y8888Y"'  88             Y88'    88`YbbdP"'   "Y888         88  `"YbbdP"'   `"YbbdP"'  88 `"YbbdP"'
                                 d8'     88
                                d8'      88
    ""","""
     ██████╗██████╗ ██╗   ██╗██████╗ ████████╗    ████████╗ ██████╗  ██████╗ ██╗     ███████╗
    ██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
    ██║     ██████╔╝ ╚████╔╝ ██████╔╝   ██║          ██║   ██║   ██║██║   ██║██║     ███████╗
    ██║     ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║          ██║   ██║   ██║██║   ██║██║     ╚════██║
    ╚██████╗██║  ██║   ██║   ██║        ██║          ██║   ╚██████╔╝╚██████╔╝███████╗███████║
     ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝          ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝
    """]

    def __init__(self):
        pass

    def get_banner(self):
        return self.__class__.banner[random.randint(0,len(self.__class__.banner)-1)]

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

    def show(self, level, msg):
        msg = self.icon_level(level) + msg
        if not msg.endswith('\n'): msg = msg + '\n'

        #sys.stdout.write(time.strftime('%H:%M:%S', time.localtime()) + '\n')
        sys.stdout.write(msg)
        sys.stdout.flush()

class Crypt():
    def __init__(self):
        pass
        
    def trans(self, key):
         return hashlib.md5(key.encode()).digest()

    def humansize(self, nbytes):
        suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
        i = 0
        while nbytes >= 1024 and i < len(suffixes)-1:
            nbytes /= 1024.
            i += 1
        f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
        return '%s %s' % (f, suffixes[i])

    @animation.wait(animation='bar', text='Waiting...')
    def encryption(self, plain_text, password):
        message = Message()
        try:
            IV = Random.new().read(BLOCK_SIZE)
            aes = AES.new(self.trans(password), AES.MODE_CFB, IV)
            encode = base64.b64encode(IV + aes.encrypt(plain_text))
            return encode
        except Exception as e:
            message.show(message.Level.DEAD, 'Error encryption message')
            message.show(message.Level.DEAD, 'Line: {} / Error: {}'.format(sys.exc_info()[-1].tb_lineno, e))
            return ''

    @animation.wait(animation='bar', text='Waiting...')
    def decryption(self, encrypted, password):
        message = Message()
        try:
            encrypted = base64.b64decode(encrypted)
            IV = encrypted[:BLOCK_SIZE]
            aes = AES.new(self.trans(password), AES.MODE_CFB, IV)
            decode = aes.decrypt(encrypted[BLOCK_SIZE:])
            return decode
        except:
            message.show(message.Level.DEAD, 'Error decryption message')
            message.show(message.Level.DEAD, 'Unexpected error: {}'.format(sys.exc_info()))
            return ''

    @animation.wait(animation='bar', text='Waiting...')
    def load_file(self, file_input):
        return open(file_input, 'rb').read()

    @animation.wait(animation='bar', text='Waiting...')
    def compress(self, content):
        return zlib.compress(content, 9)

    @animation.wait(animation='bar', text='Waiting...')
    def decompress(self, content):
        return zlib.decompress(content)

    @animation.wait(animation='bar', text='Waiting...')
    def write_file(self, file_output, content):
        file_write = open(file_output, 'wb')
        file_write.write(content)
        file_write.close()
        return

    def encrypt_file(self, file_input, file_output, password, compress):
        message = Message()
        message.show(message.Level.LIVE, 'Loading file/size: {}/{}'.format(file_input, self.humansize(os.path.getsize(file_input))))
        file_load = self.load_file(file_input)

        if compress:
            message.show(message.Level.LIVE, 'Compress content file: {}'.format(file_input))
            file_load = self.compress(file_load)

        message.show(message.Level.LIVE, 'Encryption content - OK')
        file_encrypt = self.encryption(file_load, password)

        message.show(message.Level.LIVE, 'Write encryption file: {}'.format(file_output))
        self.write_file(file_output, file_encrypt)
        return

    def decrypt_file(self, file_input, file_output, password, compress):
        message = Message()
        message.show(message.Level.LIVE, 'Loading file/size: {}/{}'.format(file_input, self.humansize(os.path.getsize(file_input))))
        file_load = self.load_file(file_input)

        message.show(message.Level.LIVE, 'Decryption content - OK')
        file_decrypt = self.decryption(file_load, password)

        if compress:
            try:
                message.show(message.Level.LIVE, 'Decompress content file: {}'.format(file_input))
                file_decrypt = self.decompress(file_decrypt)
            except:
                message.show(message.Level.DEAD, 'Error decompress content file: {}'.format(file_output))
                message.show(message.Level.DEAD, 'Unexpected error: {}'.format(sys.exc_info()))
                exit(0)

        message.show(message.Level.LIVE, 'Write plain-text file: {}'.format(file_output))
        self.write_file(file_output, file_decrypt)
        return

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
    crypt = Crypt()

    print(random.choice(list(color.fg.__dict__.values())[1:-3]) + banner.get_banner() + color.reset)

    args = Arguments().get_args()

    # Initialize Program
    if args.output:
        _file_output = open(args.output.name, 'w')

    if args.debug:
        message.show(message.Level.DEBUG, 'Mode Debug On')

    if args.mode == 'crypt':
        message.show(message.Level.LIVE, 'Encryption Start')
        message.show(message.Level.LIVE, 'Password: {}'.format(args.password))
        message.show(message.Level.LIVE, 'Password Encrypted: {}'.format(crypt.trans(args.password).hex()))
        if args.text:
            enc = crypt.encryption(args.text.encode(), args.password)
            message.show(message.Level.LIVE, 'Message Plain-Text: {}'.format(args.text))
            message.show(message.Level.LIVE, 'Message Encrypted: {}'.format(enc.decode('utf8')))
        elif args.input:
            for f in args.input:
                if len(args.input) > 1 or args.output is None: file_output = os.path.splitext(f.name)[0] + '.enc'
                else: file_output = args.output.name
                crypt.encrypt_file(f.name, file_output, args.password, args.compress)
    else:
        message.show(message.Level.LIVE, 'Decryption Start')
        message.show(message.Level.LIVE, 'Password: {}'.format(args.password))
        message.show(message.Level.LIVE, 'Password Encrypted: {}'.format(crypt.trans(args.password).hex()))
        if args.text:
            dec = crypt.decryption(args.text, args.password)
            message.show(message.Level.LIVE, 'Message Encrypted: {}'.format(args.text))
            message.show(message.Level.LIVE, 'Message Plain-Text: {}'.format(dec))
        elif args.input:
            for f in args.input:
                if len(args.input) > 1 or args.output is None: file_output = os.path.splitext(f.name)[0] + '.dec'
                else: file_output = args.output.name
                crypt.decrypt_file(f.name, file_output, args.password, args.compress)

    tend = time.time()
    hours, rem = divmod(tend-tstart, 3600)
    minutes, seconds = divmod(rem, 60)
    message.show(message.Level.INFO, 'Time Elapsed: {:0>2}:{:0>2}:{:05.2f}'.format(int(hours),int(minutes),seconds))

if __name__ == '__main__':
	main()
