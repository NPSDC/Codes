import csv
import numpy as np
from load import load

def get_unique_elements(data, col_names):
	return {key: np.unique(data[key]) for key in col_names}

def ret_count(unique_elements):	
	unqiue_counts = {}
	for keys in unique_elements.keys():
		unique_rows = unique_elements[keys][:]
		unique_elements[keys] = {}
		for row in unique_rows:
			if row in 


def main():
	data = load()
	tot_no_rows = len(data)
	indexes = np.random.permutation(tot_no_rows)[np.random.permutation(tot_no_rows/2)]
	train_data = data[indexes]
	test_data = data[list(set(range(tot_no_rows)).difference(indexes))]
	col_names = ["age", "job", "marital", "education", "default", "housing", "loan", "contact", "month", "day_of_week", "duration", "campaign", "pdays", "previous", "poutcome", "empvarrate", "conspriceidx", "consconfidx", "euribor3m", "nremployed" , "y"]
	unique_elements = get_unique_elements(train_data, col_names)
	print unique_elements
	
		
		


if __name__ == '__main__':
	main()