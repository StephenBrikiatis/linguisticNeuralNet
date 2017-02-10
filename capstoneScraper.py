# -*- coding: utf-8 -*-
import requests
from lxml import html

sourceWord = 'large'
URL = 'http://opus.lingfil.uu.se/lex.php'
payload = {'ger':'on', 'w':sourceWord, 'submit':'select', 'all':'1', 'c':'all'}
wordLinks = {}
page = requests.post(URL, data=payload)
tree = html.fromstring(page.content)
frequencies = tree.xpath('//td[@class="freq"]/a/text()')
words = tree.xpath('//td[@class="trg"]/a/text()')
wordLinks[sourceWord] = dict(zip(words, frequencies))
for links in wordLinks:
    print(links + str(wordLinks[links]))