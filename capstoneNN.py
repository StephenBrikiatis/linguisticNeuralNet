# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 06:55:56 2017

@author: john
"""

import tflearn
import numpy as np
#Currently configure to handle the word child (2 layers) as the test training data

trainDat = np.load('training_honey.npy')
testDat = np.load('test_wood.npy')
testWords = ['child', 'children', 'infant', 'baby', 'childcare', 'childhood', 'kids',
       'warn', 'facilities', 'bodies', 'dear', 'have', 'structure',
       'sweetheart', 'careful', 'infants', 'minors', 'darling', 'warning',
       'baby out', 'kid', 'honey', 'structural', 'babies', 'guard', 'care']
trainingTargets = np.array([[1, 0, 0, 0],
                   [0, 1, 0, 0],
                   [0, 0, 0, 1],
                   [0, 1, 0, 0],
                   [1, 0, 0, 0],
                   [1, 0, 0, 0],
                   [1, 0, 0, 0],
                   [1, 0, 0, 0],
                   [0, 0, 1, 0]])


net = tflearn.input_data(shape=[None, 10])
net = tflearn.fully_connected(net, 32,  weight_decay = 0.01)

net = tflearn.fully_connected(net, 4, activation='softmax',  weight_decay= 0.01)
net = tflearn.regression(net, optimizer = "adam",  learning_rate = 0.01)

# Define model
model = tflearn.DNN(net)
# Start training (apply gradient descent algorithm)
model.fit(trainDat, trainingTargets, n_epoch=800, batch_size=5, show_metric=True)

pred = model.predict(testDat)
groups = [[],[],[],[]]
for i in range(0, len(pred)):
    grouped = False
    for j in range(0, 3):
        if pred[i][j] > .65:
            grouped = True
            groups[j].append(testWords[i])
        if j == 2 and not grouped:
            groups[3].append(testWords[i])
            
print(groups)
