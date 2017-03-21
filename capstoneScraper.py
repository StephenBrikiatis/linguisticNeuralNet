# -*- coding: utf-8 -*-
import requests
import tflearn
from lxml import html
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.tools as plTools
import plotly.plotly as py
import plotly.graph_objs as go

#generates a dictionary of target words and weights
#adds it to linkDict with the key being sourceWord
def genTargetDict(sourceWord, linkDict, lang):
    #target url for english and french
    sURL = 'http://opus.lingfil.uu.se/lex.php'
    tURL = 'http://opus.lingfil.uu.se/lex.php?l=fre'
    #Using limited search for demo purposes (POST does not include all=1)
    #Given results of demo and other tests, I recommend using limited search in all cases
    sPayload = {'fre':'on', 'w':sourceWord, 'submit':'select', 'c':'all'}
    tPayload = {'eng':'on', 'w':sourceWord, 'submit':'select', 'c':'all'}
    if lang == 'eng':
        URL = sURL
        payload = sPayload
    else:
        URL = tURL
        payload = tPayload
    page = requests.post(URL, data=payload)
    #parse page to get words and frequencies
    tree = html.fromstring(page.content)
    rawFreq = tree.xpath('//td[@class="freq"]/a/text()')
    words = tree.xpath('//td[@class="trg"]/a/text()')
    intFreq = [int(str(i)) for i in list(rawFreq)]
    normFreq = [float(i)/sum(intFreq) for i in list(intFreq)]
    linkDict[sourceWord] = dict(zip(words, normFreq))
    #remove all words that already exist in the graph
    for word in linkDict.keys():
        linkDict[sourceWord].pop(word, None)
        
def sameLangTranslations(sourceWord, lattice, wordDict):
    for mirroredWord in lattice[sourceWord]:
        weight = lattice[sourceWord].get(mirroredWord, 0)
        if not weight == 0 and mirroredWord in lattice:
            for synonym in lattice[mirroredWord]:
                wordDict[synonym] += weight * lattice[mirroredWord][synonym]
                
