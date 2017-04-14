import json
#open all files
json_data = open("latticeOutput.json").read()
json_starting_word = open("visualization/scraperOutput.json").read()
lattice_raw = json.loads(json_data)
fixedLattice = {}
currentRow = 0;

#removes all items with 0 connections from the dictionary.
for dict in lattice_raw:
    fixedLattice[dict] = {}
    for item in lattice_raw[dict]:
       if lattice_raw[dict][item] != 0:
           fixedLattice[dict][item] = lattice_raw[dict][item]

removalList = []

for entries in fixedLattice:
    removalList.append([entries, 0])

treeArray = []
#remove characters from the starting word to make it readable
word = json_starting_word.replace("[",  "").replace("]",  "").replace('"',  "")

#order of items in the treeArray: word, row, position in row, items it connects to or is connected to.
treeArray = [[word,  0,  0]]

#This for loop builds the tree by checking each item of the TreeArray in the current loop, and finding what they are connected to.
rowSizes = []
clean = 0
for rows in range(0,  4):
    holder = []
    arrayLength = len(treeArray);
    itemNumber = 0;
    for node in range(0, arrayLength):
        if(treeArray[node][1] == rows):
            for items in fixedLattice[treeArray[node][0]]:
                treeArray.append([items,  rows+1,  itemNumber])
                itemNumber += 1
#this halve of the for loop removes extras and copies of words that would create a feedback loop
    rowSizes.append(itemNumber)
    for items in range(0,  len(treeArray)):
        for removalItem in removalList:
            if(items < len(treeArray)):
                if(treeArray[items][0] == removalItem[0]):
                    if(removalItem[1] >= 1):
                        del treeArray[items]
                    else:
                        removalItem[1] = 1
    for reset in removalList:
        reset[1] = 0
#secondary check to remove any extra doubles
while clean == 0:
    clean = 1
    for items in range(0,  len(treeArray)):
        for removalItem in removalList:
            if(items < len(treeArray)):
                if(treeArray[items][0] == removalItem[0]):
                    if(removalItem[1] >= 1):
                        del treeArray[items]
                        clean = 0
                    else:
                        removalItem[1] = 1
    for reset in removalList:
        reset[1] = 0
      
print(treeArray)

with open("visualization/cleanerOutput.json",  "w") as output:
    json.dump(treeArray,  output)
