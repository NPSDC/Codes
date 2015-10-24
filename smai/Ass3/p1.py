import csv
import numpy as np
from load import load

def get_unique_elements(data, col_names):
	'''return unique elements under each column'''
	unique_dict = {} #Corresponding to each column unique elements
	for i in col_names:
		unique_elements = np.unique(data[i]) #unique entries under a column and their prob
		count_dict = {}  #count of each unique element in a column
		for j in unique_elements:
			if j == '"unknown"':
				continue
			count = 0
			for ele in data[i]:
				if j == ele:
					count += 1
			count_dict[j] = float(count)/len(data)
		unique_dict[i] = count_dict
	return unique_dict

def compute_prob(test_row, unique_par, len_par, col_names):
	'''
	Compute probability of each test row
	'''
	prob = np.log(len_par)
	val_pos = 0
	for j in xrange(len(col_names)):
		val_data = test_row[j]
		if(val_data in unique_par[col_names[j]].keys()):
			prob += unique_par[col_names[j]][val_data]
	#print prob
	return prob

def test_main(test_row, unique_yes, unique_no, len_yes, len_no, col_names):
	'''
	Corresponding to each test row assign it a label
	'''
	prob_yes = compute_prob(test_row, unique_yes, len_yes, col_names)		
	prob_neg = compute_prob(test_row, unique_no, len_no, col_names)		
	#print prob_yes, prob_neg
	if(prob_yes > prob_neg):
		ans = 1
	elif(prob_yes == prob_neg):
		ans = np.random.randint(0, 2)
	else:
		ans = 0
	return ans

def test(test_data, unique_yes, unique_no, len_yes, len_no, col_names):
	'''Given a test sample and precomputed train sample return its accuracy'''
	tot_no_rows = len(test_data)
	no_of_cols = len(col_names)
	correct_predictions = 0
	for i in xrange(tot_no_rows):
		ret_val = test_main(test_data[i], unique_yes, unique_no, len_yes, len_no, col_names)
		act_val = test_data[i][no_of_cols]
		if(act_val == '"yes"' and ret_val == 1):
			correct_predictions += 1
		elif(act_val == '"no"' and ret_val == 0):
			correct_predictions += 1
	accuracy = float(correct_predictions)/tot_no_rows
	return accuracy

def do_computation(data, col_names, tot_no_rows):
	'''
	Input - Actual data, names of columns and total number of data points
	returns the accuracy
	Performs the actual computation(training and testing)
	'''
	indexes = np.random.permutation(tot_no_rows)[0:tot_no_rows/10]
	train_data = data[indexes]
	test_data = data[list(set(range(tot_no_rows)).difference(indexes))[0:tot_no_rows/10]]
	#test_data = load('bank-additional.csv', True)
	yes_out = train_data[train_data['y'] == '"yes"' ]
	no_out = train_data[train_data['y'] == '"no"' ]
	unique_yes = get_unique_elements(yes_out, col_names[0:-1]) #Look at function
	unique_no = get_unique_elements(no_out, col_names[0:-1])
	assert(len(train_data) == len(test_data))
	#print unique_yes
	#print unique_no
	for i in col_names[0:-1]:
		unique_yes[i] = {k1 : np.log(unique_yes[i][k1]) for k1 in unique_yes[i].keys()}
		unique_no[i] = {k1 : np.log(unique_no[i][k1]) for k1 in unique_no[i].keys()}
	return test(test_data, unique_yes, unique_no, len(yes_out), len(no_out), col_names[0:-1])
	

def main():
	data = load('bank-full.csv')
	tot_no_rows = len(data)	
	col_names = ["age", "job", "marital", "education", "default", "balance","housing" ,"loan", "contact", "day_of_week", "month",  "duration", "campaign", "pdays", "previous", "poutcome", "y"]
	accuracy = np.empty([10, ], dtype = float )	
	no_of_iteration = 1
	for i in xrange(no_of_iteration):
		accuracy[i] = do_computation(data, col_names, tot_no_rows)
	mean = np.mean(accuracy)
	st_dev = np.std(accuracy)
	print accuracy[0]
	#print mean, st_dev
	'''for key in unique_yes.keys():
		sum1 = 0
		for j in unique_yes[key].keys():
			sum1 += unique_yes[key][j]
		print sum1'''
	#print unique_yes['age']	


if __name__ == '__main__':
	main()