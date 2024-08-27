#include <stdio.h>
#include <stdlib.h>
#include "request.h"

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s URL\n", argv[0]);
        exit(EXIT_FAILURE);
    }
    const char *url = argv[1];
    char *content = request_wrapper(url);
    if (!content) {
        fprintf(stderr, "Fail request\n");
        exit(EXIT_FAILURE);
    }
    printf("%s\n", content);
    request_deallocate(content);
    return 0;
}
