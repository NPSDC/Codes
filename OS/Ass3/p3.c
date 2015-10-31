#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <errno.h>
#include <assert.h>
#include <sys/shm.h>
#include <sys/types.h>
#include <sys/ipc.h>

key_t key = IPC_PRIVATE;
void print(int *arr, int l, int r)
{
	int i;
	for(i = l; i <= r;i++)
		printf("%d ", arr[i]);
	printf("\n");
}
void selection_sort(int *arr, int l, int r)
{
	int i, j, min_index, temp;
	for(i = 0; i < (r-l); i++)
	{
		min_index = i;
		for(j = i; j <= (r-l); j++)
		{
			if(arr[j] < arr[min_index])
				min_index = j;
		}
		temp = arr[i];
		arr[i] = arr[min_index];
		arr[min_index] = temp;
	}
}
void merge(int *arr, int l, int m, int r)
{
	 int  j, l_start, r_start;
	 l_start = 0;
	 r_start = 0;
	 int left[m - l + 1];
	 int right[r - m];
	 for(j = l; j <= m; j++)
	 	left[j - l] = arr[j];
	 for(j = m + 1; j <= r; j++)
	 	right[j - m -1] = arr[j];
	 for(j = l; j <= r; j++)
	 {
	 	if(l_start >= m-l+1)
	 	{
	 		arr[j] = right[r_start];
	 		r_start++;
	 	}
	 	else if( r_start >= r - m)
	 	{
	 		arr[j] = left[l_start];
	 		l_start++;
	 	}
	 	else if(left[l_start] < right[r_start])
	 	{
	 		arr[j] = left[l_start];
	 		l_start++;
	 	}
	 	else
	 	{
	 		arr[j] = right[r_start];
	 		r_start++;
	 	}

	 }
}

void mergesort(int *arr, int l,  int r)
{
	pid_t pid1, pid2;
	int status, status1;
	if(l < r)
	{		
		int mid = (l + r)/2;
		pid1 = fork();
		if(pid1 == 0)
			mergesort(arr, l, mid);		
		else
		{
			pid2 = fork();
			if(pid2 == 0)
				mergesort(arr, mid + 1, r);
			else
			{
				waitpid(pid1, &status, 0);
				waitpid(pid2, &status1, 0);
				if((l - r) < 5)
					selection_sort(arr, l , r);
				else
					merge(arr, l, mid, r);
			}
		}
	}
}
int main()
{
	int *arr;
	int i, shmid, n;
	scanf("%d",&n);

	if((shmid=shmget(key, sizeof(int) *n, IPC_CREAT| 0666)) < 0)
    {
        perror("Shmget failed");
        exit(1);
    }
    
    if((arr = shmat(shmid, 0, 0)) == (int *) -1)
    {
        perror("Shmat failed");
        exit(1);
    }
    for(i = 0; i < n; i++)
		scanf("%d",&arr[i]);
	mergesort(arr, 0 ,n - 1);
	//for(i = 0; i < n; i++)
		//printf("%d ",arr[i]);
	printf("\n");
	return 0;
}