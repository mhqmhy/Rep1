#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <signal.h>
#include <pthread.h>
#include <errno.h>
#include <libgen.h>
#include <fcntl.h>
#include <vector>
#include <iostream>
#include <string>
using namespace std;
#define N 256
 
typedef struct sockaddr AS;
/*
 1.请求报文
	1.1 报头
		1B: 操作码 {0:请求文件列表,1:上传文件,2:下载文件,3:删除文件,4:重命名文件};
		
	1.2 报文
 2.返回状态及数据内容
*/
vector<string> splitString(char str[])
{
	const char s[2] = "&";
  	char *token,*list[100];
  	vector<string> myList;
   	int i = 0;   
	/* 获取第一个子字符串 */
	token = strtok(str, s);  
	/* 继续获取其他的子字符串 */
	while( token != NULL ) {
	    printf( "token: %s\t", token );   
	    myList.push_back(token);
	    cout<<myList[i]<<endl;
	    i++;
	    token = strtok(NULL, s);
	}
	return myList;
}

struct sockaddr_in taojiekou()
{
    int sockfd;
    if((sockfd = socket(AF_INET,SOCK_STREAM,0)) < 0){
        printf("fail to socket ");
        
        }
    /*服务端信息*/
    struct sockaddr_in server_addr;
    memset(&server_addr,0,sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(9500);
    server_addr.sin_addr.s_addr = inet_addr("127.0.0.1");
    return server_addr;
}

int ProcessList(vector<string> &myList,string userName, string loginPassword)
{
    struct sockaddr_in server_addr = taojiekou();
    int sockfd,nbyte,fd;
    char *buf;
    //ip
    if((sockfd = socket(AF_INET,SOCK_STREAM, 0)) < 0){
        printf("fail\n");
        return -1;
    }
/*连接服务端*/
    if(connect(sockfd,(AS *)&server_addr,sizeof(server_addr)) < 0){
        printf("fail to connect server\n");
        return -1;
    }
    
    string baowen = "0"+userName+loginPassword;//0用户名密码文件名
/*向服务端发送Get命令来获取文件，服务端返回文件是否存在*/
    buf = (char *)baowen.c_str();
    send(sockfd, buf, N, 0);
    recv(sockfd, buf, N, 0);
   
    // close(fd);
    // close(sockfd);
    myList = splitString(buf);
    return 0; //successful

   
    
}

int ProcessDelete(string command,string userName, string loginPassword)
{
    struct sockaddr_in server_addr = taojiekou();
    int sockfd,nbyte,fd;
    char *buf;
   
    if((sockfd = socket(AF_INET,SOCK_STREAM, 0)) < 0){
        printf("fail\n");
        return -1;
    }
/*连接服务端*/
    if(connect(sockfd,(AS *)&server_addr,sizeof(server_addr)) < 0){
        printf("fail to connect server\n");
        return -1;
    }
    
    string baowen = "3"+userName+loginPassword+command;//3用户名登录密码文件名
/*向服务端发送Get命令来获取文件，服务端返回文件是否存在*/
    buf = (char *)baowen.c_str();
    send(sockfd, buf, N, 0);

    printf("Delete file successfully!\n");
    close(fd);
    close(sockfd);
    return 0;
}

int ProcessRename(string command,string userName,string loginPassword)
{
    struct sockaddr_in server_addr = taojiekou();
    int sockfd,nbyte,fd;
    char *buf;
    //ip
    if((sockfd = socket(AF_INET,SOCK_STREAM, 0)) < 0){
        printf("fail\n");
        return -1;
    }
/*连接服务端*/
    if(connect(sockfd,(AS *)&server_addr,sizeof(server_addr)) < 0){
        printf("fail to connect server\n");
        return -1;
    }
    string baowen = "4"+userName+loginPassword+command;//4用户名登录密码文件名
/*向服务端发送Get命令来获取文件，服务端返回文件是否存在*/
    buf = (char *)baowen.c_str();
    
    send(sockfd, buf, N, 0);

    printf("Rename file successfully!\n");
    close(fd);
    close(sockfd);
    return 1;
}


void PrintHelp()
{
    printf("help : display help info\n");
    printf("List ：request file list\n");
    printf("get  : get <filename>\n");
    printf("put  : put <filename>\n");
    printf("rename  : rename file\n");
    printf("delete  : delete file\n");
    printf("quit : quit the client\n");
}
 
int ProcessGet(string command,string userName,string loginPassword)
{
    struct sockaddr_in server_addr = taojiekou();
    int sockfd,nbyte,fd;
    
    //ip
    if((sockfd = socket(AF_INET,SOCK_STREAM, 0)) < 0){
        printf("fail\n");
        return -1;
    }
/*连接服务端*/
    if(connect(sockfd,(AS *)&server_addr,sizeof(server_addr)) < 0){
        printf("fail to connect server\n");
        return -1;
    }
    
    string baowen = "1"+userName+loginPassword+command;//1用户名登录密码文件名
    /*向服务端发送Get命令来获取文件，服务端返回文件是否存在*/
    char *buf = (char *)baowen.c_str();

    send(sockfd, buf, N, 0);
    recv(sockfd, buf, N, 0);
/*服务端无此文件*/    
    if (buf[0] == 'N') {
        printf("No such file on server\n");
        return -1;
    }
/*mode设为0666，赋予可读可写权限*/
    char *openCommand = (char *)command.c_str();
    if((fd = open(openCommand,O_WRONLY|O_CREAT|O_TRUNC,0666)) < 0){
        printf("fail to create local file %s\n",openCommand);
        return -1;
    }
 
    while((nbyte = recv(sockfd,buf,N,0)) > 0){
        write(fd,buf,nbyte);
    }
    printf("Get file successfully!\n");
    close(fd);
    close(sockfd);
    return 1;
}

int ProcessPut(string command,string userName,string loginPassword)
{
    struct sockaddr_in server_addr = taojiekou();
   // char command[]
    int sockfd,fd,nbyte;
    char *buf;

    if((sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0){
        printf("fail to get\n");
        return -1;
    }
/*连接服务端*/
    if(connect(sockfd,(AS *)&server_addr,sizeof(server_addr)) < 0){
        printf("fail to connect server\n");
    }
/*打开文件*/
    char *openCommand = (char *)command.c_str();
    if((fd = open(openCommand,O_RDONLY)) < 0){
        printf("fail to open %s\n",openCommand);
        return -1;
    }
    string baowen = "2"+userName+loginPassword+command;      
    //sprintf(buf,"2%s%s%s",userName,loginPassword,command);//2用户名登录密码文件名
    //printf("%s\n",buf);
/*告知服务端要上传文件*/   
    buf = (char*)baowen.c_str();
    send(sockfd,buf,N,0);

    while ((nbyte = read(fd,buf,N)) > 0){
        send(sockfd,buf,nbyte, 0);
    }

    printf("Put file successfully!\n");

    close(fd);
    close(sockfd);
    return 1;
}




int main(int argc,char *argv[])
{
    vector<string> fileList;
    char comm[32];
    PrintHelp();

    ProcessDelete("1.pdf","mhq","123456");
    ProcessRename("1.pdf","mhq","123456");
    ProcessList(fileList,"mhq","123456");
    ProcessPut("1.pdf","mhq","123456");
    ProcessGet("1.pdf","mhq","123456");



//     while(1){
//      printf(">> ");
//      fgets(comm,32,stdin);
//      comm[strlen(comm)-1] = '\0'; 
//      if(strcmp(comm,"help") == 0){
//          PrintHelp();
//      }else if(strncmp(comm,"get ",4) == 0){
//          ProcessGet(server_addr,comm);
//      }else if(strncmp(comm,"put ",4) == 0){
//          ProcessPut(server_addr,comm);
//      }else if(strcmp(comm,"quit") == 0){
//          printf("Quit!\n");
//          break;
//      }else if(strcmp(comm, "list") == 0){
//          ProcessList(server_addr,comm,userName,loginPassword);
//      }
//      else if(strcmp(comm, "rename") == 0){
//          ProcessRename(server_addr,comm);
//      }
//      else if(strcmp(comm, "delete") == 0){
//          ProcessDelete(server_addr,comm);
//      }
//      else{
//          printf("warning! Input again.\n");
//    }
// }

return 0;
}
