#!/usr/bin/env python3

import socket
import subprocess

SERVER_ADDR = ('127.0.0.1', 1234)


def main():
    s = socket.socket()

    s.bind(SERVER_ADDR)
    s.listen(5)

    while True:

        conn, addr = s.accept()
        print(f"Got connection from: {addr}")

        data = conn.recv(1024)
        print(f"Recieved: {data}")

        output = subprocess.run(data, shell=True, capture_output=True).stdout

        conn.sendall(output)

        conn.shutdown(socket.SHUT_RDWR)
        conn.close()

        if data == b'exit' or not data:
            break

    s.shutdown(socket.SHUT_RDWR)
    s.close()


if __name__ == "__main__":
    main()
