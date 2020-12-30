#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <netdb.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>

void dump(const unsigned char *data_buffer, const unsigned int length);

int main(int argc, char const *argv[])
{
    if (argc < 2)
    {
        printf("Usage.\n");
        return EXIT_FAILURE;
    }

    struct sockaddr_in host_addr, client_addr;
    int sockfd;
    socklen_t sin_size;

    const unsigned char *buf = "alphabeta";

    if ((sockfd = socket(AF_INET, SOCK_RAW, IPPROTO_TCP)) == -1)
    {
        printf("Error with socket.\n");
    }

    memset(&client_addr, sizeof(remote), 0);
    client_addr.sin_addr = AF_INET;
    client_addr.sin_port = inet_aton(argv[2]);
    inet_aton()

    return EXIT_SUCCESS;
}

void dump(const unsigned char *data_buffer, const unsigned int length)
{
    unsigned char byte;
    unsigned int i, j;

    for (i = 0; i < length; i++)
    {
        byte = data_buffer[i];
        printf("%02x ", data_buffer[i]);
        if (((i % 16) == 15) || (i == length - 1))
        {
            for (j = 0; j < 15 - (i % 16); j++)
            {
                printf("  ");
            }
            printf("| ");
            for (j = (i - (i % 16)); j <= i; j++)
            {
                byte = data_buffer[j];
                if ((byte > 31) && (byte <127))
                {
                    printf("%c", byte);
                }
                else
                {
                    printf(".");
                }
            }
            printf("\n");
        }
    }
}