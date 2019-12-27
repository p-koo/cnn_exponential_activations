# Learning Sequence Motifs with Exponential Activations

This is a repository that contains datasets and scripts to reproduce the results of "Improving Convolutional Network Interpretability with Exponential Activations" by Peter K. Koo and Matt Ploenzke, which was presented at the ICML Workshop for Computational Biology 2019 in Long Beach, CA. A preprint of the workshop abstract can be found here: https://www.biorxiv.org/content/10.1101/650804v1


The code here depends on Deepomics, a custom-written, high-level APIs written on top of Tensorflow to seamlessly build, train, test, and evaluate neural network models.  WARNING: Deepomics is a required sub-repository.  To properly clone this repository, please use: 

$ git clone --recursive \url{https://github.com/p-koo/cnn_exponential_activations.git}

#### Dependencies
* Tensorflow r1.0 or greater (preferably r1.14 or r1.15)
* Python dependencies: PIL, matplotlib, numpy, scipy (version 1.1.0), sklearn
* meme suite (5.1.0)

## Overview of the code

To generate datasets:
* code/0_Generate_synthetic_datasets.ipynb
* code/0_Generate_invivo_datasets.ipynb


To train the models on the synthetic dataset and the in vivo dataset and also to get the first convolutional layer representations: 
* code/1_train_synthetic_data.py 
* code/1_train_invivo_data.py 

These scripts loop through all models described in the manuscript.  Each model can be found in /code/models/

To evaluate the performance of each model on the test set: 
* code/2_print_performance_table_synthetic.py 
* code/2_print_performance_table_invivo.py 


To perform the Tomtom search comparison tool :
* code/3_tomtom_compare_synthetic.sh  
* code/3_tomtom_compare_invivo.sh  

Requires Tomtom installation as well as command-line abilities from the current directory.

To calculate statistics across different initialization trials for each model, this script aggregates the matches to ground truth motifs:
* code/4_match_statistics_synthetic.sh  
* code/4_match_statistics_invivo.sh  


## Overview of data

* Due to size restrictions, the dataset is not included in the repository.  Each dataset can be easily created by running the python notebooks: Generate_synthetic_datasets.ipynb and Generate_invivo_datasets.ipynb
* JASPAR_CORE_2016_vertebrates.meme contains a database of PWMs which is used for the Tomtom comparison search
* pfm_vertebrates.txt also contrains JASPAR motifs. This is the file that is used as ground truth for the synthetic dataset.

## Overview of results

* All results for each CNN model and dataset are saved in a respective directory (synthetic or invivo). 
* Trained model parameters are saved in results/synthetic/model_params.  
* visualization for convolution filters and results from Tomtom are saved in results/synthetic/conv_filters
* A reported performance table is saved in results/synthetic/performance_summary.tsv (automatically outputted from print_performance_table_synthetic.py)


