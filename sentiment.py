# sentiment.py
import pdb

import numpy as np 
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

print (tf.__version__)

import tensorflow_docs as tfdocs
import tensorflow_docs.plots

##
## This is gonna be the sentiment analysis of player availability
## Starting tomorrow this is the next focus.
## Afterward, we'll work on quickening up features processing
## and look into creating a k8s cluster here at home
## :D :D :D
##