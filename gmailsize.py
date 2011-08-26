#!/usr/bin/env python

IMAP_DEBUG_LEVEL=0

import imaplib
import sys
import getpass

default = {
    'host': 'imap.gmail.com',
    'port': '993',
}

ranges = [
    { 'label': "10MB-25MB", 'start': 10, 'end': 99 },
    { 'label': "5MB-10MB",  'start': 5,  'end': 10 },
    { 'label': "2MB-5MB",   'start': 2,  'end': 5  },
    { 'label': "1MB-2MB",   'start': 1,  'end': 2  },
]

def gmail_login(username, password):
    try:
        ret = imaplib.IMAP4_SSL(default['host'], default['port'])
        ret.login(username, password)
    except:
        print "Failed to connect to Gmail's IMAP Server: "
        raise
    return ret


def main(username, password):
    imap = gmail_login(username, password)
    imap.debug = IMAP_DEBUG_LEVEL
    status, data = imap.select("\"[Gmail]/All Mail\"")
    if status == 'NO':
        sys.exit(data)

    for r in ranges:
        print "Range {}:".format(r['label']), 
        imap.create(r['label'])
        cmd = "(larger {}) (smaller {})".format(r['start'] * 1024 * 1024, 
						r['end'] * 1024 * 1024)
        _, data = imap.uid('search', None, cmd)
        if len(data[0]) == 0:
            print "No matching messages"
            continue

        uids = data[0].replace(' ', ',')
        status, data = imap.uid('STORE', uids, '+X-GM-LABELS', r['label'])
        print status

    imap.close()
    imap.logout()
    imap.shutdown()


def usage():
    print "%s <gmail address>" % (__file__)
    print "Labels emails in your Gmail account with the following:"
    for r in ranges:
        print r


if __name__ == '__main__':
    if (len(sys.argv) < 2):
        usage()
        exit()
    password = getpass.getpass("Password: ")
    if (len(password) < 1):
        exit()
    sys.exit(main(sys.argv[1], password))
