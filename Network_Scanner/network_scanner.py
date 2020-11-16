import optparse
from scapy.all import srp
from scapy.layers.l2 import ARP, Ether

# iface = "wlx9cefd5fd63ca"


def menu():
    print("------------------------------------------")
    print("|            NETWORK SCANNER             |")
    print("------------------------------------------")

def get_args():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="target IP(s)")
    options = parser.parse_args()[0]
    target = options.target
    
    if not options.target:
        print("[-] No target IP(s) specified.\n    Enter target IP below.\n    Use --help for more info.")
        target = input("target > ")

    print("------------------------------------------")
    return target

def scan(ip):
    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered = srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    client_list = []

    for resp in answered:
        client_dict = {"ip": resp[1].psrc, "mac": resp[1].hwsrc}
        client_list.append(client_dict)

    return client_list

def display(client_list):
    print("IP\t\t\tMAC ADDR")
    print("------------------------------------------")
    for client in client_list:
        print(f'{client["ip"]}\t\t{client["mac"]}')

if __name__ == "__main__":
    menu()
    target = get_args()
    results = scan(target)
    display(results)

