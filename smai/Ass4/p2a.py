from gen_files import extract
import numpy as np
import os
from functools import partial

def gram(func, data, param = None):
	no_of_data_points = data.shape[1]
	gram_mat = np.zeros((no_of_data_points, no_of_data_points))
	for i in xrange(no_of_data_points):
		for j in xrange(no_of_data_points):
			gram_mat[i][j] = f(func, data.T[i], data.T[j], param)
	#print gram_mat		
	eig_val, eig_vec = np.linalg.eigh(gram_mat)
	return (eig_val, eig_vec)

def form_kern_mat(func, data_test, data_train, param = None):
	ker_mat = np.empty((data_test.shape[1], data_train.shape[1]))
	for i in xrange(data_test.shape[1]):
		for j in xrange(data_train.shape[1]):
			ker_mat[i][j] = f(func, data_test.T[i], data_train.T[j], param)
	return ker_mat


def kernel_pca(func, k, eig_vec, eig_val, data, data_train, param = None):
	k_indexes = eig_val.argsort()[-k:]
	K_eigen_vec = eig_vec[k_indexes]
	new_mat = form_kern_mat(func, data, data_train, param)	
	reduced_points = np.dot(new_mat, K_eigen_vec.T)
	assert(reduced_points.shape[0] == data.shape[1] and reduced_points.shape[1] == k) 
	return reduced_points

def get_sigma(data, labels):
	indexes_1 = labels == 1
	indexes_2 = labels == -1
	indexes = np.array([indexes_1, indexes_2])
	W = 0
	B = 0
	assert(data.shape[0] == 10000)
	for i in xrange(2):
		dat = data.T[indexes[i]]
		assert(dat.shape[0] == indexes[i].sum())
		for j in xrange(indexes[i].sum()):
			for k in range(j + 1, indexes[i].sum()):
				W += np.dot((dat[j]	- dat[k]), (dat[j] - dat[k]).T)

	for i in xrange(2):
		data1 = data.T[indexes[i]]
		assert(data1.shape[0] == indexes[i].sum())
		for j in xrange(2):
			data2 = data.T[indexes[j]]
			assert(data2.shape[0] == indexes[j].sum())
			if(i != j and j > i):
				for k in xrange(indexes[i].sum()):
					#print indexes[1]
					for l in xrange(indexes[j].sum()):
						#print np.dot((data1[k] - data2[l]), (data1[k] - data2[l]).T) 
						B += np.dot((data1[k] - data2[l]), (data1[k] - data2[l]).T)

	indexes = np.array([indexes_1.sum(), indexes_2.sum()])
	W /= np.square(indexes).sum()
	B /= np.prod(indexes)
	sig = (B - W)/(4*np.log(B/W))
	return sig

def rbf(x1, x2, sig):
	sig = 311109737.452
	return np.exp(-np.dot((x1 -x2), (x1 - x2))/(2*sig))

def f(func, x1, x2, param = None):
	return func(x1, x2, param)

def gen_labels(filename):
	labels = np.genfromtxt(
            filename,
            skip_header=0,
            dtype ='int')
	return labels

def get_lda(data, labels, func, param = None):
	indexes_1 = labels == 1
	indexes_2 = labels == -1
	indexes = np.array([indexes_1, indexes_2])
	no_of_data_points = data.shape[1]
	data = data.T
	M = []
	K = []
	for i in xrange(indexes.shape[0]):
		M.append(np.empty((no_of_data_points, 1)))
		for j in xrange(no_of_data_points):
			dat = data[indexes[i]]
			assert(dat.shape[0] == indexes[i].sum())
			for k in xrange(dat.shape[0]):
				M[i][j][0] += func(data[j], data[k], param)
			M[i][j][0] /= dat.shape[0]
			assert(M[i].shape[0] == no_of_data_points)

	for i in xrange(indexes.shape[0]):
		K.append(np.empty((no_of_data_points, indexes[i].sum())))
		dat = data[indexes[i]]
		for j in xrange(no_of_data_points):
			#mapfunc = partial(f, func = func, x1 = data[j], param = param)
			for k in xrange(dat.shape[0]):
				K[i][j][k] = f(func, data[j], dat[k], param)

			#val = map(mapfunc, dat)	
	N = np.zeros((no_of_data_points,no_of_data_points))
	for i in xrange(indexes.shape[0]):
		N += np.matrix(K[i])*(np.identity(indexes[i].sum()) - np.ones(indexes[i].sum()))*np.matrix(K[i].T)	

	alpha = np.matrix(np.linalg.inv(N))*np.matrix(M[1] - M[0])
	return alpha

def lda(alpha, data_test, data_train, func, param = None):
	kern_mat = form_kern_mat(func, data_test, data_train, param)
	return kern_mat*np.matrix(alpha)

def centre(data, mean = None):
	no_of_data_points = data.shape[1]
	if mean is None:
		mean = np.mean(data, axis = 1)
		mean = mean.reshape((10000, 1))
	assert(mean.shape[0] == 10000)
	
	data = data - mean
	assert(data.shape[0] == 10000)
	return data, mean

def main():
	DATA_DIR = 'arcene'
	data = extract(os.path.join(DATA_DIR,'arcene_train.data'))
	data = data.T
	data, mean = centre(data)
	
	data_valid = extract(os.path.join(DATA_DIR,'arcene_train.data'))
	data_valid,mean = centre(data_valid.T, mean)
	
	labels = gen_labels(os.path.join(DATA_DIR, 'arcene_train.labels'))

	sig = get_sigma(data, labels)

	eig_val, eig_vec = gram(rbf, data, sig)
	alpha = get_lda(data, labels, rbf, sig)
	reduced_points = kernel_pca(rbf, 10, eig_vec, eig_val, data, data, sig)
	red_points = lda(alpha, data, data, rbf, sig)
	
	#print reduced_points

if __name__ == '__main__' :
	main()