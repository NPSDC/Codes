import numpy as np
import pickle
import re

def extract(file):
	'''Extracting the  required pattern from file'''
	content = []	
	f = open(file)
	for line in f:
		if(line[-2] == '0' or line[-2] == '7'):
			strng = re.split(',', line)
			strng[-1] = strng[-1][0]
			content.append(strng)
	f.close()
	return content
	
def main():
	file_store = 'extracted_data'
	file_test = 'test_data'
	content = extract('optdigits.tra')
	test_data = extract('optdigits.tes')
	f = open(file_store, 'wb')
	pickle.dump(content, f)
	f.close()
	f = open(file_test, 'wb')
	pickle.dump(test_data, f)
	f.close()
	

if (__name__ == '__main__'):
	main()
