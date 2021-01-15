#!/usr/bin/env python3

import socket
import subprocess

SOURCE_ADDR = ('127.0.0.1', 1234)


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(SOURCE_ADDR)

    while True:
        message, addr = s.recvfrom(1024)
        print(f"Recv: {message} from {addr}")
        if (message == b'exit'):
            break
        output = subprocess.run(message, shell=True, capture_output=True).stdout
        s.sendto(output, addr)

    s.close()


if __name__ == "__main__":
    main()
