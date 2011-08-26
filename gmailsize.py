#!/usr/bin/env python

import imaplib
import re
import rfc822
import StringIO
import email.header
import getpass
import os
import sys
from optparse import OptionParser

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

	#status, data = imap.search(None, "(larger {})".format(8 * 1024 * 1024))
	status, data = imap.uid('search', None, "(larger {})".format(8 * 1024 * 1024))

	imap.create("8MB")
	for uid in data[0].split(' '):
		status, data = imap.uid('STORE', uid, '+X-GM-LABELS', '8MB')
		print uid, status, data

if __name__ == '__main__':
	sys.exit(main(sys.argv[1], sys.argv[2]))
