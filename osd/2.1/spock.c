#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <sys/wait.h>

void kirks_log(int sig)
{
    int ch;
    char *path = "/tmp/kirk.log";
    FILE *f = fopen(path,"r");
    if(NULL != f)
    {
        while((ch = getc(f)) != EOF)
            putc(ch, stdout);
        fclose(f);
        unlink(path);
    }
    else
        printf("No log found\n");

}

int spock_to_enterprise(void)
{
    char *ext_name = "enterprise";
    //char *ext_name = "nginx";
    int ext_pid;
    FILE *file;
    char *path = "/tmp/enterprise.pid";

    while(1)
    {
        file = fopen(path,"r");
        if(NULL != file)
        {
            fscanf(file,"%d", &ext_pid);
            printf("Spock, %s is at: %d, sending signal...\n", ext_name, ext_pid);
            kill(ext_pid,SIGUSR1);
            fclose(file);
        }
        else
            printf("Spock, %s is down\n", ext_name);
        usleep(random()/30);
    }

    exit(0);
}

int main(void)
{
    pid_t pid;

    char *pidfile = "/tmp/spock.pid";
    FILE *pf = fopen(pidfile,"r");
    if(NULL == pf) 
    {   
        pf = fopen(pidfile,"w");
        fprintf(pf,"%d\n",getpid());
        fclose(pf);
    }   
    else
    {   
        printf("Spock didn't die yet\n");
        exit(1);
    }   


    // Handle SIGUSR1
    signal(SIGUSR1, kirks_log);

    spock_to_enterprise();
    
    unlink(pidfile);
    return 0;
}
