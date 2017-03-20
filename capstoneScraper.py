# -*- coding: utf-8 -*-
import requests
from lxml import html
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

#generates a dictionary of target words and weights
#adds it to linkDict with the key being sourceWord
def genTargetDict(sourceWord, linkDict, lang):
    #target url for english and german
    eURL = 'http://opus.lingfil.uu.se/lex.php'
    gURL = 'http://opus.lingfil.uu.se/lex.php?l=ger'
    #Using limited search for demo purposes (POST does not include all=1)
    ePayload = {'ger':'on', 'w':sourceWord, 'submit':'select', 'c':'all', 'all' : '1'}
    gPayload = {'eng':'on', 'w':sourceWord, 'submit':'select', 'c':'all', 'all' : '1'}
    if lang == 'eng':
        URL = eURL
        payload = ePayload
    else:
        URL = gURL
        payload = gPayload
    page = requests.post(URL, data=payload)
    #parse page to get words and frequencies
    tree = html.fromstring(page.content)
    frequencies = tree.xpath('//td[@class="freq"]/a/text()')
    words = tree.xpath('//td[@class="trg"]/a/text()')
    linkDict[sourceWord] = dict(zip(words, frequencies))
    #remove all words that already exist in the graph
    for word in linkDict.keys():
        linkDict[sourceWord].pop(word, None)

lang = 'eng'
#create graph for displaying lattice
visual = nx.Graph()
#dictionary of dictionaries, connects words to their translations and lists weights
wordLinks = {}
#get source word from user for demo purposes
sourceWord = input('Source word: ')
iterations = int(input('Number of iterations: '))
genTargetDict(sourceWord, wordLinks, lang)
#Mirror for the first time
nextSources = list(wordLinks.values())[0].keys()
#limit iterations of mirroring to 4 for demo purposes
for iterLimit in range(0,iterations):
    #toggle language selection with each iteration
    if lang == 'eng':
        lang = 'ger'
    else:
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