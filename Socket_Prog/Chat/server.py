#!/usr/bin/env python3

import socket
import select
import protocol


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(protocol.SERVER_ADDRESS)
    server.listen(5)

    clients = [server]

    while True:
        readables, _, _, = select.select(clients, [], [], 0.1)
        for readable in readables:
            if readable == server:
                conn, addr = server.accept()
                print(f'New client: {addr}')
                clients.append(conn)
            else:
                message = protocol.protocol_read_msg(readable)
                if not message or message == b'exit':
                    # client disconnect
                    readable.shutdown(socket.SHUT_RDWR)
                    readable.close()
                    clients.remove(readable)
                for client in clients:
                    if client != readable and client != server:
                        protocol.protocol_write_msg(client, message)

    server.shutdown(socket.SHUT_RDWR)
    server.close()


if __name__ == "__main__":
    main()
