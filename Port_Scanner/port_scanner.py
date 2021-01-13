""" 
    PORT SCANNER
"""

import socket
import threading

results = {}

def worker(ip, port):
    s = socket.socket(socket.AF_INET, )
    s.settimeout(0.5)
    if s.connect_ex((ip, port)) == 0:
        if port == 80:
            s.send(b'GET / HTTP/1.0\r\n\r\n')
        results[port] = s.recv(1024).decode()


def scan(ip):
    for port in range(1000):
        t = threading.Thread(target=worker, args=(ip, port))
        t.start()


if __name__ == "__main__":
    ip = input('Enter target IP > ')
    scan(ip)
    for port, data in results.items():
        print(f'Port {port}\t\t{data}')
        
