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

list_re   = re.compile(r'\((?P<flags>.*?)\) "(?P<delim>.*)" (?P<mbox>.*)')
rfc822_re = re.compile("(\d+) \(RFC822.SIZE (\d+).*\)")

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


def main(username):
    imap = gmail_login(username)
    imap.debug = IMAP_DEBUG_LEVEL

    status, data = imap.list("", "*")

    for box in data:
        flags, delim, label = list_re.match(box).groups()
        label = label.strip('\"')

        status, data = imap.select(label)
        if status == 'NO':
            continue
        label_len = int(data[0])

        status, msg = imap.search(None, 'ALL')
        m = [int(x) for x in msg[0].split()]

        m.sort()
        if not m:
            continue

        msg_set = "%d:%d" % (m[0], m[-1])
        status, sizes = imap.fetch(msg_set, "(RFC822.SIZE)")

        label_siz = 0
        for rfc in sizes:
            match = rfc822_re.match(rfc)
            label_siz += int(match.group(2))

        print label.ljust(25), str(sizeof_fmt(label_siz)).rjust(15)
        imap.close()

    imap.logout()
    imap.shutdown()


def usage():
    print "%s <gmail address>" % (__file__)
    print "Labels emails in your Gmail according to their size."


if __name__ == '__main__':
    if (len(sys.argv) < 2):
        usage()
        exit()
    sys.exit(main(sys.argv[1]))
