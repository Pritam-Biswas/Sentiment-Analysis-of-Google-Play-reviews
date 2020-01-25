from __future__ import print_function
import numpy as np
import theano
import theano.tensor as T
import time
import Tweet
import json
import lasagne
from gensim.models import word2vec
import imdb
import gensim
MAX_SEQ = 100 # maximum length of a sequence
vocabSize=0
my_embed=None
old_W=None


def build_model(V, # input vocab mapping
	num_classes, # number classes to predict
	vmap, # vocab map
	K=128, # dimensionality of embeddings
	num_hidden=32, # number of hidden_units
	batchsize=None, # size of each batch (None for variable size)
	input_var=None, # theano variable for input
	mask_var=None, # theano variable for input mask
	grad_clip=5, # gradients above this will be clipped
	max_seq_len=MAX_SEQ, # maximum lenght of a sequence
	ini_word2vec=False, # whether to initialize with word2vec
	word2vec_file='glove.twitter.27B.50d.txt',):
	
	global my_embed
	global old_W
	print (" vocabSize is :"+str(V))

	with open('embedding.json') as emoji_unicode:
		data = json.load(emoji_unicode)
	
	if ini_word2vec:
		t_vocab=data['t_vocab']
		t_map=data['t_map']
		
		print ("Loaded Word2Vec model")
		K=50 ### for 50D
		W = np.zeros((V, K), dtype=np.float32)
		no_vectors = 0
		word_count=0
		word_match=0
		
		for w in vmap:
			if word_count%1000 == 0:
				print ("Words in vocab searched ::"+str(word_count)+" ; word matches ::"+str(word_match))
				word_count+=1
			if w in t_vocab:
				W[vmap[w]] = t_map[w]
				word_match+=1
			else:
				W[vmap[w]] = np.random.normal(scale=0.01, size=K)
				no_vectors += 1
			print (" Initialized with word2vec. Couldn't find", no_vectors, "words!")
	else:
		W = lasagne.init.Normal()
	old_W=W

	l_in = lasagne.layers.InputLayer((batchsize, max_seq_len),
	input_var=input_var)
	l_mask = lasagne.layers.InputLayer((batchsize, max_seq_len),
	input_var=mask_var)
	l_emb = lasagne.layers.EmbeddingLayer(l_in, input_size=V,
	output_size=K, W=W)

	print (lasagne.layers.get_output_shape(l_emb,
	{l_in: (200, 100),
	l_mask: (200, 100)}))

	network = lasagne.layers.LSTMLayer(
	l_emb, num_units=num_hidden, grad_clipping=grad_clip,
	nonlinearity=lasagne.nonlinearities.tanh, mask_input=l_mask,
	# only_return_final=True
	)

	my_embed=network
	print (lasagne.layers.get_output_shape(network,
	{l_in: (200, 100),
	l_mask: (200, 100)}))
	# add droput
	network = lasagne.layers.DropoutLayer(network, p=0.5)
	
	network = lasagne.layers.DenseLayer(
	network, num_units=num_classes,
	nonlinearity=lasagne.nonlinearities.softmax
	)
	
	print (lasagne.layers.get_output_shape(network,
	Page 54 of 60
	{l_in: (200, 100),
	l_mask: (200, 100)}))

	return network

def preprocess(tweets, vmap=None, stopf='stopwords.txt'):

	with open('X_Y_lstm_imdb.json') as emoji_unicode:
		data = json.load(emoji_unicode)
	
	corpora_x=data['corpora_X']
	corpora_y=data['corpora_Y']
	
	if vmap is None:
		with open(stopf, mode='r') as f:
			stopwords = map(lambda x: x.strip(), f.readlines())
		V = 0
		vmap = {}
		for review in corpora_x:
			for w in review.strip().split():
				w = w.lower()
				if w not in vmap and w not in stopwords:
					vmap[w] = V
					V += 1

	X = []
	y = []

	label_map = {'negative': 0,
	'neutral': 1,
	'positive': 2}

	for i in range(0,len(corpora_x)):
		review=corpora_X[i]
		out = []
		for w in review.strip().split():
			w = w.lower()
			if w.strip() in vmap:
				out.append(vmap[w.strip()])
		if out:
			X.append(out)
			y.append(corpora_Y[i])
	return X, y, vmap

def pad_mask(X, max_seq_length=MAX_SEQ):

	N = len(X)
	X_out = np.zeros((N, max_seq_length, 2), dtype=np.int32)
	for i, x in enumerate(X):
		n = len(x)
		if n < max_seq_length:
			X_out[i, :n, 0] = x
			X_out[i, :n, 1] = 1
		else:
			X_out[i, :, 0] = x[:max_seq_length]
			X_out[i, :, 1] = 1
	return X_out

def load_dataset(n_words=10000, maxlen=140):
	global vocabSize

	with open('X_Y_lstm_imdb.json') as emoji_unicode:
		data = json.load(emoji_unicode)
	
	vocabSize=21001
	
	X_train=data['trainX']
	y_train=data['trainY']
	X_test=data['testX']
	y_test=data['testY']
	X_val=data['valX']
	y_val=data['valY']
	# X_train, y_train = train
	# X_val, y_val = val
	# X_test, y_test = test
	X_train, X_val, X_test = map(pad_mask, [X_train, X_val, X_test])
	y_train, y_val, y_test = map(np.asarray, [y_train, y_val, y_test])
	return X_train, y_train, X_val, y_val, X_test, y_test


