import numpy as np
import sklearn.svm as svm
import os
from gen_files import extract
from p2a import *

def classify(data_train, labels_train, data_valid, labels_valid):
	classifier = svm.SVC()
	classifier.fit(data_train, labels_train)
	predicted_results = classifier.predict(data_valid)
	#print predicted_results
	#print (predicted_results == labels_valid).sum()


def main():
	Data_Dir = 'arcene'
	data_train = extract(os.path.join(Data_Dir, 'arcene_train.data'))
	data_train = data_train.T
	labels_train =  gen_labels(os.path.join(Data_Dir, 'arcene_train.labels'))
	data_valid = extract(os.path.join(Data_Dir, 'arcene_valid.data'))
	data_valid = data_valid.T
	data_train, mean = centre(data_train)
	data_valid, mean = centre(data_valid, mean)
	labels_valid =  gen_labels(os.path.join(Data_Dir, 'arcene_valid.labels'))


	
	sig = get_sigma(data_train, labels_train)
	eig_val1, eig_vec1 = gram(np.dot, data_train)
	eig_val2, eig_vec2 = gram(rbf, data_train, sig)
	
	
	alpha_lin = get_lda(data_train, labels_train, np.dot)
	alpha_rbf = get_lda(data_train, labels_train, rbf, sig)

	dim = [10, 100]
	red_points_pca_lin_train = [kernel_pca(np.dot, k, eig_vec1, eig_val1, data_train, data_train ) for k in dim]
	red_points_pca_rbf_train = [kernel_pca(rbf, k, eig_vec1, eig_val1, data_train, data_train, sig ) for k in dim]
	red_points_pca_lin_valid = [kernel_pca(np.dot, k, eig_vec1, eig_val1, data_valid, data_train ) for k in dim]
	red_points_pca_rbf_valid = [kernel_pca(rbf, k, eig_vec1, eig_val1, data_valid, data_train, sig ) for k in dim]

	red_points_lda_rbf_train = lda(alpha_rbf, data_train, data_train, np.dot)
	red_points_lda_rbf = lda(alpha_rbf, data_valid, data_train, rbf, sig )
	red_points_lda_lin = lda(alpha_lin, data_valid, data_train, np.dot)

	#print red_points_pca_lin_valid 

	
	classify(red_points_pca_rbf_train[0], labels_train, red_points_pca_rbf_valid[0], labels_valid)

if __name__ == '__main__' :
	main()