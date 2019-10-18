#include "bdCloud_Lib.h"

int recv_header(int sock_fd,char *buf,int *auth)
{
	if(recv(sock_fd,(void*)buf,MAX_BUF_SIZE,0) < 0)
	{
		perror("Error: fail to recv!\n");
		exit(1);
	}
	else
	{
		*auth=((buf[1]=='A')?1:0);
		if(*auth==1)
		{
			if(strncmp(&buf[2],ADMIN_PSD,PSD_LEN)==0)
			{
				return (int)(buf[0]-'0');
			}
			else
			{
				*auth=-1;
				return -1;
			}
		}
		else
		{
			if(strncmp(&buf[2],USER_PSD,PSD_LEN)==0)
			{
				return (int)(buf[0]-'0');
			}
			else
			{
				*auth=-1;
				return -1;
			}
		}
	}
}