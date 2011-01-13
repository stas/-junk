#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <string.h>

#define PORT 5555
#define HOST "localhost"
#define SIZE 256

int 
main( int argc, char **argv)
{
    char hostname[100] = HOST;
    int port = PORT;
	char msg[SIZE];
	int	sd;
	struct sockaddr_in sin;
	struct sockaddr_in pin;
	struct hostent *hp;

    if (argc > 1)
    {
        strcpy (msg, argv[1] );
        printf ("Asking about %s...\n", msg);
    }
    else
    {
        printf ("Nothing to send!\n");
        exit(EXIT_FAILURE);
    }

    if (argc > 2)
    {
        strcpy (hostname, argv[2] );
    }
    
    if (argc > 3)
    {
        port = atoi (argv[3]);
    }

	if ((hp = gethostbyname(hostname)) == 0) {
		perror("gethostbyname");
		exit(EXIT_FAILURE);
	}

	memset(&pin, 0, sizeof(pin));
	pin.sin_family = AF_INET;
	pin.sin_addr.s_addr = ((struct in_addr *)(hp->h_addr))->s_addr;
	pin.sin_port = htons(port);

	if ((sd = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
		perror("socket");
		exit(EXIT_FAILURE);
	}

	if (connect(sd,(struct sockaddr *)  &pin, sizeof(pin)) == -1) {
		perror("connect");
		exit(EXIT_FAILURE);
	}

	if (send(sd, msg, strlen(msg), 0) == -1) {
		perror("send");
		exit(EXIT_FAILURE);
	}

    if (recv(sd, msg, SIZE, 0) == -1) {
            perror("recv");
		    exit(EXIT_FAILURE);
    }
    else
    {
        printf("Server responded:\n\t%s\n", msg);
    }

	close(sd);
}

 
