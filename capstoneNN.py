# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 06:55:56 2017

@author: john
"""

import tflearn
import numpy as np
import json
#Currently configure to handle the word child (2 layers) as the test training data
categorizationThreshold = input("Categorization Threshold: ")
oneCategoryOnly = 'z'
while oneCategoryOnly.lower() not in ['y', 'n']:
    oneCategoryOnly = input("Only place words in one category [Y/N]: ")
trainDat = np.load('training_honey.npy')
testDat = np.load('test_wood.npy')
testWords = ['child', 'children', 'infant', 'baby', 'childcare', 'childhood', 'kids',
       'warn', 'facilities', 'bodies', 'dear', 'have', 'structure',
       'sweetheart', 'careful', 'infants', 'minors', 'darling', 'warning',
       'baby out', 'kid', 'honey', 'structural', 'babies', 'guard', 'care']
trainingTargets = np.array([[1, 0, 0],
                   [0, 1, 0],
                   [0, 0, 1],
                   [0, 1, 0],
                   [1, 0, 0],
                   [1, 0, 0],
                   [1, 0, 0],
                   [1, 0, 0],
                   [0, 0, 1]])


net = tflearn.input_data(shape=[None, 10])
net = tflearn.fully_connected(net, 8,  weight_decay = 0.01)


net = tflearn.fully_connected(net, 4, activation='softmax',  weight_decay= 0.1)
net = tflearn.regression(net, optimizer = "adam",  learning_rate = 0.1)


# Define model
model = tflearn.DNN(net)
# Start training (apply gradient descent algorithm)
model.fit(trainDat, trainingTargets, n_epoch=800, batch_size=5, show_metric=True)

pred = model.predict(testDat)
groups = [] #[[],[],[],[]]
if oneCategoryOnly.lower() == 'y':
    for i in range(0, len(pred)):
        grouped = 0
        for j in range(0, 4):
            if pred[i][j] > categorizationThreshold and pred[i][j] > grouped:
                grouped = pred[i][j]
                temp = [j,  testWords[i]]
            if j == 4 - 1 and not grouped:
                temp = [4,  testWords[i]]
        groups.append(temp)
if oneCategoryOnly.lower() == 'n':
    for i in range(0, len(pred)):
        grouped = False
        for j in range(0, 4):
            if pred[i][j] > categorizationThreshold:
                grouped = True
                temp = [j,  testWords[i]]
                groups.append(temp)
            if j == 4 - 1 and not grouped:
                temp = [4,  testWords[i]]
                groups.append(temp)
groups.sort()
print(groups)

with open("visualization/netOutput.json",  "w") as output:
    json.dump(groups,  output)
