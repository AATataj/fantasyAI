import collections
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import pandas as pd
import mysql.connector

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dropout
# This is the first attempt to get a model to work.
# it's using an LSTM to predict daily stats per player
# LSTM isn't necessary because my featureset contains career/seasons/monthly/weekly averages as features
# and the number of previous steps varies from player to player, and isn't necessarily the latest step 
# in the mdel that matters.  As a result, I'm hammering a square peg into a round hole here trying to get 
# perceptron to fit into the shape of an LSTM.  I'm going to re-write this as a perceptron model
# but keep this code as an example.

def train(cnx):
    ## set up db cursor : 
    cursor = cnx.cursor()

    ## get the data from db :
    query = """
            select * from inputvectors where playerID = 3019 order by date asc
            """
    unfiltered = pd.read_sql_query(query, cnx)

    ## partition into the labels and features
    labels = unfiltered.pts
    features = unfiltered.drop(["index", "name", "date", "playerID", "fgPer", "ftPer", "pts", "3fgm", "trb", 
    "ast", "stl", "blk", "tov"], axis=1)

    ## normalize feature values to between 0..1:

    ## by standard deviation (handles outliers better):
    features=(features-features.mean())/features.std()
    
    ## by min-max normalization (handles same scale best): 
    ####features=(features-features.min())/(features.max()-features.min())
    


    ## partition into training vs testing sets
    labelsTrain = labels.iloc[1:1229]
    labelsTest = labels.iloc[1330:1529]
    featuresTrain = features.iloc[1:1229]
    featuresTest = features.iloc[1330:1529]

    print(featuresTrain.head())

    ## convert to numpy arrays
    labelsTrain = np.array(labelsTrain)
    labelsTest = np.array(labelsTest)
    featuresTrain = np.array(featuresTrain)
    featuresTest = np.array(featuresTest)

    ## reshape numpy arrays to something tensorflow lstms will like :
    print ("samples " + str(featuresTrain.shape[0]))
    print ("features per sample " + str(featuresTrain.shape[1]))    
    featuresTrain = np.reshape(featuresTrain, (featuresTrain.shape[0], 1, featuresTrain.shape[1]))
    featuresTest = np.reshape(featuresTest, (featuresTest.shape[0], 1, featuresTest.shape[1]))

    ## create the model :
    model = Sequential()
    ## figuring out the add() call...
    print(featuresTrain.shape[2])
    ## units => a parameter I need to play with.  Too low -> underfitting, too high -> overfitting
    ## basically, how many lstm (memory units?) in a cell.  Before running,
    ## I'm thinking one per feature?
    
    ## return sequences
    model.add(LSTM(units=50, return_sequences=True, input_shape=(featuresTrain.shape[1], featuresTrain.shape[2])))
    # dropout helps prevent overfitting during training
    # randomly 
    model.add(Dropout(0.2))

    # add a couple more dropout layers (these appear to be intermediate layers combining various features in aggregate)
    model.add(LSTM(units=50, return_sequences=True, input_shape=(featuresTrain.shape[1], featuresTrain.shape[2])))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=True, input_shape=(featuresTrain.shape[1], featuresTrain.shape[2])))
    model.add(Dropout(0.2))

    # add a dense layer at the end (dense is a fully connected layer where every neuron of output is connected to 
    # every previous layer's neurons of input)
    model.add(Dense(units=1))

    # adam = adaptive movement estimation.  A different method for optimizing gradient descent
    model.compile(optimizer='adam', loss='mean_squared_error')
    print ("model compiled...")

    model.fit(features, labels, epochs=100, batch_size=32)

    print ("model trained...gotta learn how to visualize results now...")
