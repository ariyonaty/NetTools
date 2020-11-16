import optparse
from scapy.all import srp
from scapy.layers.l2 import ARP, Ether

def menu():
    '''
        Generic console output header for network scanner
    '''
    print("------------------------------------------")
    print("|            NETWORK SCANNER             |")
    print("------------------------------------------")

def get_args():
    '''
        Gets arguments for program execution

        Returns:
            target IP or IP range
    '''
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
    '''
        Performs ARP scan on target IP or IP range

        Parameters:
            ip - target IP or IP range

        Returns:
            client_list - list of dict containing mapping between IP and MAC
    '''
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
    '''
        Display results in formatted table
    '''
    print("IP\t\t\tMAC ADDR")
    print("------------------------------------------")
    for client in client_list:
        print(f'{client["ip"]}\t\t{client["mac"]}')

if __name__ == "__main__":
    menu()
    target = get_args()
    results = scan(target)
    display(results)

