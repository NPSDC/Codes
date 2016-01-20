import numpy as np
import os
#from p3 import pca

def pca(data, k):
	cov_mat = np.cov(data.T)
	eig_val, eig_vec = np.linalg.eigh(cov_mat)
	k_indexes = eig_val.argsort()[-k:]
	K_eigen_vec = eig_vec[k_indexes]
	#transformed_data = np.dot(K_eigen_vec, data.T)
	#print K_eigen_vec.shape
	return K_eigen_vec

def extract(filename):
	i = 0
	with open(filename) as f:
		lis = f.readlines()
	no_of_data_points = len(lis)
	data = np.empty([no_of_data_points,10000])
	for i in xrange(no_of_data_points):
		data[i] = np.asarray(map(float, lis[i].split()))
	return data

def main():
	DATA_DIR = 'arcene'
	header = "arcene_.data"
	index = header.find('.')
	files = [header[:index] + x + header[index:] for x in ["train"]]
	no_of_dims = [10, 100, 1000]
	for f in files:
		data = extract(os.path.join(DATA_DIR ,f))
		for k in no_of_dims:
			weight_vec = pca(data, k)
			assert(weight_vec.shape[1] == 10000 and weight_vec.shape[0] == k)
			np.savetxt(f+'_'+str(k), weight_vec)


if __name__ == '__main__' :
	main()