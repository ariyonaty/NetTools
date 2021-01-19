#!/usr/bin/env python3

import socket
from scapy.all import sr, srp
from scapy.layers.l2 import ARP, Ether
from scapy.layers.inet import IP, TCP
from collections import namedtuple

Answer = namedtuple('Answer', 'ip mac')
TCPPort = namedtuple('TCPPort', 'port')

def tcp_scan(ip, port):
    try:
        syn = IP(dst=ip) / TCP(dport=port, flags='S')
    except socket.gaierror:
        raise Exception(f'Could not resolve {ip}')

    answer, _ = sr(syn, timeout=0.5, retry=1)

    results = []

    for _, packet in answer:
        if packet[TCP].flags == 'SA':
            results.append(TCPPort(packet[TCP].sport))

    return results

def arp_scan(ip):
    request = Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(pdst=ip)
    answer, _ = srp(request, timeout=0.5, retry=1)
    results = []

    for _, packet in answer:
        results.append(Answer(packet.psrc, packet.hwsrc))

    return results

def main():
    # answers = arp_scan('192.168.217.1/24')
    # if not answers:
    #     print("Router is down.")
    #     return
    # for answer in answers:
    #     print(f'Host {answer.ip} ({answer.mac}) is up.')

    ports_to_scan = [22,23,80,443,445]
    for port in ports_to_scan:
        results = tcp_scan('192.168.217.2', port)
        if results:
            for result in results:
                print(f'Port {result.port} is open.')
        else:
            print(f'Port {port} is closed.')


if __name__ == "__main__":
    main()