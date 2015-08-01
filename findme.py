#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  hzsunshx
# Created: 2015-08-01 15:09

"""
findme (This is client)

Third lib:
    https://pypi.python.org/pypi/urlfetch
"""

import os
import sys
import subprocess
import urllib, urllib2
import fcntl, socket, struct

def shell(cmd):
    try:
        output = subprocess.check_output(cmd)
        return output
    except Exception as e:
        return str(e)


def getHwAddr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
    return ':'.join(['%02x' % ord(char) for char in info[18:24]])


def findme(server_addr):
    data = urllib.urlencode({
        'ifconfig': shell('ifconfig'),
        'mac': getHwAddr('eth0'),
    })
    req = urllib2.Request(server_addr, data)
    response = urllib2.urlopen(req, timeout=5)
    print response.read()


def test():
    print getHwAddr('eth0')

if __name__ == '__main__':
    SERVER=os.getenv('SERVER')
    if not SERVER:
        sys.exit("Need env-var: SERVER")
    findme(SERVER)
