#!/usr/bin/env python

import netfilterqueue
from scapy.all import IP

def process_packet(packet):
    scapy_packet = IP(packet.get_payload)
    # print(packet.get_payload())
    print(scapy_packet.show())
    packet.accept()


if __name__ == "__main__":
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()

