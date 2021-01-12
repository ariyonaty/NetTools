#!/usr/bin/python3

# use of underscore is to prevent namespace conflicts
import os as _os
import socket as _socket
import time as _time
import sys as _sys

from struct import Struct as _Struct
from ipaddress import IPv4Address as _IPv4Address

# assigning variables to direct function refs
_fast_time = _time.time
_write_err = _sys.stdout.write

tcp_header_unpack = _Struct('!2H2LB').unpack_from
udp_header_unpack = _Struct('!4H').unpack_from


class RawPacket(object):

    def __init__(self, data):
        self.timestamp = _fast_time()
        self.protocol = 0

        self._name = self.__class__.__name__

        self._datalen = len(data)

        # parsing ethernet header here for efficiency
        self.dst_mac = data[:6].hex()
        self.src_mac = data[6:12].hex()
        self._data = data[14:]


    # NOTE: this is very slow to have to print and should only be used for testing or learning. Generally you wouldnt need
    # to print a string representation of the class instance anyways.
    def __str__(self):
        return '\n'.join([
            f'{"="*32}',
            f'{" "*8}PACKET',
            f'{"="*32}',
            f'{" "*8}ETHERNET',
            f'{"-"*32}',
            f'src mac: {self.src_mac}',
            f'dst mac: {self.dst_mac}',
            f'{"-"*32}',
            f'{" "*8}IP',
            f'{"-"*32}',
            f'header length: {self.header_len}',
            f'protocol: {self.protocol}',
            f'src ip: {self.src_ip}',
            f'dst ip: {self.dst_ip}',
            f'{"-"*32}',
            f'{" "*8}PROTOCOL',
            f'{"-"*32}',
            f'src port: {self.src_port}',
            f'dst port: {self.dst_port}',
            f'{"-"*32}',
            f'{" "*8}PAYLOAD',
            f'{"-"*32}',
            f'{self.payload}'
        ])

    def parse(self):
        '''
            Index TCP/IP packet layers 3 & 4
            use as instance objects
        '''

        self._ip()
        if (self.protocol == 6):
            self._tcp()
        elif (self.protocol == 17):
            self._udp()
        else:
            _write_err('[-] Not a TCP/UDP packet!\n')
            _write_err(f'Protocol --> {self.protocol}\n')

    def _ip(self):

        data = self._data

        self.src_ip = _IPv4Address(data[12:16])
        self.dst_ip = _IPv4Address(data[16:20])

        self.header_len = (data[0] & 15) * 4
        self.protocol = data[9]
        self.ip_header = data[:self.header_len]

        # separate IP header from data
        self._data = data[self.header_len:]

    def _tcp(self):
        '''
            TCP header w/ max len of 32 bytes
            See RFC 793 
        '''

        data = self._data

        tcp_header = tcp_header_unpack(data)
        self.src_port = tcp_header[0]
        self.dst_port = tcp_header[1]
        self.seq_number = tcp_header[2]
        self.ack_number = tcp_header[3]

        header_len = (tcp_header[4] >> 4 & 15) * 4

        self.proto_header = data[:header_len]
        self.payload = data[header_len:]

    def _udp(self):
        '''
            UDP header 8 bytes
            See RFC 768
        '''

        data = self._data

        udp_header = udp_header_unpack(data)
        self.src_port = udp_header[0]
        self.dst_port = udp_header[1]
        self.udp_len = udp_header[2]
        self.udp_chk = udp_header[3]

        self.proto_header = data[:8]
        self.payload = data[8:]
