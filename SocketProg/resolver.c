#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <netdb.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>

#define BUF_SIZE 1024

const char *hostname_to_ip(const char *hostname);

int main(int argc, char const *argv[])
{
    struct addrinfo hints;
    struct addrinfo *res, *p;

    int status;
    char ipstr[INET6_ADDRSTRLEN];

    if (argc != 2)
    {
        fprintf(stderr, "Usage: %s <HOST>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    if ((status = getaddrinfo(argv[1], NULL, &hints, &res)) != 0)
    {
        fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(status));
        exit(EXIT_FAILURE);
    }

    printf("IP addresses for %s:\n\n", argv[1]);

    for (p = res; p != NULL; p = p->ai_next)
    { 
        void *addr;
        char *ipver;

        if (p->ai_family == AF_INET)
        {
            struct sockaddr_in *ipv4 = (struct sockaddr_in *)p->ai_addr;
            addr = &(ipv4->sin_addr);
            ipver = "IPv4";
        }
        else
        {
            struct sockaddr_in6 *ipv6 = (struct sockaddr_in6 *)p->ai_addr;
            addr = &(ipv6->sin6_addr);
            ipver = "IPv6";
        }

        inet_ntop(p->ai_family, addr, ipstr, sizeof(ipstr));
        printf("  %s: %s\n", ipver, ipstr);
    }

    freeaddrinfo(res);

    return 0;
}

const char *hostname_to_ip(const char *hostname)
{
    int sockfd;
    struct addrinfo hints;
    struct addrinfo *servinfo, *p;
    struct sockaddr_in *host;
    int rv;

    char *ip;

    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_INET;
    hints.ai_socktype = SOCK_STREAM;

    printf("Here\n");

    if ((rv = getaddrinfo(hostname, "http", &hints, &servinfo)) != 0)
    {
        fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(rv));
        exit(EXIT_FAILURE);
    }

    printf("Here\n");

    for (p = servinfo; p != NULL; p = p->ai_next)
    {
        host = (struct sockaddr_in *)p->ai_addr;
    }

    printf("Here\n");

    freeaddrinfo(servinfo);
    printf("%s\n", ip);
    return ip;
}