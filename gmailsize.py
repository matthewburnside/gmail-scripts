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
    ("10MB-25MB", 10),
    ("5MB-10MB", 5),
    ("2MB-5MB", 2),
    ("1MB-2MB", 1),
]

def gmail_login(username, password):
    try:
        ret = imaplib.IMAP4_SSL(default['host'], default['port'])
        ret.login(username, password)
    except:
        print "Failed to connect to gmail's IMAP Server: "
        raise
    return ret

def main(username, password):

    imap = gmail_login(username, password)
    imap.debug = IMAP_DEBUG_LEVEL
    status, data = imap.select("\"[Gmail]/All Mail\"")
    if status == 'NO':
        sys.exit(data)

    last = None
    for r in ranges:
        print "Working on range %s" % (r[0])
        label = r[0]
        if last == None:
            cmd = "(larger {})".format(r[1] * 1024 * 1024)
        else:
            cmd = "(larger {}) (smaller {})".format(r[1] * 1024 * 1024, 
                                                    last * 1024 * 1024)
        print cmd
        _, data = imap.uid('search', None, cmd)
        imap.create(label)
        if len(data[0]) == 0:
            print "No matching messages"
            continue
        for uid in data[0].split(' '):
            status, data = imap.uid('STORE', uid, '+X-GM-LABELS', label)
            print uid, status, data
        last = r[1]

    imap.close()
    imap.logout()
    imap.shutdown()

def usage():
    print "%s <gmail address>" % (__file__)
    print "Labels emails in your gmail account with their sizes in the following ranges:"
    for r in ranges:
        print r

if __name__ == '__main__':
    if(len(sys.argv) < 2):
        usage()
        exit()
    password = getpass.getpass("Gmail Password:")
    if(len(password) < 1):
        exit()
    sys.exit(main(sys.argv[1], password))
