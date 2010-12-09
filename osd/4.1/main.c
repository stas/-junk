#define _REENTRANT    /* basic 3-lines for threads */
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <string.h>
#include <assert.h>

#if defined (__SVR4) && defined (__sun)
#include <thread.h>
#endif 

#define NUM_THREADS 3
#define MAX_NUMS 100

int array[MAX_NUMS];
int f_half[MAX_NUMS/2];
int s_half[MAX_NUMS/2];
int elements;

void print_array(int array[])
{
    int i;
    printf("ARRAY[");
    for(i=0;i<=elements;i++)
        printf("%d,", array[i]);
    printf("]\n");
}

void *
sorting(void *thread_id)
{
    int tid;
    tid = *((int *) thread_id);

    return NULL;
}

void *
do_sort(void *thread_id)
{
    int tid, rc, i;
    tid = *((int *) thread_id);
    pthread_t threads[NUM_THREADS];
    int tids[NUM_THREADS];

    /* create all threads */
    for (i=1; i<NUM_THREADS; ++i) {
        printf("do_sort: Thread %d starts....\n", i);
        tids[i] = i;
        rc = pthread_create(&threads[i], NULL, sorting, (void *) &tids[i]);
        assert(0 == rc);
    }

    /* wait for all threads to complete */
    for (i=1; i<NUM_THREADS; ++i) {
        printf("do_sort: Thread %d terminates.\n", i);
        rc = pthread_join(threads[i], NULL);
        assert(0 == rc);
    }

    printf("do_sort: Thread %d terminates.\n", tid);
    return NULL;
}

void
read_file(char *filename)
{
    int index = 0;
    FILE *fh = fopen(filename,"r");
    if(fh != NULL)
        while( fscanf(fh, "%d", &array[index]) != EOF)
        {
            index++;
        }
    elements = index;
    fclose(fh);
}

int
main (int argc, char *argv[])
{
    int rc, i;
    char *filename = 0;
    pthread_t thread;
    int thread_arg = 0;

    /* read our arguments */
    if( argc == 2 ) {
        filename =  malloc( strlen( argv[1] )+1 );
        if( filename != 0 )
            filename = argv[1];
        else {
            printf("main: Could not allocate memory.\n");
            exit(EXIT_FAILURE);
        }
    } else {
        printf("Nothing to sort. Exiting...\n");
        exit(EXIT_SUCCESS);
    }

    printf("Sorting from %s...\n", filename);
    read_file(filename);
    print_array(array);
    
    rc = pthread_create(&thread, NULL, do_sort, (void *) &thread_arg);
    assert(0 == rc);

    rc = pthread_join(thread, NULL);
    assert(0 == rc);

    exit(EXIT_SUCCESS);
}
