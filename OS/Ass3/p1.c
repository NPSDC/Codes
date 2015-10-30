#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <errno.h>
#include <assert.h>
#include <time.h>
#define ErrorHandler(msg) \
	do {perror(msg);exit(EXIT_FAILURE);}while(0)

int n, no_of_threads,end = 0;
int *write; //makes sure buffer is not rewritten before being read
int *count; //makes sure that every buffer is read before being rewritten
pthread_mutex_t lock;
pthread_mutex_t lock_read;
char *buffer;

typedef struct thread_var
{
	int id;
	int *read;//makes sure that every buffer is read only once
}thread_var;

void *read_buffer(void *th)
{
	int thread_id = (*(thread_var *)th).id;
	printf("read %d\n", thread_id);
	int i = 0, j;	
	while(1)
	{
		if(write[i%n] == 0)
		{
			pthread_mutex_lock(&lock_read);
			
			if((*(thread_var *)th).read[i%n] == 0)
			{
				printf("%d %c %d\n", thread_id, *(char *)(buffer + i%n), i%n);
				count[i%n]++;
				(*(thread_var *)th).read[i%n] = 1;
			}
			if(count[i%n] == no_of_threads)
			{
				write[i%n] = 1;
				count[i%n] = 0;
			}
			
			//end++;
			//printf("end %d\n", end);
			pthread_mutex_unlock(&lock_read);
		}
		i++;
		if(end == 1)
		{
			int c = 0;
			for(j = 0; j < n; j++)
			{
				if(write[j] == 1)
					c++;
			}
			if(c == n)
				break;
		}
		/*else
		{
			printf("En%d %d\n", thread_id, i%n);
			(*(thread_var *)th).read[i%n] = 0;
		}*/
		
		//i++;
	}
	
}

void *write_buffer(void *th)
{
	int i = 0,j;	
	char c;
	printf("write\n");
	while(i < 100)
	{
		if(write[i%n] == 1)
		{
			pthread_mutex_lock(&lock);
			c = rand()%26 + 97;
			buffer[i%n] = c;
			write[i%n] = 0;
			for(j = 0; j < no_of_threads; j++)
			{
				(*((thread_var *)th + j )).read[i%n] = 0;
			}
			printf("%d %c write\n", i%n, c);
			i++;
			pthread_mutex_unlock(&lock);			
		}
		//i++;
		
	}
	end = 1;
}

int main()
{
	int i, rc,t;
	pthread_t *tid1, tid2;
	thread_var *th;
	printf("Enter size of buffer\n");	
	scanf("%d",&n);

	printf("Enter no of threads\n");
	scanf("%d",&no_of_threads);

	th = (thread_var *)malloc(sizeof(thread_var)*no_of_threads);
	for(i = 0; i < no_of_threads; i++)
	{
		th[i].id = i + 1;
		th[i].read = (int *)malloc(sizeof(int)*n);
		for(t = 0; t < n; t++)
			th[i].read[t] = 1;
	}

	write = (int *)malloc(sizeof(int) * n);
	for(i = 0; i < n; i++)
		write[i] = 1;

	count = (int *)malloc(sizeof(int) * n);
	for(i = 0; i < n; i++)
		count[i] = 0;

	tid1 = (pthread_t *)malloc(sizeof(pthread_t)*no_of_threads);
	buffer = (char *)malloc(sizeof(char)*n);

	rc = pthread_create(&tid2, NULL, write_buffer, th);
	assert(rc == 0);

	for(i = 0;i < no_of_threads; i++)
	{		
		rc = pthread_create(&tid1[i], NULL, read_buffer, &th[i]);
		assert(rc == 0);
	}
	rc = pthread_join(tid2, NULL);
	for(i = 0;i < no_of_threads; i++)
	{
		rc = pthread_join(tid1[i], NULL);
		//assert(rc == 0);
	}
	return 0;
}