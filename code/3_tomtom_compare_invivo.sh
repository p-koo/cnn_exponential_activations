#!/bin/bash

# In vivo TomTom analysis 
dirpath="../results/invivo/conv_filters"
for MODEL in cnn_2 cnn_50 cnn_deep
do
	for ACTIVATION in exp relu 
	do
		for TRIAL in {0..4}
		do
		    tomtom -evalue -thresh 0.1 -o $dirpath/${MODEL}_${ACTIVATION}_${TRIAL} $dirpath/${MODEL}_${ACTIVATION}_${TRIAL}_clip.meme ../data/JASPAR_CORE_2016_vertebrates.meme
		done
	done
done
