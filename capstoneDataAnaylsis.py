import numpy as np
import tflearn

from tflearn.data_utils import load_csv
data,  labels = load_csv('testfile.csv',  target_column=2, categorical_labels=True,  n_classes=100)



def reassign(data, library):
    for i in range(len(data)):
        if(i in library):
            data[0][i] = library.index(data[0][i]) +2
        else:
            library.append(data[i][0])
            data[i][0] = library.index(data[i][0]) +2
    return np.array(data, dtype=np.float32) 

listOfWords = []

data = reassign(data, listOfWords)

net = tflearn.input_data([None,  5])
net = tflearn.fully_connected(net,  30)
net = tflearn.fully_connected(net,  100,  activation='softmax')
net = tflearn.regression(net)

model = tflearn.DNN(net)
print("Model stuff?")
model.fit(data,  labels,  n_epoch= 8,  batch_size=10,  show_metric=True)

exampleItem = [1, 4,  17,  89,  1]

print("Before predictions")

pred = model.predict([exampleItem])

print("Example output: ",  pred[0][1])
