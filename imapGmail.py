import imaplib,sys
box = imaplib.IMAP4_SSL('imap.gmail.com', 993)
box.login("user@mail.com","passwrod")
box.select('inbox')
typ, data = box.search(None, 'ALL')
cont = 1
for num in data[0].split():
	print num	
	box.store(num, '+X-GM-LABELS', '\\Trash')
box.expunge()
box.close()
box.logout()


