#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <string.h>
#include <net/ethernet.h>
#include <netinet/ip.h>
#include <netinet/if_ether.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <arpa/inet.h>

#define PACKET_BUFFER_SIZE 65536

int main(int argc, char const *argv[])
{
    ssize_t data_size;
    uint8_t packet_buffer[PACKET_BUFFER_SIZE];

    if (argc != 2)
    {
        fprintf(stderr, "[-] Usage: %s [interface]\n", argv[0]);
        return EXIT_FAILURE;
    }

    const char *interface_name = argv[1];

    int raw_sock = socket(AF_PACKET, SOCK_RAW, htons(ETH_P_ALL));
    if (raw_sock == -1)
    {
        perror("socket");
        return EXIT_FAILURE;
    }

    if (setsockopt(raw_sock, SOL_SOCKET, SO_BINDTODEVICE, interface_name, strlen(interface_name)) == -1)
    {
        perror("setsockopt");
        return EXIT_FAILURE;
    }

    for (;;)
    {
        data_size = recvfrom(raw_sock, packet_buffer, PACKET_BUFFER_SIZE, 0, NULL, NULL);
        if (data_size == -1)
        {
            perror("recvfrom");
            close(raw_sock);
            return EXIT_FAILURE;
        }
        // packet recvd at this point
        printf("Recieved: %lu bytes\n", data_size);
    }

    return EXIT_SUCCESS;
}

