#!/usr/bin/env python

IMAP_DEBUG_LEVEL=0

import imaplib
import sys
import getpass
import re

default = {
    'host': 'imap.gmail.com',
    'port': '993',
}

rfc822_re = re.compile("(\d+) \(UID (\d+) RFC822.SIZE (\d+).*\)")

def sizeof_fmt(num):
    for x in ['bytes','KB','MB','GB','TB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0

def gmail_login(username):
    try:
        ret = imaplib.IMAP4_SSL(default['host'], default['port'])
        password = getpass.getpass("Password: ")
        if (len(password) < 1):
            exit()
        ret.login(username, password)
    except:
        print "Failed to connect to Gmail's IMAP Server: "
        raise
    return ret


def main(username, search):
    imap = gmail_login(username)
    imap.debug = IMAP_DEBUG_LEVEL
    status, data = imap.select("\"[Gmail]/All Mail\"")
    if status == 'NO':
        sys.exit(data)

    status, data = imap.uid('search', None, "(X-GM-RAW \"{}\")".format(search))
    msg_set = data[0].replace(' ', ',')
    status, sizes = imap.uid('fetch', msg_set, "(RFC822.SIZE)")

    search_siz = 0
    for rfc in sizes:
        match = rfc822_re.match(rfc)
        search_siz += int(match.group(3))

    print search.ljust(25), str(sizeof_fmt(search_siz)).rjust(15)

    imap.close()
    imap.logout()
    imap.shutdown()


def usage():
    print "%s <gmail address> <gmail search>" % (__file__)
    print "Labels emails in your Gmail according to their size."
    exit()


if __name__ == '__main__':
    if (len(sys.argv) < 3):
        usage()
    sys.exit(main(sys.argv[1], sys.argv[2]))