def iterate_minibatches(inputs, targets, batchsize, shuffle=False):

	assert inputs.shape[0] == targets.size
	if shuffle:
		indices = np.arange(inputs.shape[0])
		np.random.shuffle(indices)
	for start_idx in range(0, inputs.shape[0] - batchsize + 1, batchsize):
		if shuffle:
			excerpt = indices[start_idx:start_idx + batchsize]
		else:
			excerpt = slice(start_idx, start_idx + batchsize)
		yield inputs[excerpt], targets[excerpt]


def learn_model(max_norm=5, num_epochs=5, batchsize=64,
 learn_rate=0.1, V=21001):
	global my_embed
	global old_W
	print ("vocabSize in learn is :"+str(V))
	print ("Loading Dataset")
	
	X_train, y_train, X_val, y_val, X_test, y_test = load_dataset(n_words=V)
	n_classes = len(set(y_train))
	print ("Classes", set(y_train))
	print ("Vocab size:", V)
	print ("Number of classes", n_classes)
	# Initialize theano variables for input and output
	X = T.imatrix('X')
	M = T.matrix('M')
	y = T.ivector('y')
	# Construct network
	
	print ("Building Model")
	with open('X_Y_lstm_imdb.json') as emoji_unicode:
		data = json.load(emoji_unicode)
	vmap=data['vmap']
	
	network = build_model(V, n_classes, vmap,input_var=X, mask_var=M,ini_word2vec=False)
	
	# Get network output
	output = lasagne.layers.get_output(network)
	
	# Define objective function (cost) to minimize, mean crossentropy error
	cost = lasagne.objectives.categorical_crossentropy(output, y).mean()
	
	# Compute gradient updates
	params = lasagne.layers.get_all_params(network)
	param_count=lasagne.layers.count_params(network)
	print("total no params :"+str(param_count))
	
	e_param=lasagne.layers.get_all_param_values(my_embed)

	e_param=e_param[0]
	print(e_param)
	print("Dimesions are :"+str(len(e_param))+" , "+str(len(e_param[0])))
	
	grad_updates = lasagne.updates.adadelta(cost, params, learn_rate)
	# Compile train objective
	print ("Compiling training functions")
	train = theano.function([X, M, y], cost,
	updates=grad_updates,
	allow_input_downcast=True)

	# need to switch off droput while testing
	test_output = lasagne.layers.get_output(network, deterministic=True)
	val_cost = lasagne.objectives.categorical_crossentropy(
	test_output, y).mean()
	
	preds = T.argmax(test_output, axis=1)
	val_acc = T.mean(T.eq(preds, y),
	dtype=theano.config.floatX)
	val_fn = theano.function([X, M, y], [val_cost, val_acc, preds],
	allow_input_downcast=True)
	
	print ("Starting Training")
	
	begin_time = time.time()
	for epoch in xrange(num_epochs):
		
		print ("Epoch no ::"+str(epoch+1))
		train_err = 0.
		train_batches = 0
		start_time = time.time()
		train_count=0
		
		for batch in iterate_minibatches(X_train, y_train,
		batchsize, shuffle=True):
			x_mini, y_mini = batch
			train_err += train(x_mini[:, :, 0], x_mini[:, :, 1], y_mini)
			train_batches += 1
			train_count+=1
			print('Training samples :'+str(train_count)+' / '+str(len(X_train))+' completed ...', end='\r')
		
		print ("Training error done ...")
		
		val_err = [0.,0.]
		val_batches = 0
		
		for batch in iterate_minibatches(X_val, y_val,
		batchsize, shuffle=True):
		
			x_val_mini, y_val_mini = batch
			v_err, v_acc, _ = val_fn(x_val_mini[:, :, 0], x_val_mini[:, :, 1], y_val_mini)
			val_err[0] += v_err
			val_err[1] += v_acc
			val_batches += 1


		print ("Validation error done ...")
		# test_err = val_fn(X_test[:, :, 0], X_test[:, :, 1], y_test)
		print("Epoch {} of {} took {:.3f}s".format(
		epoch + 1, num_epochs, time.time() - start_time))
		print(" training loss:\t\t{:.6f}".format(train_err / train_batches))
		print(" validation loss:\t\t{:.6f}".format(val_err[0] * 1.0/ val_batches))
		print(" validation accuracy:\t\t{:.2f} %".format(
		val_err[1] * 100. / val_batches))
		
	test_err = [0., 0.]
	test_batches = 0
	
	for batch in iterate_minibatches(X_test, y_test,
	batchsize, shuffle=True):
	
		x_val_mini, y_val_mini = batch
		v_err, v_acc, _ = val_fn(x_val_mini[:, :, 0], x_val_mini[:, :, 1], y_val_mini)
		test_err[0] += v_err
		test_err[1] += v_acc
		test_batches += 1

	print("Test accuracy:\t\t{:.2f} %".format(
	test_err[1] * 100. / test_batches))
	print ("Training took {:.3f}s".format(time.time() - begin_time))

	return network

if __name__ == "__main__":
	learn_model(num_epochs=10, max_norm=5, batchsize=64, learn_rate=0.5)
