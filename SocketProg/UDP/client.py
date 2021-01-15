#!/usr/bin/env python3

import socket

SOURCE_ADDR = ('127.0.0.1', 4321)
SERVER_ADDR = ('127.0.0.1', 1234)


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(SOURCE_ADDR)

    cmd = input('> ')
    while cmd != 'exit':
        s.sendto(cmd.encode(), SERVER_ADDR)
        message, addr = s.recvfrom(1024)
        print(f"{message.decode()}")
        cmd = input('> ')
    else:
        s.sendto(cmd.encode(), SERVER_ADDR)
        
    s.close()


if __name__ == "__main__":
    main()
