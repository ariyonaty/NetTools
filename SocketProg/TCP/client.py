#!/usr/bin/env python3

import socket

SERVER_ADDR = ('127.0.0.1', 1234)


def main():
    s = socket.socket()

    s.connect(SERVER_ADDR)

    while True:
        send = input("> ")
        print(send)
        s.sendall(send.encode())
        data = s.recv(1024)
        print(f"{data.decode()}")

    s.shutdown(socket.SHUT_RDWR)
    s.close()


if __name__ == "__main__":
    main()
