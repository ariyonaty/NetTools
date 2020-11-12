from scapy.all import srp
from scapy.layers.l2 import ARP, Ether

iface = "wlx9cefd5fd63ca"

def scan(ip):
    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered, unanswered = srp(arp_request_broadcast, iface=iface)
    print(answered.summary())

scan("192.168.88.1")
