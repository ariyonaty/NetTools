#!/usr/bin/python3

import os
import sys
import socket
from raw_packet import RawPacket


def parse(data):
    try:
        packet = RawPacket(data)
        packet.parse()
        print(packet)
    except:
        pass


def listen_forever(iface):

    sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
    try:
        sock.bind((iface, 3))
    except OSError:
        sys.exit(f'[-] Cannot bind interface: {iface}! Quitting...')

    while True:
        try:
            data = sock.recv(2048)
        except OSError:
            pass
        else:
            parse(data)


if __name__ == "__main__":
    if os.geteuid():
        sys.exit("[-] Listener must be ran as root! Quitting...")

    listen_forever('eth0')
