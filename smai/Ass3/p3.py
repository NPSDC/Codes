import numpy as np
import os

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
	eig_val, eig_vec = np.linalg.eig(cov_mat)
	k_indexes = eig_val.argsort()[-k:]
	K_eigen_vec = eig_vec[:k_indexes]
	transformed = np.dot(K_eigen_vec, data.T)

def get_count(element, array):
	count = 0
	for i in array:
		if i == element:
			count += 1
	return count

def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

def gaussian_classify(data, prior , means, sigs, classes ):
	ass_labels = np.empty([100,1])
	for i in xrange(data.shape[1]):
		class1_prob = prior[0]*gaussian(data[:i], means[0], sigs[0] )
		class2_prob = prior[1]*gaussian(data[:i], means[1], sigs[1] )
		if(class1_prob > class2_prob):
			ass_labels[i] = classes[0]
		else:
			ass_labels[i] = classes[1]

def train_data(train_file, data):
	train_labels = np.genfromtxt(
            train_file,
            skip_header=0,
            dtype ='i3')
	classes = np.unique(train_labels)
	class_1_data = data[train_labels == classes[0]]
	class_2_data = data[train_labels == classes[1]]
	class_1_mean = np.mean(class_1_data, axis = 0)
	class_2_mean = np.mean(class_2_data, axis = 0)
	class_1_sig = np.std(class_1_data, axis = 0)
	class_2_sig = np.std(class_2_data, axis = 0)
	prob_counts = np.empty([2,1])
	prob_counts[0] = float(class_1_data.shape(1))/train_labels.size
	prob_counts[1] = (train_labels.size - prob_counts[0] )/train_labels.size
	return prob_counts, np.array([class_1_mean, class_2_mean]), np.array([class_1_sig, class_2_sig]), classes

def main():
	k = 10
	DATA_DIR = 'arcrene'
	filename = os.path.join('arcrene', 'arcene_train.data')	
	file_labels = os.path.join('arcrene', 'arcene_train.labels')	
	data = extract(filename)	
	transformed_pca =  pca(data, k) # k * N matrix
	prior, means, sigs, classes = train_data(file_labels)
	labels = gaussian_classify(data, prior, means, sigs, classes)
	
if __name__ == '__main__' :
	main()