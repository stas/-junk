#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <pthread.h>
#include <assert.h>

#define DEF_PORT 5555
#define MAX_SIZE 256
#define MAX_CLIENTS 5

pthread_mutex_t clients_lock;
int clients[MAX_CLIENTS];

struct thread_data{
    int  thread_id;
    int  connection;
};

int
start_server (uint16_t port)
{
    int sock;
    struct sockaddr_in name;

    /* Create the socket. */
    sock = socket (PF_INET, SOCK_STREAM, 0);
    if (sock < 0)
    {
        perror ("socket");
        exit (EXIT_FAILURE);
    }

    /* Give the socket a name. */
    name.sin_family = AF_INET;
    name.sin_port = htons (port);
    name.sin_addr.s_addr = htonl (INADDR_ANY);
    if (bind (sock, (struct sockaddr *) &name, sizeof (name)) < 0)
    {
        perror ("bind");
        exit (EXIT_FAILURE);
    }

    if (listen(sock, MAX_CLIENTS) < 0 ) 
    {
        perror ("listen");
        exit (EXIT_FAILURE);
    }

    return sock;
}

void
check_msg (char *msg, int connection)
{
    // Trim newline on console input
    //msg[strlen(msg)-1]='\0';

    char result1[MAX_SIZE];
    char result2[MAX_SIZE];
    FILE *pipe;
    char online_cmd[MAX_SIZE];
    sprintf(online_cmd, "users |grep %s ", msg);
    char last_cmd[MAX_SIZE];
    sprintf(last_cmd, "last | grep logged | wc -l ");

    printf("Running: %s \n", online_cmd);
    pipe = popen (online_cmd, "r");
    fgets(result1, MAX_SIZE, pipe);
    pclose(pipe);
    if( strlen(result1) > 1 )
    {
        strcpy (msg, "User is logged in now. ");

        printf ("Running: %s \n", last_cmd);
        pipe = popen (last_cmd, "r");
        fgets (result2, MAX_SIZE, pipe);
        strcat (msg, "Current number of users logged in: ");
        strcat (msg, result2);
        write (connection, msg, strlen(msg));
        pclose (pipe);
    }
    else
        write (connection, "User is not logged in now. \n", 29);

}

void
*connection_handler (void *args)
{
    struct thread_data *data = (struct thread_data *) args;
    int id = data->thread_id;
    int connection = data->connection;
    char *msg = malloc( MAX_SIZE * sizeof(char));

    read (connection, msg, MAX_SIZE - 1 );
    check_msg (msg, connection);
    write (connection, "Bye...\n", 8);
   
    if ( close(connection) < 0 )
    {
        perror("close");
        exit(EXIT_FAILURE);
    }

    pthread_mutex_lock(&clients_lock); 
    clients[id] = 0;
    pthread_mutex_unlock(&clients_lock); 
}

int
find_free_slot()
{
    int i;
    for( i = 0; i < MAX_CLIENTS; i++)
        if (clients[i] == 0)
            return i;

    return MAX_CLIENTS;
}

int
main (int argc, char *argv[])
{
    int port = DEF_PORT;
    int server = 0;
    int connection = 0;
    int slot = 0;
    int i, rc;

    pthread_t threads[MAX_CLIENTS];
    struct thread_data thread_args[MAX_CLIENTS];

    if (argc == 2)
    {
        port = atoi(argv[1]);
    }

    printf("The server will start on localhost using port: %d\n", port);

    server = start_server (port); 
    if (server == 0)
    {
        printf ("Server could not start, exiting...\n");
        exit (EXIT_FAILURE);
    }

    while (1) 
    {
        if (slot >= MAX_CLIENTS)
        {
            //printf ("Maximum number of clients already, please wait...\n");
            slot = find_free_slot();
        }
        else
        {
            if( (connection = accept(server, NULL, NULL) ) < 0)
            {
                perror ("accept");
                exit(EXIT_FAILURE);
            }
        }

        if ( connection )
        {
            slot = find_free_slot();

            printf("Connection: %d\n", slot);

            pthread_mutex_lock(&clients_lock); 
            clients[slot] = connection;
            pthread_mutex_unlock(&clients_lock); 

            thread_args[slot].thread_id = slot;
            thread_args[slot].connection = connection;
            rc = pthread_create(&threads[slot], NULL, connection_handler, (void *) &thread_args[slot]);
            assert(0 == rc);
            connection = 0;
        }
    }

    for (i=0; i < MAX_CLIENTS; ++i)
    {
        rc = pthread_join(threads[i], NULL);
        assert(0 == rc);
    }

    exit (EXIT_SUCCESS);
}
