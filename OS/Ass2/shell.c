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

void get_user_name(char user_name[MAX])
{
	struct passwd *p = getpwuid(getuid());
	if(p != NULL)
	{
		strcpy( user_name, p->pw_name);
		printf("%s@", user_name);
	}
	else
		perror("");
}
void get_host_name(char *hostname)
{
	gethostname(hostname, MAX + 1);
	if(hostname)
		printf("%s:", hostname);	
	else
		perror("Error");	
}

void get_current_directory(char *cwd)
{
	getcwd(cwd, MAX);
	if(cwd == NULL)
		perror("Error");
}
void print(char *arr[], int l)
{
	int i;
	for(i = 0; i < l ; i++)
		printf("%s ", arr[i]);
	printf("\n");
}

int get_last(char *hwd)
{
	int i = 0;
	int l = strlen(hwd);
	int ans = -1;
	for(i = 0; i < l; i++)
	{
		if(hwd[i] == '/')
			ans = i;
	}
	return ans;
}
void set_directory(char *hwd, char *cwd, char* output) //sets the current directory
{
	int l = strlen(output);
	if(output[0] == '~')
	{
		if(l == 1)
			strcpy(output, hwd);
		else if(l >= 3)
			strcpy(output, strstr(output, &output[2]));
	}
	int er = chdir(output);
	if(er < 0)
		perror("Error");
	get_current_directory(cwd);
}
void set_print_wd(char *hwd, char *cwd, char *print_wd)
{
	char *cmp;
	int l = strlen(hwd);
	cmp = strstr(cwd, hwd);
	if(strcmp(hwd, cwd) == 0)
	{
		strcpy(print_wd, "~");
	}
	
	if(cmp)
	{
		strcpy(&print_wd[1],&cwd[l]);
	}
	else
		strcpy(print_wd, cwd);
	
}
int main()
{
	pid_t pid;
	int run = 1,i;
	char user_name[MAX],host_name[MAX],hwd[MAX],cwd[MAX],print_wd[MAX]; //print_wd contains the format in which directory is printed, hwd home and cwd current
	char *commands[MAX]; //structure  given by user			
	char *token;
	char Inp_file[100];
	char Out_file[100];
	char dump[100];
	char arr[MAX];
	const char del[2] = " ";
	
	get_user_name(user_name);	
	get_host_name(host_name);
	get_current_directory(hwd);
	strcpy(cwd , hwd);
	strcpy(print_wd, "~");
	printf("~$ ");
	int flag_W = 0, flag_R_O = 0, flag_R_A = 0;
	while(run)
	{
		
		i = 0;
		flag_W = flag_R_A = flag_R_O = 0;
		scanf(" %[^\n]s",arr);
		token = strtok(arr, " ");
		//commands[0] = token;
		while(token != NULL)
		{	
			//printf("%s %d YES\n", token, i);
			if(strcmp(token, "<") == 0)
			{
				token = strtok(NULL, " ");
				strcpy(Inp_file , token);
				//printf("%s\n", Inp_file);
				flag_W = 1;
			}	
			else if(strcmp(token, ">") == 0)
			{
				
				token = strtok(NULL, " ");
				strcpy(Out_file , token);
				flag_R_O = 1;
			}
			else if(strcmp(token, ">>") == 0)
			{
				token = strtok(NULL, " ");
				strcpy(Out_file , token);
				flag_R_A = 1;
			}
			else
			{
				//printf("%d\n", i);
				//printf("%d %d %d\n", flag_W, flag_R_A, flag_R_O);
				if(flag_W == 0 && flag_R_A == 0 && flag_R_O == 0)
				{//commands[i-1] = "\0";
					
					commands[i] = token;
					i++;
					//printf("%s\n", commands[i]);
					
				}
				//printf("%d\n", i);
				
				token = strtok(NULL, " ");
				//strcpy(dump, token);
				//i++;				
			}
			
		}
		//print(commands, i);
		if(strlen(commands[0]) > 1)
		{
			if(commands[0][0] == 'l' && commands[0][1] == 's')
			{	commands[i] = "--color=auto";
			i++;
			}
		}
		
		commands[i] = NULL;
	//	printf("%d\n", i);
	//	print(commands, i);
		if(arr[0] == 'c' && arr[1] == 'd')
		{
			if(commands[1] != NULL)	
				set_directory(hwd, cwd, commands[1]);
			else
				set_directory(hwd, cwd, hwd);
				
			set_print_wd(hwd, cwd, print_wd);
		}
		else
		{
			pid = fork();
			char *error[3] = {"echo", commands[0], ": command not found"};
			if(pid < 0)
			{
				perror("Could not create child\n");
				_exit(-1);
			}
			else if(pid == 0)
			{
				int ret;
				int f;

				if(flag_W == 1)
				{
					//printf("YES\n");
					f = open(Inp_file,  O_RDONLY | O_CREAT, S_IRWXU);
					dup2(f, 0);
				    close(f);	
				}

				if(flag_R_O || flag_R_A)
				{

					if(flag_R_O)
		 				f = open(Out_file, O_WRONLY |  O_CREAT, S_IRWXU);
		 			else
		 				f = open(Out_file, O_APPEND | O_WRONLY |  O_CREAT, S_IRWXU);

				    dup2(f, 1);
				    close(f);
				}
				//printf("%d\n", flag_W);
				

				ret = execvp(commands[0],commands);
				if(ret < 0)
				{
					execvp(error[0], error );
					_exit(-2);
					perror("command not found");				
					_exit(-2);
				}
			}
				
		}
		if(pid > 0)
			wait(0);	
		printf("%s@%s:%s$ ",user_name,host_name,print_wd);
		for(i = 0; i < MAX; i++)
			commands[i] = NULL;
	}
	
	return 0;
}
