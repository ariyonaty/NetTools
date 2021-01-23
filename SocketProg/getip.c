/**
 * getip.c - hostname lookup
 */

#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <netdb.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

int main(int argc, char const *argv[])
{
    struct hostent *h;

    if (argc != 2)
    {
        fprintf(stderr, "Usage: %s <HOST>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    return 0;
}
