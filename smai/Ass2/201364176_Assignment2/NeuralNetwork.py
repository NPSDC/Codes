import numpy as np
import pickle
from extract import *
import math
import copy 

def sigmoid(x):
	return np.array([float(1/(1 + math.exp(-x)))], dtype = 'float64')[0]

def sigmoid_derivate(x):
	return sigmoid(x)*math.exp(-x)/(1 + math.exp(-x))

def compute_net(x, w):
	x = np.array(x, dtype = 'float64')
	net = np.dot(w, x)
	return net

def compute_f(weights, inp):
	out = [1]
	for i in xrange(weights.shape[1]):
		out.append(sigmoid(compute_net(inp, weights[:,i])))
	return np.array(out)

def compute_delta_wkj(eta, j, y, w, expec_out_k, actual_out_k ):
	delta_k = (expec_out_k - actual_out_k)*sigmoid_derivate(compute_net(y, w))
	delta_w = eta*delta_k*float(y[j])
	return delta_w

def compute_delta_wji(eta, y, w_k, expec_outs, actual_outs, i, j, x_inp, w_yj ):	
	delta_j_1 = sigmoid_derivate(compute_net(x_inp, w_yj))
	delta_j_2 = 0
	for p in xrange(expec_outs.shape[0]):
		delta_j_2 += w_k[j,p] * compute_delta_wkj(eta, j, y, w_k[:,p], expec_outs[p][0], actual_outs[p+1])/eta/float(y[j])	
	delta_j = delta_j_1*delta_j_2
	#print float(x_inp[i])
	delta_w = eta*delta_j*float(x_inp[i])
	return delta_w

def set_expec_weight(expec_outs, expec_out):
	if(expec_out == '0'):
		expec_outs[0] = 1.
		expec_outs[1] = 0.
	else:
		expec_outs[0] = 0.
		expec_outs[1] = 1.
	return expec_outs

def set_data(data):
	data[1:] = data[:-1]
	data[0] = '1'
	data = np.array(data, dtype = 'float64')
	data = data/16
	data[0] = 1
	return data

def main():
	f = open('extracted_data', 'r')
	data = pickle.load(f) #putting the required set in data
	data = np.random.permutation(data)
	f.close()
	no_of_inputs = 64
	no_of_hidden = 2
	eta = 2
	no_of_output = 2
	weights_first = np.random.rand(no_of_inputs + 1, no_of_hidden)
	weights_second = np.random.rand(no_of_hidden + 1, no_of_output)

	expec_outs = np.zeros((2, 1))
	expec_out = data[0][-1]
	dat = set_data(data[0])
	
	inp_y = compute_f(weights_first, set_data(data[0]))
	#print inp_y

	for i in xrange(len(data)):
		#print weights_first, weights_second
		expec_out = data[i][-1]
		dat = set_data(data[i])

		inp_y = compute_f(weights_first, dat)
		actual_outs = compute_f(weights_second, inp_y)	
		expec_outs = set_expec_weight(expec_outs, expec_out)
		#J = np.square(np.transpose(actual_outs) - weight_out[1:])/2
		#print weight_out,expec_outs, inp_out, weights_second[:,1]
		for a in xrange(no_of_inputs + 1):
			for b in xrange(no_of_hidden):
				delta_w_ji = compute_delta_wji(eta, inp_y, weights_second, expec_outs, actual_outs, a, b, data[i], weights_first[:,b])
				#print delta_w_ji			
				weights_first[a,b] += delta_w_ji

		for a in xrange(no_of_hidden + 1):
			for b in xrange(no_of_output):
				delta_w_kj = compute_delta_wkj(eta, a, inp_y, weights_second[:,b], expec_outs[b][0], actual_outs[b+1])
				weights_second[a,b] += delta_w_kj
		


	f = open('test_data', 'r')			
	test_data = pickle.load(f)
	f.close()

	for i in xrange(len(test_data)):
		expec_out = test_data[i][-1]
		test = set_data(test_data[i])
		inp_y = compute_f(weights_first, test)
		actual_outs = compute_f(weights_second, inp_y)	
		print expec_out, actual_outs	

if __name__ == "__main__":
	main()
