#define _XOPEN_SOURCE 500
#include <assert.h>
#include <ftw.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <fnmatch.h>

#define NUM_THREADS 3
#define MAX_DIRS 10
#define MAX_DEPTH 10

char *search_s;
char *dirlist[MAX_DIRS];
pthread_mutex_t dirlist_acc[MAX_DIRS]; 

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

int
read_dirlist()
{
    int position = 0;
    while(position < MAX_DIRS)
    {
        if(dirlist[position] != 0 && 0 == pthread_mutex_trylock(&dirlist_acc[position]))
        {
            return position;
            break;
        }
        position++;
    }
    return -1;
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

int
add_dir(char *path)
{
   int position = 0;
   int len = strlen(path);

   if( check_duplicates(path) == 1 )
       return 0;
   // find a free position in fifo
   while(position < MAX_DIRS)
   {
       if(dirlist[position] == 0)
       {
           pthread_mutex_lock(&dirlist_acc[position]); 
           dirlist[position] = malloc( len+1 );
           if(dirlist[position] != 0)
           {
               strncpy(dirlist[position], path, len);
           }
           else
           {
               printf("add_dir: Could not allocate memory.\n");
               return 0;
           }
           pthread_mutex_unlock(&dirlist_acc[position]); 
           break;
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
               dirlist[position] = 0;
               break;
           }
       }
       position++;
   }
}

static int
add_dir_wrapper(const char *fpath, const struct stat *sp, int tf, struct FTW *pfwt)
{
    char *new_path = malloc( strlen(fpath)+1 );
    strncpy(new_path,fpath, strlen(fpath));
    if(tf == FTW_D && pfwt->level == 1) 
    {
        add_dir(new_path);
    }
    return 0;
}

void
build_dirlist(char *path)
{
    nftw(path, add_dir_wrapper, MAX_DEPTH, 0);
}

static int
ffile_wrapper(const char *fpath, const struct stat *sp, int tf, struct FTW *pfwt)
{
    if(tf == FTW_F && pfwt->level == 1) 
    {
        if(fnmatch(search_s, fpath, 0) == 0)
            printf("\tFOUND MATCH: %s\n", fpath);
    }
    return 0;
}

void
find_in_dir(char *path)
{
    nftw(path, ffile_wrapper, MAX_DEPTH, 0);
}

void
*do_search(void *thread_id)
{
    int tid;
    int cur_queue = count_dirlist();
    int position = -1;
    tid = *((int *) thread_id);
    printf("Thread %d started with %d dirs in queue...\n", tid, cur_queue);
    while(cur_queue != 0)
    {
        // Catch a lock
        do {
            position = read_dirlist();
        } while (position < 0 && count_dirlist() != 0);

        if(position < 0)
            break;

        char *path = dirlist[position];
        if(path != NULL)
        {
            build_dirlist(path);
            printf("do_search: Thread %d found a new path: %s\n", tid, path);
            find_in_dir(path);
            del_dir(path);
        }
        if(position >= 0)
            pthread_mutex_unlock(&dirlist_acc[position]); 
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
    char *search_p;

    /* read our arguments */
    if( argc >= 3 ) {
        search_s =  malloc( strlen( argv[1] )+1 );
        search_p =  malloc( strlen( argv[2] )+1 );
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
