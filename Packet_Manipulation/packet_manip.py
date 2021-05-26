#!/usr/bin/env python3

import socket

from ipaddress import IPv4Address
from enum import IntEnum


class PROTO(IntEnum):
    TCP = 6
    UDP = 17


class PacketManipulation:
    '''
        class to manipulate tcp/ip packets

        currently limited to UDP only

            packet = PacketManipulation(('127.0.0.1', 4444))

            packet.create_socket()
            packet.sent_to(b'what's cracking')
    '''
    __slots__ = (
        'target', 'data', 'protocol', 'socket',

        'connect'
    )

    def __init__(self, target, *, protocol=PROTO.UDP):
        self.target = target

        self._validate_target()

        self.socket = socket.socket()
        self.connect = False
        self.protocol = PROTO.UDP

    def create_socket(self, *, connect=False):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        if connect:
            self.socket.connect(self.target)
            self.connect = True

    def send(self, data):
        '''
            Calls send_to() on socket, then sends data to specified target and prints 
            number of bytes sent. Requires connect argument to be used at socket creation

                packet.send(b'message here')
        '''

        if not self.connect:
            raise RuntimeError(
                "Cannot call send method without connect argument in socket creation.")

        if not isinstance(data, bytes):
            raise TypeError("data must be a bytestring.")

        send_count = self.socket.send(data)

        print(f'sent {send_count} bytes!')

    def send_to(self, data, *, target=None):
        '''
            Calls send_to() on socket, then sends data to specified target and prints 
            number of bytes sent. Requires connect argument to be used at socket creation

                packet.send_to(b'message here')
        '''
        if not isinstance(data, bytes):
            raise TypeError("data must be a bytestring.")

        if not target:
            target = self.target
            self._validate_target(target)

        send_count = self.socket.sendto(data, target)
        
        print(f'sent {send_count} bytes!')

    def _validate_target(self, target=None):
        if target is None:
            target = self.target

        if not isinstance(target, tuple) or len(target) != 2:
            raise TypeError("target must a two-tuple containg host IP/port.")

        try:
            IPv4Address(target[0])
        except:
            raise ValueError("invalid IP address provided for target.")

        if not isinstance(target[1], int):
            raise TypeError('target port must be an integer.')

        if not target[1] in range(0, 65536):
            raise ValueError('target port must be between 0-65536')

if __name__ == "__main__":
    packet = PacketManipulation(('127.0.0.1', 4444))
    packet.create_socket()
    packet.send_to(b'Why so serious?!')



