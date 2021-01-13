#ifndef __PACKET_SNIFFER_H__
#define __PACKET_SNIFFER_H__

#include <stdint.h>


#define MAX_IP_LEN 16
#define PACKET_BUFFER_SIZE 65536

typedef enum
{
    ERROR_SUCCESS = 0,
    ERROR_BAD_ARGS,
    ERROR_API,
    ERROR_NULL_ARGS
} ErrorCode;

ErrorCode handle_pkt(const uint8_t *pkt_buffer, ssize_t pkt_length);
ErrorCode sniff_packets(const char *interface_name);

#endif