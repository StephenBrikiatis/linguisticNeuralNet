# -*- coding: utf-8 -*-
import requests
from lxml import html
import networkx as nx

#generates a dictionary of target words and weights
#adds it to linkDict with the key being sourceWord
def genTargetDict(sourceWord, linkDict, lang):
    #target url for english and german
    eURL = 'http://opus.lingfil.uu.se/lex.php'
    gURL = 'http://opus.lingfil.uu.se/lex.php?l=ger'
    #Using limited search for demo purposes (POST does not include all=1)
    ePayload = {'ger':'on', 'w':sourceWord, 'submit':'select', 'c':'all'}
    gPayload = {'eng':'on', 'w':sourceWord, 'submit':'select', 'c':'all'}
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
sourceWord = input('Input source word: ')
genTargetDict(sourceWord, wordLinks, lang)
#Mirror for the first time
nextSources = list(wordLinks.values())[0].keys()
#limit iterations of mirroring to 4 for demo purposes
for iterLimit in range(0,100):
    #toggle language selection with each iteration
    if lang == 'eng':
        lang = 'ger'
    else:
        lang = 'eng'
    while nextSources:
        print(nextSources)
        #no candidate sources yet for this iteration
        candidateSources = []
        #for each source, find all translations
        #add all translations to candidateSources
        for source in nextSources:
            src = str(source)
            print(src + ' ' + lang)
            genTargetDict(src, wordLinks, lang)
            print(list(wordLinks[src]))
            #add all keys(translations) to the candidate list
            for word in list(wordLinks[src]):
                candidateSources.append(word)
            print(candidateSources)
        nextSources = []
    nextSources = candidateSources
        
#add edges and nodes to the graph
for source in wordLinks.keys():
    for target in wordLinks[source]:
        print(source + ' ' + target + ' ' + wordLinks[source][target])
        #visual.add_edge(sourceWord, target, weight=wordLinks[sourceWord][target])