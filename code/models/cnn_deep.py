
def model(input_shape, output_shape, activation='relu', dropout=True, l2=True, batch_norm=True):

    layer1 = {  'layer': 'input',
                'input_shape': input_shape
             }
    layer2 = {  'layer': 'conv1d',
                'num_filters': 30,
                'filter_size': 19, 
                'padding': 'SAME',
                'activation': activation,
                }
    if dropout:
        layer2['dropout'] = 0.1
    if batch_norm:
        layer2['norm'] = 'batch'
    layer3 = {  'layer': 'conv1d',
                'num_filters': 64,
                'filter_size': 9,  #195
                'padding': 'VALID', 
                'activation': 'relu',
                'max_pool': 3,  # 65
                }
    if dropout:
        layer3['dropout'] = 0.2
    if batch_norm:
        layer3['norm'] = 'batch'

    layer4 = {  'layer': 'conv1d',
                'num_filters': 96,
                'filter_size': 6,  
                'padding': 'VALID', # 60
                'activation': 'relu',
                'max_pool': 4,  # 15
                }
    if dropout:
        layer4['dropout'] = 0.3
    if batch_norm:
        layer4['norm'] = 'batch'

    layer5 = {  'layer': 'conv1d',
                'num_filters': 128,
                'filter_size': 4, # 12
                'padding': 'VALID',
                'activation': 'relu',
                'max_pool': 3, # 4
                }
    if dropout:
        layer5['dropout'] = 0.4
    if batch_norm:
        layer5['norm'] = 'batch'
    layer6 = {  'layer': 'dense',
	        'num_units': 512,
	        'activation': 'relu',
            }
    if dropout:
        layer6['dropout'] = 0.5
    if batch_norm:
        layer6['norm'] = 'batch'

    layer7 = {  'layer': 'dense',
                'num_units': output_shape[1],
                'activation': 'sigmoid',
                }

    model_layers = [layer1, layer2, layer3, layer4, layer5, layer6, layer7]

    # optimization parameters
    optimization = {"objective": "binary",
                  "optimizer": "adam",
                  "learning_rate": 0.001,
                  }
    if l2:
        optimization['l2'] = 1e-6

    return model_layers, optimization
