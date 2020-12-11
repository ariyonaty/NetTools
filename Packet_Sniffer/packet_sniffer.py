import scapy.all as scapy
from scapy.layers import http

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)

def process_sniffed_packet(packet:scapy.packet):
    if (packet.haslayer(http.HTTPRequest)):
        print(packet)

if __name__ == "__main__":
    sniff('eth0')