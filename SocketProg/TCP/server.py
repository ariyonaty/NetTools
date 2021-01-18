#!/usr/bin/env python3

import socket
import subprocess

HOST = '127.0.0.1'
PORT = 4567


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(3)
        conn, addr = s.accept()
        with conn:
            print(f"Got connection from: {addr}")
            while True:
                data = conn.recv(1024)
                print(f"Recieved: {data}")
                if not data or data == b'exit':
                    break
                output = subprocess.run(
                    data, shell=True, capture_output=True).stdout
                conn.sendall(output)


if __name__ == "__main__":
    main()
