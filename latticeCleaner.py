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


treeArray = []
#remove characters from the starting word to make it readable
word = json_starting_word.replace("[",  "").replace("]",  "").replace('"',  "")
print(word)

#order of items in the treeArray: word, row, position in row, items it connects to or is connected to.
treeArray = [[word,  0,  0]]

#This for loop builds the tree by checking each item of the TreeArray in the current loop, and finding what they are connected to.
rowSizes = []
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
    for identifierRow in range(0,  rows+1):
        total = 1
        for adder in rowSizes:
            total += adder
        subtotal = total - rowSizes[-1]
        print(rowSizes)
        print(treeArray)
        for identiferPositionX in range(0,  subtotal):
            for identifierPositionY in range(0,  total):
                print ("%02d, %02d" % (identiferPositionX,  identifierPositionY))
                print(treeArray[identifierPositionY])
                if(treeArray[identiferPositionX][0] == treeArray[identifierPositionY][0]):
                    del treeArray[identiferPositionX]
                    rowSizes[-1] -= 1
                    
print(treeArray)
#holderItem = fixedLattice.get(word)
#holderArray.append(holderItem)
#holderArray.append(currentRow)
#theRealLattice.append(holderArray)
#
#for times in range(0,  4):
#    for item in holderItem:
#        holderItem = fixedLattice.get(item, "empty")
#        holderArray.append(holderItem)
#    currentRow += 1
#    theRealLattice.append(holderArray)    
