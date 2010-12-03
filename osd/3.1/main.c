#define _XOPEN_SOURCE 500
#include <assert.h>
#include <ftw.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>

#define NUM_THREADS 1
#define MAX_DIRS 10
#define MAX_DEPTH 10

char *dirlist[MAX_DIRS];
pthread_mutex_t dirlist_acc;

int
count_dirlist()
{
    int counter = 0;
    int position = 0;
    while(position < MAX_DIRS)
    {
        if(dirlist[position] != 0)
            counter++;
        position++;
    }
    return counter;
}

char
*read_dirlist()
{
    int position = 0;
    while(position < MAX_DIRS)
    {
        if(dirlist[position] != 0)
        {
            printf("FOUND: %s\n",dirlist[position]);
            //return dirlist[position];
            //break;
        }
        position++;
    }
    return 0;
}

int
check_duplicates(char *path)
{
    int index = 0;
    while(index < MAX_DIRS)
    {
        if(dirlist[index] != 0 && strcmp(dirlist[index], path) == 0)
        {
            return 1;
            break;
        }
        index++;
    }
    return 0;
}

void
add_dir(char *path)
{
   int position = 0;

   if( check_duplicates(path) == 1 )
       return 0;
   // find a free position in fifo
   while(position < MAX_DIRS)
   {
       if(dirlist[position] == 0)
       {
           pthread_mutex_lock(&dirlist_acc); 
           dirlist[position] = (char *) malloc( sizeof(path) );
           if(dirlist[position] != 0)
           {
               printf("add_dir: adding path: %s to dirlist index: %d\n", path, position);
               dirlist[position] = path;
               printf("add_dir: added path: %s to dirlist index: %d\n", dirlist[position], position);
               pthread_mutex_unlock(&dirlist_acc); 
               break;
           }
           else
           {
               printf("add_dir: Could not allocate memory.\n");
               return 0;
           }
           
       }
       position++;
   }
}

void
del_dir(char *path)
{
   int position = 0;
   // find a free position in fifo
   while(position < MAX_DIRS)
   {
       if(dirlist[position] != 0)
       {
           if(dirlist[position] != 0 && strcmp(dirlist[position], path) == 0)
           {
               printf("Deleting %s\n", path);
               pthread_mutex_lock(&dirlist_acc); 
               dirlist[position] = 0;
               pthread_mutex_unlock(&dirlist_acc); 
               break;
           }
       }
       position++;
   }
}

static int
add_dir_wrapper(const char *fpath, const struct stat *sp, int tf, struct FTW *pfwt)
{
    char *new_path = fpath;
    printf("New path: %s\n", fpath);
    if(tf == FTW_D && pfwt->level == 1) 
    {
        printf("add_dir_wrapper: adding path: %s\n", new_path);
        add_dir(new_path);
    }
    return 0;
}

void
build_dirlist(char *path)
{
    nftw(path, add_dir_wrapper, MAX_DEPTH, 0);
}

void
*do_search(void *thread_id)
{
    int tid;
    int cur_queue = count_dirlist();
    tid = *((int *) thread_id);
    printf("Thread %d started with %d dirs in queue...\n", tid, cur_queue);
    while(cur_queue => 1)
    {
        char *path = read_dirlist();
        if(path != NULL)
        {
            build_dirlist(path);
            printf("do_search: Thread %d found a new path: %s\n", tid, path);
            del_dir(path);
        }
        cur_queue = count_dirlist();
    }
    printf("do_search: Directory list is empty. Thread %d terminates.\n", tid);
    return NULL;
}

int
main (int argc, char *argv[])
{
    pthread_t threads[NUM_THREADS];
    int thread_args[NUM_THREADS];
    int rc, i;
    char *search_s, *search_p;

    /* read our arguments */
    if( argc >= 3 ) {
        search_s = (char *) malloc( sizeof( argv[1] ) );
        search_p = (char *) malloc( sizeof( argv[2] ) );
        if( search_s != 0 )
            search_s = argv[1];
        else {
            printf("main: Could not allocate memory.\n");
            exit(EXIT_FAILURE);
        }

        if( search_p != 0 )
            search_p = argv[2];
        else {
            printf("main: Could not allocate memory.\n");
            exit(EXIT_FAILURE);
        }
    } else {
        printf("Nothing to search for. Exiting...\n");
        exit(EXIT_SUCCESS);
    }

    printf("Searching for: '%s' in '%s', using %d threads...\n", search_s, search_p, NUM_THREADS);
    add_dir(search_p);
    //build_dirlist(search_p);

    /* create all threads */
    for (i=0; i<NUM_THREADS; ++i) {
        thread_args[i] = i;
        rc = pthread_create(&threads[i], NULL, do_search, (void *) &thread_args[i]);
        assert(0 == rc);
    }

    /* wait for all threads to complete */
    for (i=0; i<NUM_THREADS; ++i) {
        rc = pthread_join(threads[i], NULL);
        assert(0 == rc);
    }

    exit(EXIT_SUCCESS);
}
