from gen_files import extract
import numpy as np
import os

def gen_labels(filename):
	labels = np.genfromtxt(
            filename,
            skip_header=0,
            dtype ='int')
	return labels

def lda(data):
	data = data.T
	train_file_labels = os.path.join('arcene', 'arcene_train.labels')
	train_labels = gen_labels(train_file_labels)
	classes = np.unique(train_labels)
	indexes_1 = train_labels == classes[0]
	indexes_2 = train_labels == classes[1]
	
	#overall_mean = np.mean(data, axis = 1)
	class_1_data = data.T[indexes_1].T
	class_2_data = data.T[indexes_2].T
	class_mean = np.asarray([np.mean(np.asarray(x) , axis = 1) for x in [class_1_data, class_2_data]])
	#class_mean[0] = class_mean[0].reshape((class_mean[0].shape[0], 1))
	scat_class_1 = class_1_data - class_mean[0].reshape((class_mean[0].shape[0], 1))
	scat_class_2 = class_2_data - class_mean[1].reshape((class_mean[1].shape[0], 1))
	scatter_mat = np.matmul(scat_class_1, scat_class_1.T) + np.matmul(scat_class_2, scat_class_2.T)
	transform_mat = np.matmul(np.linalg.inv(scatter_mat), class_mean[0] - class_mean[1])
	assert(transform_mat.shape[0] == 10000 and transform_mat.shape[1] == 1)
	#print (class_mean - overall_mean).shape

def main():
	DATA_DIR = 'arcene'
	header = "arcene_.data"
	index = header.find('.')
	files = [header[:index] + x + header[index:] for x in ["train"]]
	data = []
	for f in files:
		data = extract(os.path.join(DATA_DIR ,f))
		lda(data)

if __name__ == '__main__':
	main()