#!/usr/bin/env python

import imaplib
import sys

default = {
	'host': 'imap.gmail.com',
	'port': '993',
}

def gmail_login(username, password):
	ret = imaplib.IMAP4_SSL(default['host'], default['port'])
	ret.login(username, password)
	return ret

def main(username, password):

	imap = gmail_login(username, password)
	status, data = imap.select("\"[Gmail]/All Mail\"")
	if status == 'NO':
		sys.exit(data)

	label = "10MB-25MB"
	_, data = imap.uid('search', None, "(larger {})".format(10 * 1024 * 1024))
	imap.create(label)
	for uid in data[0].split(' '):
		status, data = imap.uid('STORE', uid, '+X-GM-LABELS', label)
		print uid, status, data

	label = "5MB-10MB"
	_, data = imap.uid('search', None, "(larger {}) (smaller {})".format(5 * 1024 * 1024, 10 * 1024 * 1024))
	imap.create(label)
	for uid in data[0].split(' '):
		status, data = imap.uid('STORE', uid, '+X-GM-LABELS', label)
		print uid, status, data

	label = "2MB-5MB"
	_, data = imap.uid('search', None, "(larger {}) (smaller {})".format(2 * 1024 * 1024, 5 * 1024 * 1024))
	imap.create(label)
	for uid in data[0].split(' '):
		status, data = imap.uid('STORE', uid, '+X-GM-LABELS', label)
		print uid, status, data

	label = "1MB-2MB"
	_, data = imap.uid('search', None, "(larger {}) (smaller {})".format(1 * 1024 * 1024, 2 * 1024 * 1024))
	imap.create(label)
	for uid in data[0].split(' '):
		status, data = imap.uid('STORE', uid, '+X-GM-LABELS', label)
		print uid, status, data

	imap.close()
	imap.logout()
	imap.shutdown()


if __name__ == '__main__':
	sys.exit(main(sys.argv[1], sys.argv[2]))
