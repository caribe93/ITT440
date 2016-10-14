#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <netdb.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <arpa/inet.h>

int main(void)
{
    int sockfd = 0;
    int years = 0;
    char name[100];
    char suID[100];
    float salary = 0.0;
    int bytesReceived = 0;
    char recvBuff[256];
    memset(recvBuff, '0', sizeof(recvBuff));
    struct sockaddr_in serv_addr;

    /* Create a socket first */
    if((sockfd = socket(AF_INET, SOCK_STREAM, 0))< 0)
    {
        printf("\n Error : Could not create socket \n");
        return 1;
    }

    /* Initialize sockaddr_in data structure */
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(5000); // port
    serv_addr.sin_addr.s_addr = inet_addr("127.0.0.1");

    /* Attempt a connection */
    if(connect(sockfd, (struct sockaddr *)&serv_addr, 
sizeof(serv_addr))<0)
    {
        printf("\n Error : Connect Failed \n");
        return 1;
    }

    /* Create file where data will be stored */
    FILE *fp;
    fp = fopen("data.txt", "ab"); 
    if(NULL == fp)
    {
        printf("Error opening file");
        return 1;
    }
	printf("Enter name :\n");
	scanf ("%s",&name);
	fprintf(fp, "NAME    = %s\n", name);

	printf("Enter salary :\n");
	scanf("%f",&salary);
	fprintf(fp, "SALARY  = RM %.2f\n", salary);

	printf("Enter years of service :\n");
	scanf("%d",&years);
	fprintf(fp, "SERVICE = %d\n", years);

	printf("Enter supervisor ID :\n");
	scanf("%s",&suID);
	fprintf(fp, "SU ID   = %s\n", suID);
	fprintf(fp, "\n\n");

    /* Receive data in chunks of 256 bytes */
    while((bytesReceived = read(sockfd, recvBuff, 256)) > 0)
    {
        printf("Bytes received %d\n",bytesReceived);    
        //recvBuff[n] = 0;
        //fwrite(recvBuff, 1,bytesReceived,fp);
	//fprintf(fp, "content of file \n");
        //printf("%s \n", recvBuff);
    }

    if(bytesReceived < 0)
    {
        printf("\n Read Error \n");
    }


    return 0;
}
