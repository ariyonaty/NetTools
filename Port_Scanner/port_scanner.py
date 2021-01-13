""" 
    PORT SCANNER
"""

import socket
import threading

def worker(ip, port):
    pass

def scan(ip):
    for port in range(1000):
        t = threading.Thread(target=worker, args=(ip, port))
        t.start()

if __name__ == "__main__":
    ip = input('Enter target IP > ')
