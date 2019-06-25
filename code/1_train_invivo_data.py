from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os, sys
import numpy as np
import matplotlib.pyplot as plt
import helper
import tensorflow as tf
from deepomics import neuralnetwork as nn
from deepomics import utils, fit, visualize

#------------------------------------------------------------------------------------------------


all_models = ['distnet', 'cnn_2', 'cnn_50']
activations = ['exp', 'relu']

num_trials = 5

# save path
results_path = utils.make_directory('../results', 'invivo')
params_path = utils.make_directory(results_path, 'model_params')
save_path = utils.make_directory(results_path, 'conv_filters')

# load dataset
data_path = '../data/invivo_dataset.h5'
train, valid, test = helper.load_invivo_dataset(data_path)

# get data shapes
input_shape = list(train['inputs'].shape)
input_shape[0] = None
output_shape = [None, train['targets'].shape[1]]

for activation in activations:
  for model_name in all_models:
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
            file_path = os.path.join(params_path, model_name+'_'+activation'_'+str(trial))
            nntrainer = nn.NeuralTrainer(nnmodel, save='best', file_path=file_path)

            # initialize session
            sess = utils.initialize_session()

            # set data in dictionary
            data = {'train': train, 'valid': valid, 'test': test}

            # fit model
            fit.train_minibatch(sess, nntrainer, data, batch_size=100, num_epochs=200,
                  patience=20, verbose=2, shuffle=True, save_all=False)


            # set the best parameters
            nntrainer.set_best_parameters(sess)
            
            # get 1st convolution layer filters
            fmap = nntrainer.get_activations(sess, test, layer='conv1d_0_active')
            W = visualize.activation_pwm(fmap, X=test['inputs'], threshold=0.5, window=19)


            # plot 1st convolution layer filters
            fig = visualize.plot_filter_logos(W, nt_width=50, height=100, norm_factor=None, num_rows=10)
            fig.set_size_inches(100, 100)
            outfile = os.path.join(save_path, model_name+'_'+activation+'_'+str(trial)+'_conv_filters.pdf')
            fig.savefig(outfile, format='pdf', dpi=200, bbox_inches='tight')
            plt.close()

            # save filters as a meme file for Tomtom 
            output_file = os.path.join(save_path, model_name+'_'+activation+'_'+str(trial)+'.meme')
            utils.meme_generate(W, output_file, factor=None)

            # clip filters about motif to reduce false-positive Tomtom matches 
            W = np.squeeze(np.transpose(W, [3, 2, 0, 1]))
            W_clipped = helper.clip_filters(W, threshold=0.5, pad=3)
            
            # since W is different format, have to use a different function
            output_file = os.path.join(save_path, model_name+'_'+activation+'_'+str(trial)+'_clip.meme')
            helper.meme_generate(W_clipped, output_file, factor=None) 

            
            