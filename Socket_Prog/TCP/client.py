#!/usr/bin/env python3

import socket
import subprocess


HOST = '127.0.0.1'
PORT = 4567

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            send = input("> ")
            if not send:
                continue
            if send == 'exit':
                s.sendall(b'exit')
                break
            s.sendall(send.encode())
            data = s.recv(1024)
            if not data:
                continue
            print(data.decode())

if __name__ == "__main__":
    main()