#ifndef _RETRIEVER_H
#define _RETRIEVER_H 0

char *request_wrapper(const char *url);
void request_deallocate(char *content);

#endif // _RETRIEVER_H
