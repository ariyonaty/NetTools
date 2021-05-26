import socket
import struct

MESSAGE_FORMAT = struct.Struct('!I')
SERVER_ADDRESS = ('127.0.0.1', 1337)

def protocol_write_msg(sock, msg):
    msg_len = len(msg)
    msg = MESSAGE_FORMAT.pack(msg_len) + msg
    sock.sendall(msg)

def protocol_read_msg(sock):
    metadata = sock.recv(MESSAGE_FORMAT.size)
    if not metadata:
        return b''
    msg_len = MESSAGE_FORMAT.unpack(metadata)[0]
    return sock.recv(msg_len)