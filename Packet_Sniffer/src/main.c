#include <stdio.h>
#include "packet_sniffer.h"

int main(int argc, char const *argv[])
{
    ErrorCode error_code = ERROR_SUCCESS;

    if (argc != 2)
    {
        fprintf(stderr, "[-] Usage: %s [interface]\n", argv[0]);
        error_code = ERROR_BAD_ARGS;
        goto cleanup;
    }

    const char *interface_name = argv[1];

    error_code = sniff_packets(interface_name);

cleanup:
    return error_code;
}
