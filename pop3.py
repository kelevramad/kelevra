#!/usr/bin/python
# -*- coding: utf-8 -*-

import poplib

try:
	user = 'sonohara@bol.com.br'
	pwd = 'edu751216'
	box = poplib.POP3_SSL('pop3.bol.com.br', '995')
	box.user(user)
	auth = box.pass_(pwd)

	print "[+] chekcing {0} valid, reason:{1}".format(user, str(auth))

	numMessages = len(box.list()[1])
	for i in range(numMessages):
		for msg in box.retr(i+1)[1]:
		    print msg

	box.quit()

except Exception as error:
	print "[!] chekcing {0} failed, reason:{1}".format(user, str(error))



