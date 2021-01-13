#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <net/ethernet.h>
#include <netinet/ip.h>
#include <netinet/if_ether.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <arpa/inet.h>
#include "packet_sniffer.h"

ErrorCode handle_pkt(const uint8_t *pkt_buffer, ssize_t pkt_length)
{
    ErrorCode error_code = ERROR_SUCCESS;
    if (!pkt_buffer)
    {
        error_code = ERROR_NULL_ARGS;
        return error_code;
    }
    printf("Recieved: %lu bytes\n", pkt_length);
    printf("\tFirst byte: %x\n", pkt_buffer[0]);

    return ERROR_SUCCESS;
}

ErrorCode sniff_packets(const char *interface_name)
{
    ErrorCode error_code = ERROR_SUCCESS;

    ssize_t data_size;
    uint8_t packet_buffer[PACKET_BUFFER_SIZE] = {0};

    int raw_sock = socket(AF_PACKET, SOCK_RAW, htons(ETH_P_ALL));
    if (raw_sock == -1)
    {
        perror("socket");
        error_code = ERROR_API;
        goto cleanup;
    }

    if (setsockopt(raw_sock, SOL_SOCKET, SO_BINDTODEVICE, interface_name, strlen(interface_name)) == -1)
    {
        perror("setsockopt");
        error_code = ERROR_API;
        goto cleanup;
    }

    for (;;)
    {
        data_size = recvfrom(raw_sock, packet_buffer, PACKET_BUFFER_SIZE, 0, NULL, NULL);
        if (data_size == -1)
        {
            perror("recvfrom");
            error_code = ERROR_API;
            goto cleanup;
        }
        error_code = handle_pkt(packet_buffer, data_size);
        if (error_code != ERROR_SUCCESS)
        {
            printf("handle_packet failed with: %d\n", error_code);
            goto cleanup;
        }
    }

cleanup:
    if (raw_sock != -1 && close(raw_sock) == -1)
    {
        perror("close");
    }
    
    return error_code;
}