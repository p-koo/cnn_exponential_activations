from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os, sys
import numpy as np
import helper
import tensorflow as tf
from deepomics import neuralnetwork as nn
from deepomics import utils, metrics

#------------------------------------------------------------------------------------------------

all_models = ['cnn_2', 'cnn_50', 'distnet']
activations = ['exp', 'relu']
num_trials = 5

# save path
results_path = utils.make_directory('../results', 'synthetic')
params_path = utils.make_directory(results_path, 'model_params')
save_path = os.path.join(results_path, 'performance_summary.tsv')

# load dataset
data_path = '../data/synthetic_dataset.h5'
train, valid, test = helper.load_synthetic_dataset(data_path)

# get data shapes
input_shape = list(train['inputs'].shape)
input_shape[0] = None
output_shape = [None, train['targets'].shape[1]]


# save results to file
with open(save_path, 'wb') as f:
	f.write("%s\t%s\t%s\t%s\n"%('model', 'num_params', 'ave roc', 'ave pr'))

	# loop through models
	for activation in activations:
		for model_name in all_models:

			roc_mean = []
			roc_std = []
			pr_mean = []
			pr_std = []
			for trial in range(num_trials):
				tf.reset_default_graph()
				print('model: ' + model_name)

				# load model parameters
				genome_model = helper.import_model(model_name)
				model_layers, optimization = genome_model.model(input_shape, output_shape, activation)

				# build neural network class
				nnmodel = nn.NeuralNet()
				nnmodel.build_layers(model_layers, optimization, supervised=True)
				nnmodel.inspect_layers()

				# create neural trainer
				file_path = os.path.join(params_path, model_name+'_'+activation+'_'+str(trial))
				nntrainer = nn.NeuralTrainer(nnmodel, save='best', file_path=file_path)

				# initialize session
				sess = utils.initialize_session()

				# set the best parameters
				nntrainer.set_best_parameters(sess)

				# count number of trainable parameters
				all_params = sess.run(nntrainer.nnmodel.get_trainable_parameters())
				num_params = 0
				for params in all_params:
					if isinstance(params, list):
						for param in params:
							num_params += np.prod(param.shape)
					else:
						num_params += np.prod(params.shape)

				# get performance metrics
				predictions = nntrainer.get_activations(sess, test, 'output')
				roc, roc_curves = metrics.roc(test['targets'], predictions)
				pr, pr_curves = metrics.pr(test['targets'], predictions)

				roc_mean.append(np.mean(roc))
				roc_std.append(np.std(roc))
				pr_mean.append(np.mean(pr))
				pr_std.append(np.std(pr))

				sess.close()
			mean_roc = np.mean(roc_mean)
			std_roc = np.std(roc_mean)
			mean_pr = np.mean(pr_mean)
			std_pr = np.std(pr_mean)
			f.write("%s\t%d\t%.3f$\pm$%.3f\t%.3f$\pm$%.3f\n"%(model_name+'_'+activation, num_params, mean_roc, std_roc, mean_pr, std_pr))
