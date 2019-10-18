#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <errno.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <sys/stat.h>
//#include </in.h>
#include <arpa/inet.h>
#include <fcntl.h>

/*-----------------------Macros----------------------------------*/

#define PORT 8000
#define MAX_BUF_SIZE 4096
#define MAX_CONNECT 20
#define ADMIN_PSD "981122"
#define USER_PSD "123456"
#define PSD_LEN 6

/*---------------------Functions--------------------------------*/
int recv_headr(int sockfd, void *buf,int *auth);