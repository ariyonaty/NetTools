/**
 * Libcurl example
 * 
 * Compile:
 *  $ gcc downloadex.c -l curl
 */

#include <curl/curl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

size_t got_data(char *buffer, size_t itemsize, size_t niterms, void *ign);

int main(int argc, char const *argv[])
{
    CURL *curl = curl_easy_init();


    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./downloadex <URL>\n");
        return EXIT_FAILURE;
    }

    const char *url = argv[1];

    if (!curl)
    {
        fprintf(stderr, "init failed!\n");
        return EXIT_FAILURE;
    }

    // Set options
    curl_easy_setopt(curl, CURLOPT_URL, url);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, got_data);

    // Perform action
    CURLcode result = curl_easy_perform(curl);
    if (result != CURLE_OK)
    {
        fprintf(stderr, "download problem :  %s\n", curl_easy_strerror(result));
        return EXIT_FAILURE;
    }

    curl_easy_cleanup(curl);
    return EXIT_SUCCESS;
}

size_t got_data(char *buffer, size_t itemsize, size_t niterms, void *ign)
{
    size_t bytes = itemsize * niterms;
    int linenumber = 1;

    printf("New chuck size: (%zu bytes)\n", bytes);
    printf("%d:\t", linenumber);
    for (int i = 0; i < bytes; i++)
    {
        printf("%c", buffer[i]);

        if (buffer[i] == '\n')
        {
            linenumber++;
            printf("%d:\t", linenumber);
        }
    }

    printf("\n\n");
    return bytes;
}