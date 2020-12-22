import matplotlib.pyplot as plt
import os
import re
import shutil
import string
import tensorflow as tf

from tensorflow.keras import layers
from tensorflow.keras import losses
from tensorflow.keras import preprocessing
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization

import pandas as pd
import numpy as np
import pdb
import mysql.connector
import datetime

def trainSentimentTrades(cnx):
    cursor = cnx.cursor()
    query = """
            select nbaID, date, title, content, traded 
            from rotoworld
            where nbaID is not null
            """
    dataset = pd.read_sql_query(query, cnx)
    # split the dataset into 80-20 parts
    # randomize the dataset order so we don't get a 
    # huge chunk of consecutive offseason moves
    trainSet = dataset.sample(frac=0.8)
    testSet = dataset.drop(trainSet.index)
    testSet = testSet.sample(frac=1)

    print(trainSet.head())
    print("....")
    print(testSet.head())
    return

def trainSentimentAvail(cnx):
    cursor = cnx.cursor()
    return

