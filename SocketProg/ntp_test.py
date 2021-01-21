#!/usr/bin/env python3

import socket
import sys
import struct
import time
from contextlib import closing

def getNTPTime():
    host = 'us.pool.ntp.org'
    port = 123
    buf = 1024
    msgstr = '\x1b' + 47 * '\0'
    msg = msgstr.encode()

    # reference time (in seconds since 1900-01-01 00:00:00)
    TIME1970 = 2208988800 # 1970-01-01 00:00:00

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.sendto(msg, (host, port))
    msg, addr = client.recvfrom(buf)

    t = struct.unpack("!12I", msg)
    print (t)
    print (t[10])
    t = t[10] - TIME1970

    return time.ctime(t)

if __name__ == "__main__":
    print(getNTPTime())