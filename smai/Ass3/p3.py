import numpy as np
import os
from scipy.stats import multivariate_normal as mv
from gen_files import extract

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
	no_of_data_points = data.shape[1]
	ass_labels = np.empty([no_of_data_points,], dtype = 'int')
	mv_1 = gaussian_multivariate(means[0], cov[0])
	mv_2 = gaussian_multivariate(means[1], cov[1])
	for i in xrange(data.shape[1]):
		class1_prob = prior[0]*mv_1.pdf(data[: , i])
		class2_prob = prior[1]*mv_2.pdf(data[: , i])
		assign_label(class1_prob, class2_prob, ass_labels, i, classes)
	return ass_labels

def train_data(train_labels, data):
	classes = np.unique(train_labels)
	prob_counts = np.empty((data.shape[0], classes.size))
	class_mean = np.empty((data.shape[0], classes.size, data.shape[1]))
	class_cov = np.empty((data.shape[0], classes.size, data.shape[1], data.shape[1]))
	for i in xrange(data.shape[0]):
		class_1_data = data[i].T[train_labels == classes[0]]
		class_2_data = data[i].T[train_labels == classes[1]]
		class_mean[i] = np.asarray([np.mean(np.asarray(x) , axis = 0) for x in [class_1_data, class_2_data]])
		class_cov[i] = np.asarray(map(np.cov, [class_1_data.T, class_2_data.T]))
		prob_counts[i][0] = float(class_1_data.shape[0])/train_labels.size
		prob_counts[i][1] = float(class_2_data.shape[0])/train_labels.size
	return prob_counts, class_mean, class_cov, classes

def accuracy(actual, obtained):
	count = 0
	for i in xrange(actual.size):
		if(actual[i] == obtained[i]):
			count += 1
	return float(count)/actual.size

def gen_labels(filename):
	labels = np.genfromtxt(
            filename,
            skip_header=0,
            dtype ='int')
	return labels

def main():
	k = 10
	DATA_DIR = 'arcene'	
	train_file_labels = os.path.join(DATA_DIR, 'arcene_train.labels')	
	#data = extract(filename)	
	header = "arcene_.data10"
	index = header.find('.')
	train_labels = gen_labels(train_file_labels)
	actual_files = ["test", "train", "valid"]

	files = [header[:index] + x + header[index:] + j for x in actual_files for j in ['', '0', '00']]

	'''for i in files:
		data = np.loadtxt(i)
		sub_index = i.find('10')
		#assert(data.shape[0] == int(i[sub_index :]) and data.shape[1] == extract(os.path.join(DATA_DIR, i[:sub_index])).shape[0])'''
	transformed_pca_train_data = np.asarray([np.loadtxt(files[3]), np.loadtxt(files[4])]) 
	#print transformed_pca_data.shape
#	print a
#	print "##################################"
	print transformed_pca_train_data[1].shape
	assert(transformed_pca_train_data.shape[1] == 100)
	prior, means, cov, classes = train_data(train_labels, transformed_pca_train_data)
	print means
	#labels = gaussian_classify(np.loadtxt(files[3]), prior, means, cov, classes)
	#print accuracy(train_labels, labels)
	
if __name__ == '__main__' :
	main()