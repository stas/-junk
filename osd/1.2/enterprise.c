#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <sys/wait.h>

void kirk_logs(int sig)
{
    int ch;
    char *path = "/tmp/kirk.log";
    char msg[101] = {0};
    FILE *f = fopen(path,"a+");
    if(NULL != f)
    {
        printf("Kirk, say something:\n");
        fread(msg, 1, 100, stdin);
        fprintf(f,"%s",msg);
        fclose(f);
    }
    else
        printf("No log found\n");

}

int enterprise_to_spock(void)
{
    char *ext_name = "spock";
    //char *ext_name = "nginx";
    int ext_pid;
    FILE *file;
    char *path = "/tmp/spock.pid";

    while(1)
    {
        file = fopen(path,"r");
        if(NULL != file)
        {
            fscanf(file,"%d", &ext_pid);
            printf("Enterprise, %s is at: %d, sending signal...\n", ext_name, ext_pid);
            kill(ext_pid,SIGUSR1);
            fclose(file);
        }
        else
            printf("Enterprise can't find %s\n", ext_name);
    }

    exit(0);
}

int main(void)
{
    pid_t pid;

    char *pidfile = "/tmp/enterprise.pid";
    FILE *pf = fopen(pidfile,"r");
    if(NULL == pf)
    {
        pf = fopen(pidfile,"w");
        fprintf(pf,"%d\n",getpid());
        fclose(pf);
    }
    else
    {
        printf("One USS is enough for our galaxy\n");
        exit(1);
    }

    // Handle SIGUSR1
    signal(SIGUSR1, kirk_logs);

    enterprise_to_spock();

    unlink(pidfile);
    return 0;
}
