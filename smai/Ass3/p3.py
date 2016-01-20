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

def gaussian(x, mu, sig):
    prob = np.log(np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.))))
    #print prob,mu,sig
    return prob

def get_count(element, array):
	count = 0
	for i in array:
		if i == element:
			count += 1
	return count

def gaussian_multivariate(mu, cov):
    return mv(mean = mu, cov = cov)

def assign_label(prob_1, prob_2, label_array, i, classes):
	#print prob_1,prob_2
	if(prob_1 > prob_2):
		label_array[i] = classes[0]
	else:
		label_array[i] = classes[1]

def naive_gaussian(test_data, prior, means, cov, classes):

	assert(test_data.shape[0] == means.shape[1])
	assert(means.shape[0] == cov.shape[0] == classes.shape[0])
	assert(means.shape[1] == cov.shape[1] == cov.shape[2])
	#print np.log(prior)
	no_of_data_points = test_data.shape[1]
	ass_labels = np.empty([no_of_data_points,], dtype = 'int')

	prob_1 = np.log(prior[0])
	prob_2 = np.log(prior[1])

	for i in xrange(no_of_data_points):
		for j in xrange(means.shape[1]):
			#print i,j
			prob_1 += gaussian(test_data[j][i], means[0][j], cov[0][j][j])
			prob_2 += gaussian(test_data[j][i], means[1][j], cov[1][j][j])
		assign_label(prob_1, prob_2, ass_labels, i, classes)
		#print prob_1, prob_2
		prob_1 = np.log(prior[0])
		prob_2 = np.log(prior[1])

	return ass_labels

def gaussian_classify(data, prior , means, cov, classes ):
	assert(data.shape[0] == means.shape[1])
	assert(means.shape[0] == cov.shape[0] == classes.shape[0])
	assert(means.shape[1] == cov.shape[1])
	no_of_data_points = data.shape[1]
	ass_labels = np.empty([no_of_data_points,], dtype = 'int')
	#print np.linalg.det(cov[1])
	mv_1 = gaussian_multivariate(means[0], cov[0])
	mv_2 = gaussian_multivariate(means[1], cov[1])
	for i in xrange(data.shape[1]):
		class1_prob = prior[0]*mv_1.pdf(data[: , i])
		class2_prob = prior[1]*mv_2.pdf(data[: , i])
		assign_label(class1_prob, class2_prob, ass_labels, i, classes)
	return ass_labels


def train_data(train_labels, data):
	classes = np.unique(train_labels)
	indexes_1 = train_labels == classes[0]
	indexes_2 = train_labels == classes[1]
	prob_counts = np.empty(classes.size)
	prob_counts[0] = float(indexes_1.sum())/train_labels.size
	prob_counts[1] = float(indexes_2.sum())/train_labels.size
	class_mean = []
	class_cov = []

	for i in xrange(data.shape[0]):
		class_1_data = data[i].T[indexes_1]
		class_2_data = data[i].T[indexes_2]
		class_mean.append(np.asarray([np.mean(np.asarray(x) , axis = 0) for x in [class_1_data, class_2_data]]))
		class_cov.append(np.asarray(map(np.cov, [class_1_data.T, class_2_data.T])))
		
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
	header = "arcene_train.data_10"
	header2 = "arcene_.data"
	index = header2.find('.')
	train_labels = gen_labels(train_file_labels)
	actual_files = ["test", "train", "valid"]
	transformed_pca_data = []
	data = []

	data_files = [header2[:index] + x + header2[index:] for x in actual_files]
	weight_files = [header + j for j in ['', '0', '00' ]]
	weights = np.asarray(map(np.loadtxt, weight_files))
	assert(weights[0].shape[1] == 10000 and weights[0].shape[0] == 10)
	assert(weights[1].shape[1] == 10000 and weights[1].shape[0] == 100)
	assert(weights[2].shape[1] == 10000 and weights[2].shape[0] == 1000)
	
	for file in data_files:
		data.append(extract(os.path.join(DATA_DIR,file)))

	for i in xrange(len(data)):
		for j in xrange(len(weights)):
			transformed_pca_data.append(np.dot(weights[j], data[i].T))

	#transformed_pca_data = np.asarray(map(np.loadtxt, files))
	transformed_pca_train_data = np.asarray([transformed_pca_data[3], transformed_pca_data[4], transformed_pca_data[5]]) 
	
	assert(len(transformed_pca_data) == 9)
	for i in xrange(9):
		if(i/3 == 0):
			assert(transformed_pca_data[i].shape[1] == 700)
		else:
			assert(transformed_pca_data[i].shape[1] == 100)
		if(i%3 == 0):
			assert(transformed_pca_data[i].shape[0] == 10)
		elif(i%3 == 1):
			assert(transformed_pca_data[i].shape[0] == 100)
		else:
			assert(transformed_pca_data[i].shape[0] == 1000)
	
	prior, means, cov, classes = train_data(train_labels, transformed_pca_train_data)
	assert(len(means) == len(transformed_pca_train_data))
	assert(len(cov) == len(transformed_pca_train_data))

	#labels = gaussian_classify(transformed_pca_train_data[1], prior, means[1], cov[1], classes)
	labels = naive_gaussian(transformed_pca_data[7], prior, means[1], cov[1], classes)
	#print labels
	#print accuracy(train_labels, labels)
	
if __name__ == '__main__' :
	main()