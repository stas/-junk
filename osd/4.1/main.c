#define _REENTRANT    /* basic 3-lines for threads */
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <string.h>
#include <assert.h>
#include <time.h>

#if defined (__SVR4) && defined (__sun)
#include <thread.h>
#endif 

#define NUM_THREADS 3
#define MAX_NUMS 100

int array[MAX_NUMS];
int *f_half;
int *s_half;
int elements;

void print_array(int array[], int len)
{
    int i;
    printf("ARRAY[");
    for(i=0;i<len;i++)
        printf("%d,", array[i]);
    printf("]\n");
}

int
intcmp(const void *p1, const void *p2)
{
    int i = *((int *)p1);
    int j = *((int *)p2);

    if (i > j)
        return (1);
    if (i < j)
        return (-1);
    return (0);
}

void *
sorting(void *thread_id)
{
    int tid, i;
    tid = *((int *) thread_id);

    if(tid == 1)
    {
        f_half = malloc(elements/2);
        f_half = &array[0];
        qsort(f_half, elements/2, sizeof(int), intcmp);
    }
    else
    {
        s_half = malloc(elements/2);
        s_half = &array[elements/2];
        qsort(s_half, elements/2, sizeof(int), intcmp);
    }
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
    
    // Concatenate
    array[0] = f_half[0];
    array[elements/2] = s_half[0];
    qsort(array, elements, sizeof(int), intcmp);
    print_array(array, elements);

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
    struct timespec start, finish;
    clock_gettime(CLOCK_MONOTONIC, &start);

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
    print_array(array, elements);

    rc = pthread_create(&thread, NULL, do_sort, (void *) &thread_arg);
    assert(0 == rc);

    rc = pthread_join(thread, NULL);
    assert(0 == rc);

    clock_gettime(CLOCK_MONOTONIC, &finish);
    printf("Used time: %f\n", (finish.tv_sec - start.tv_sec) + (finish.tv_nsec - start.tv_nsec) / 1000000000.0 );
    exit(EXIT_SUCCESS);
}
