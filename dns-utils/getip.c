#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <string.h>

int main(int argc, char *argv[]) {

    // Usage check
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <hostname>\n", argv[0]);
        return EXIT_FAILURE;
    }

    const char* hostname = argv[1];

    struct addrinfo hint;
    struct addrinfo* result;

    memset(&hint, 0, sizeof(hint));
    hint.ai_family = AF_UNSPEC;
    hint.ai_socktype = SOCK_STREAM;

    int status = getaddrinfo(hostname, NULL, &hint, &result);
    if (status != 0) {
        fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(status));
        return EXIT_FAILURE;
    }

    // Traverse linked list
    struct addrinfo* ptr;
    char ipstr[INET6_ADDRSTRLEN];
    printf("IP addresses for %s:\n", hostname);
    for (ptr = result; ptr != NULL; ptr=ptr->ai_next) {
        void *addr;
        char *ipver;

        if (ptr->ai_family == AF_INET) {
            struct sockaddr_in* ipv4 = (struct sockaddr_in *)ptr->ai_addr;
            addr = &(ipv4->sin_addr);
            ipver = "IPv4";
        }
        else {
            struct sockaddr_in6* ipv6 = (struct sockaddr_in6 *)ptr->ai_addr;
            addr = &(ipv6->sin6_addr);
            ipver = "IPv6";
        }
        inet_ntop(ptr->ai_family, addr, ipstr, sizeof(ipstr));
        printf("  %s: %s\n", ipver, ipstr);
    }


    freeaddrinfo(result);

    return EXIT_SUCCESS;
}
