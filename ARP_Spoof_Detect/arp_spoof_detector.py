#!/usr/bin/env python3

from scapy import all as scapy


def get_mac(ip):
    '''
        Performs ARP scan on target IP or IP range

        Parameters:
            ip - target IP or IP range

        Returns:
            MAC address of target ip
    '''
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered[0][1].hwsrc

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)

def process_sniffed_packet(packet):
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        try:
            real_mac = get_mac(packet[scapy.ARP].psrc)
            resp_mac = get_mac(packet[scapy.ARP].psrc)
        except ListIndex:
            if real_mac != resp_mac:
                print("[+] Detected ARP Spoof.")


def main():
    sniff("ens33")


if __name__ == "__main__":
    main()
