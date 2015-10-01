#include <stdio.h>
#include <unistd.h>
#include <pwd.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <signal.h>
#include <wait.h>
#define MAX 1024

void print(char *arr[], int l)
{
	int i;
	for(i = 0; i < l ; i++)
		printf("%s ", arr[i]);
	printf("\n");
}

int main()
{
	pid_t pid, pid2;
	int i,j,k, flag;
	int fd[2], prevfd[2], stdfd[2];
	char *commands[MAX]; //structure  given by user			
	char *commands1[MAX];
	char *token;
	char arr[MAX];
	while(1)
	{
		scanf(" %[^\n]s",arr);
		token = strtok(arr, " |");
		i = 0;
		k = 0;
		flag = 0;
		while(token != NULL)
		{
			commands[i] = token;
			token = strtok(NULL, " |");
			i++;
		}
		//printf("%d\n", i);
		//print(commands, i);
		for(j = 0; j < i; j++)
		{
			commands1[0] = commands[j];
			commands1[1] = NULL;
			if(j < i-1)
			{
				pipe(fd);	
			}
	
			pid = fork();			
			if(pid == 0)
			{
				if(j > 0)
				{
					close(prevfd[1]);
					dup2(prevfd[0], 0);
					close(prevfd[0]);	
				}
				if(j < i-1)
				{
					close(fd[0]);
					dup2(fd[1], 1);
					close(fd[1]);	
				
				}
				execvp(commands1[0], commands1);
			}
			else
			{
				if(j>0){
					close(prevfd[0]);
					close(prevfd[1]);
				}
				if(j<i-1){
					prevfd[0] = fd[0];
					prevfd[1] = fd[1];
				}
				wait(NULL);								
				

			}
			if(flag == 0)
				flag = 1;
		}
			
		
	}
	return 0;
}