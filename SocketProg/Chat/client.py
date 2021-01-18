#!/usr/bin/env python3

import sys
import socket
import select
import protocol


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(protocol.SERVER_ADDRESS)

    to_read = [client, sys.stdin]

    finished = False
    while not finished:
        readables, _, _, = select.select(to_read, [], [], 0.1)

        for readable in readables:
            if readable == client:
                from_server = protocol.protocol_read_msg(client)
                print(f'From server: {from_server}')
            else:
                message = readable.readline().strip().encode()
                protocol.protocol_write_msg(client, message)
                if message == b'exit':
                    finished = True

    client.shutdown(socket.SHUT_RDWR)
    client.close()


if __name__ == "__main__":
    main()
