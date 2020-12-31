/**
 * Libcurl example
 * 
 * Compile:
 *  $ gcc downloadex.c -l curl
 */

#include <curl/curl.h>
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    CURL *curl = curl_easy_init();

    if (!curl)
    {
        fprintf(stderr, "init failed!\n");
        return EXIT_FAILURE;
    }

    // Set options
    curl_easy_setopt(curl, CURLOPT_URL, "https://google.com");

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