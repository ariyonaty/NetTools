#!/usr/bin/python3

import subprocess
import re
import optparse
import time

# interface = "wlx9cefd5fd63ca"
# new_mac = "00:11:22:33:44:77"

def menu():
    '''
        Generic console output header for mac changer
    '''
    print("------------------------------------------")
    print("|          MAC ADDRESS CHANGER           |")
    print("------------------------------------------")

def get_args():
    """
        Collects data needed to change MAC address.

        Returns:
            Interface and new MAC address
    """
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="interface to target")
    parser.add_option("-m", "--mac", dest="mac", help="initialize new MAC address")

    options = parser.parse_args()[0]
    interface, new_mac = options.interface, options.mac

    if not options.interface:
        print("[-] No interface. Enter interface below.\nUse --help for more info.")
        interface = input("interface > ")
    if not options.mac:
        print("[-] No MAC address. Enter MAC below.\nUse --help for more info.")
        new_mac = input("new MAC > ")
        
    return (interface, new_mac)


def change_mac(interface, new_mac):
    """
        Changes the interface MAC address to new_mac

        Params:
            interface: network interface to update MAC addr
            new_mac: new MAC address 
    """
    print(f"[+] Changing MAC address for {interface} to {new_mac}")

    try:
        subprocess.call(["ip", "link", "set", interface, "down"])
        subprocess.call(["ip", "link", "set", interface, "address", new_mac])
        subprocess.call(["ip", "link", "set", interface, "up"])
    except Exception as e:
        print(e)
        return -1

def get_ether(interface):
    """
        Get the MAC address.

        Returns:
            HW Ether address
    """
    try:
        ip_result = subprocess.check_output(["ip", "link", "show", interface])
        ip_result = str(ip_result, 'utf-8')
        ether_search = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ip_result)
        return ether_search[0]
    except Exception as e:
        print(e)
        return -2

if __name__ == "__main__":
    menu()
    iface, new_mac = get_args()
    mac_orig = get_ether(iface)
    change_mac(iface, new_mac)
    curr_mac = get_ether(iface)

    if curr_mac == new_mac:
        print(f"[+] MAC address changed from {mac_orig} to {curr_mac}")
    else:
        print("[-] MAC address did not change")

    
