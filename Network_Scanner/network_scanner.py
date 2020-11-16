from scapy.all import srp
from scapy.layers.l2 import ARP, Ether

# iface = "wlx9cefd5fd63ca"


def scan(ip):
    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered = srp(arp_request_broadcast, timeout=1)[0]
    print(answered.summary())

    for resp in answered:
        print (resp)

scan("10.0.2.2/24")
