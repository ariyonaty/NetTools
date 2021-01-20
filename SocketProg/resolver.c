#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <netdb.h>
#include <errno.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/types.h>
#include <sys/socket.h>

#define BUF_SIZE 1024

const char *hostname_to_ip(const char *hostname);

int main(int argc, char const *argv[])
{
    struct addrinfo hints;
    struct addrinfo *results, *rp;

    int sfd, s;
    size_t len;
    ssize_t nread;
    char buf[BUF_SIZE];

    if (argc != 2)
    {
        fprintf(stderr, "Usage: %s <HOST>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    const char *hostname = argv[1];
    const char *ip = hostname_to_ip(argv[1]);

    printf("%s resolved to %s\n", hostname, ip);

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
        strcpy(ip, inet_ntoa(host->sin_addr));
    }

    printf("Here\n");

    freeaddrinfo(servinfo);
    printf("%s\n", ip);
    return ip;
}