def generateWordData():
    lang = 'eng'
    #dictionary of dictionaries, connects words to their translations and lists weights
    wordLinks = {}
    #lists holding what words were added at each iteration, grouped by language
    sourceIterations = []
    targetIterations = []
    #get source word from user
    sourceWord = input('Source word: ')
    sLangLayers = int(input('Number of source language layers: '))
    #number of iterations needed to generage desired depth, minus 1 because the initial word is a layer
    #layers is then doubled because for each layer created in source lang. a target lang layer must also be created
    iterations = ( sLangLayers - 1 ) * 2
    #Add the list of iteration 0 words to the source list
    sourceIterations.append([sourceWord])
    #generate the first set of translations
    genTargetDict(sourceWord, wordLinks, lang)
    #Mirror for the first time (target treated as source, source treated as target)
    nextSources = list(list(wordLinks.values())[0].keys())
    #limit iterations of mirroring to the user defined value
    for iterLimit in range(0,iterations):
        #toggle language selection with each iteration, lang is the current source language
        if lang == 'eng':
            #if the last source was english, the nextSources will be french
            targetIterations.insert(0, list(set(nextSources)))
            lang = 'fre'
        else:
            #if the last source was not english, the nextSources will be english
            sourceIterations.insert(0, list(set(nextSources)))
            lang = 'eng'
        while nextSources:
            #no candidate sources yet for this iteration
            candidateSources = []
            #for each source, find all translations
            #add all translations to candidateSources
            for source in nextSources:
                src = str(source)
                genTargetDict(src, wordLinks, lang)
                #add all keys(translations) to the candidate list
                for word in list(wordLinks[src]):
                    candidateSources.append(word)
            nextSources = []
        nextSources = candidateSources
        print(iterations - iterLimit)
    
    #record the last set of targets after the mirroring finishes
    targetIterations.insert(0, nextSources)
    #Create a master list of all words in the order that they will have in the tensorFlow input
    allWords = []
    for wordIter in reversed(sourceIterations):
        for word in wordIter:
            allWords.append(word)
            
    for wordIter in reversed(targetIterations):
        for word in wordIter:
            allWords.append(word)
    #remove any duplicates from allWords
    allWords = list(set(allWords))
    #Build dictionaries for each word that extend past initial translations
    wordDicts = {}
    for eachWord in allWords:
        wordDicts[eachWord] = {}
        #add all the words to each dictionary
        for everyWord in allWords:
            wordDicts[eachWord][everyWord] = 0
        #add in the weights of the first translations to each word
        if eachWord in wordLinks:
            for eachKey in wordLinks[eachWord]:
                wordDicts[eachWord][eachKey] = wordLinks[eachWord][eachKey]
    #Starting from the bottom of the tree, connect every word to its translations
    #then connect the word to its childrens translations, weighted by its connection to its children       
    for eachIter in sourceIterations:
        for eachWord in eachIter:
            sameLangTranslations(eachWord, wordLinks, wordDicts[eachWord])
            for everyWord in wordDicts[eachWord]:
                weight = wordDicts[eachWord].get(everyWord, 0)
                if not weight == 0 and everyWord in wordDicts:
                    #checks that key exists, and skips if not
                    for eachConnection in wordDicts[everyWord]:
                        #checks that key exists, and skips if not
                        if eachConnection in wordDicts[eachWord] and eachConnection in wordDicts[everyWord]:
                            wordDicts[eachWord][eachConnection] += weight * wordDicts[everyWord][eachConnection]
        
    #Make all the connections bi-directional (each child connects back to its parent)
    for parent in wordDicts:
        for child in wordDicts[parent]:
            #skip if the child has no entry
            if child in wordDicts:
                wordDicts[child][parent] = wordDicts[parent][child]
                
    #normalize the dataset
    for eachDict in wordDicts.values():
        for eachWord in eachDict:
            if not sum(list(eachDict.values())) == 0:
                eachDict[eachWord] = eachDict[eachWord]/sum(list(eachDict.values()))
    
    #make all words connect to themselves
    for eachWord in wordDicts:
        wordDicts[eachWord][eachWord] = 1
        
    #convert dictionaries into a single data table
    dataTable = []
    rowNames = []
    
    for eachIter in reversed(sourceIterations):
        for eachWord in eachIter:
            rowNames.append(eachWord)
            dataTable.append(list(wordDicts[eachWord].values()))
    wordData = pd.DataFrame(dataTable)
    wordData.columns = allWords
    wordData.index = rowNames
    #reduce the dimensionality of the dataset to n x 30
    #this is to ensure consistent column meanings for the neural net
    #Credit to Sebastian Raschka's plotly tutorial for significant contributions to the PCA code section
    #Original tutorial can be found at https://plot.ly/ipython-notebooks/principal-component-analysis/#PCA-Vs.-LDA
    covariance = wordData.cov()
    eigenVals, eigenVects = np.linalg.eigh(covariance.values.real)
    eigenPairs = [(np.abs(eigenVals[i]), eigenVects[:,i]) for i in range(len(eigenVals))]
    eigenPairs = sorted(eigenPairs, key=lambda eigenPairs: eigenPairs[0])
    eigenPairs.reverse()
    transformation = np.array([i[1] for i in eigenPairs[0:10]])
    transformation = np.transpose(transformation)
    preparedData = wordData.dot(transformation)
    for iter8 in sourceIterations:
        print(iter8)
    print(len(allWords))
    return preparedData


#plTools.set_credentials_file(username='JackHouk', api_key='dEl1WMGPvkeClnayYxJz')
np.save('training_honey', generateWordData())
np.save('test_wood', generateWordData())
#Visualizations for demo here
'''
#sum weights so the edge weights can be normalized
totalWeight = 0
for source in wordLinks.keys():
    for target in wordLinks[source]:
        totalWeight = totalWeight + int(wordLinks[source][target])
#add edges and nodes to the graph
for source in wordLinks.keys():
    for target in wordLinks[source]:
        visual.add_edge(source, target, weight=int(int(wordLinks[source][target])/totalWeight*100000)/100)
        #visual.add_edge(source, target, weight=1000*int(wordLinks[source][target]))
pos=nx.spring_layout(visual, scale = 360, k = 1, iterations = 8)
nx.draw(visual,pos)
labels = nx.get_edge_attributes(visual,'weight')
nx.draw_networkx_nodes(visual,pos,node_size=1)
#nx.draw_networkx_edge_labels(visual,pos,edge_labels=labels)
nx.draw_networkx_labels(visual,pos,font_size=12,font_family='sans-serif')
plt.axis('off')
plt.savefig("test.png") 
plt.show()
'''