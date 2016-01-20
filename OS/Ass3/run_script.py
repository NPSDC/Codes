import os

def main():
	while(1):
		command = "perf stat -o out -p 25744 sleep 10 "
		os.system(command)
		f = open('out', 'r')
		output = f.readlines()
		f.close()
		f = open('cpu_usage', 'a')
		f.write(output[5].split()[0])
		f.write('\n')
		f.close()
		f = open('context_switch', 'a')
		f.write(output[6].split()[0])
		f.write('\n')	
		f.close()

if __name__ == '__main__':

	main()