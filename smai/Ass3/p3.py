import numpy as np
import os
import pickle
from scipy.stats import multivariate_normal as mv

def extract(filename):
	data = np.empty([100,10000])
	i = 0
	with open(filename) as f:
		lis = f.readlines()
	for i in xrange(len(lis)):
		data[i] = np.asarray(map(float, lis[i].split()))

	return data

def pca(data, k):
	cov_mat = np.cov(data.T)
	eig_val, eig_vec = np.linalg.eigh(cov_mat)
	k_indexes = eig_val.argsort()[-k:]
	K_eigen_vec = eig_vec[k_indexes]
	transformed_data = np.dot(K_eigen_vec, data.T)
	return transformed_data

def get_count(element, array):
	count = 0
	for i in array:
		if i == element:
			count += 1
	return count

def gaussian_multivariate(mu, cov):
    return mv(mean = mu, cov = cov)

def assign_label(prob_1, prob_2, label_array, i, classes):
	if(prob_1 > prob_2):
		label_array[i] = classes[0]
	else:
		label_array[i] = classes[1]

def gaussian_classify(data, prior , means, cov, classes ):
	ass_labels = np.empty([100,], dtype = 'int')
	mv_1 = gaussian_multivariate(means[0], cov[0])
	mv_2 = gaussian_multivariate(means[1], cov[1])
	assert(data.shape[0] == 10 and data.shape[1] == 100)
	for i in xrange(data.shape[1]):
		class1_prob = prior[0]*mv_1.pdf(data[: , i])
		class2_prob = prior[1]*mv_2.pdf(data[: , i])
		assign_label(class1_prob, class2_prob, ass_labels, i, classes)
	return ass_labels

def train_data(train_file_labels, data):
	train_labels = np.genfromtxt(
            train_file_labels,
            skip_header=0,
            dtype ='int')
	classes = np.unique(train_labels)
	class_1_data = data.T[train_labels == classes[0]]
	class_2_data = data.T[train_labels == classes[1]]
	class_mean = np.asarray([np.mean(np.asarray(x) , axis = 0) for x in [class_1_data, class_2_data]])
	class_cov = np.asarray(map(np.cov, [class_1_data.T, class_2_data.T]))
	prob_counts = np.empty([2,1])
	prob_counts[0] = float(class_1_data.shape[0])/train_labels.size
	prob_counts[1] = float(class_2_data.shape[0])/train_labels.size
	return prob_counts, class_mean, class_cov, classes, train_labels

def accuracy(actual, obtained):
	count = 0
	for i in xrange(actual.size):
		#print actual[i] == obtained[i]
		if(actual[i] == obtained[i]):
			count += 1
	return float(count)/actual.size

def main():
	k = 10
	DATA_DIR = 'arcene'
	filename = os.path.join(DATA_DIR, 'arcene_train.data')	
	file_labels = os.path.join(DATA_DIR, 'arcene_train.labels')	
	data = extract(filename)	
	#transformed_pca_data =  pca(data, k) # k * N matrix
	#pickle.dump(transformed_pca_data, open("pca_data_pickle", "wb"))
	#transformed_pca_data = pickle.load(open("pca_data_pickle", "rb"))
	#np.savetxt("pca_data", transformed_pca_data)
	transformed_pca_data = np.loadtxt("pca_data")
#	print a
#	print "##################################"
	prior, means, cov, classes, train_labels = train_data(file_labels, transformed_pca_data)
	labels = gaussian_classify(transformed_pca_data, prior, means, cov, classes)
	print accuracy(train_labels, labels)
	
if __name__ == '__main__' :
	main()