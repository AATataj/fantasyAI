# linearRegression.py
import numpy as np 
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

def linReg(cnx) :
    ## set up db cursor : 
    cursor = cnx.cursor()

    ## get vince carter's data from db :
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

    ##### building model :
    print ("shape[0] : "+ str(labelsTrain.shape[0]))
    ##print ("shape[1] : "+ str(labelsTrain.shape[1]))
    ##print ("shape[2] : "+ str(labelsTrain.shape[2]))
    
    #layers.Dense(64, activation='relu', input_shape=[labelsTrain.shape[0]]),
        
    model = keras.Sequential([
        layers.Dense(64, activation='relu', input_shape=[len(features.keys())]),
        layers.Dense(64, activation='relu'),
        layers.Dense(1)
    ])
    optimizer = tf.keras.optimizers.RMSprop(0.001)

    model.compile(loss='mse', optimizer=optimizer, metrics=['mae', 'mse'])
    print('model compiled...')
    #print basic data about the compiled model
    model.summary()

    result = model.predict(featuresTrain)
    print(result)


    print ("linReg() complete.")

