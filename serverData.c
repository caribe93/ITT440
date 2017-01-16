#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <wiringPi.h>
 
const int ledPin = 23; //Green LED position

int main(void)
{
	wiringPiSetupGpio();
	pinMode(ledPin, OUTPUT);
	int listenfd = 0;
	int connfd = 0;
	struct sockaddr_in serv_addr;char sendBuff[1025];
	int numrv;

	listenfd = socket(AF_INET, SOCK_STREAM, 0);

	printf("Socket retrieve success\n");

	memset(&serv_addr, '0', sizeof(serv_addr));
	memset(sendBuff, '0', sizeof(sendBuff));

	serv_addr.sin_family = AF_INET;
	serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
	serv_addr.sin_port = htons(5000);

	bind(listenfd, (struct sockaddr*)&serv_addr,sizeof(serv_addr));

	if(listen(listenfd, 10) == -1)
	{
		printf("Failed to listen\n");
        	return -1;
    	}

    	while(1)
    	{
        	connfd = accept(listenfd, (struct sockaddr*)NULL ,NULL);

        	/* Open the file that we wish to transfer */
        	FILE *fp = fopen("data.txt","rb");
        	if(fp==NULL)
        	{
            		printf("File open error");
            		return 1;   
        	}   

        	/* Read data from file and send it */
        	while(1)
        	{
            		/* First read file in chunks of 256 bytes */
            		unsigned char buff[256]={0};
            		int nread = fread(buff,1,256,fp);

	    		/*display text file content. */
	    		//system("cat data.txt");

            		/* If read was success, send data. */
            		if(nread > 0)
            		{
                		printf("Sending \n");
                		write(connfd, buff, nread);
            		}

            		/*reading the file created*/
            		if (nread < 256)
            		{
                		if (feof(fp))
                    			printf("End of file\n");
                		if (ferror(fp))
                    			printf("Error reading\n");
                		break;
            		}
        	}
		close(connfd);
	digitalWrite(ledPin, HIGH);
        delay(100);
        digitalWrite(ledPin,LOW);
        delay(100);
        digitalWrite(ledPin, HIGH);
        delay(100);
        digitalWrite(ledPin,LOW);
        delay(100);
        printf("Green LED blinks two times indicating data successfully updated\n\n");
		/*display text file content. */
		printf("\n\n");
                system("cat data.txt");
		sleep(1);
	}
	return 0;
}

