# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 15:35:00 2017

@author: john
"""

from capstoneScraper import *

import unittest

class testScraper( unittest.TestCase ):
    
    def test_genTargetDict( self ):
        testWord = 'honey'
        expResult = ['miel', 'chérie', 'le miel', 'miels', 'chéri']
        result = {}
        genTargetDict(testWord, result, 'eng')
        result = list(result['honey'].keys())
        self.assertEqual(set(expResult), set(result))
    
    def test_sameLangTranslations( self ):
        sourceWord = 'A'
        exampleLattice = {'A' : {'Z' : 1}, 'Z' : {'B' : 1, 'C' : 2, 'D' : 3}}
        result = {'B' : 0, 'C' : 0, 'D' : 0}
        expResult = {'B' : 1, 'C' : 2, 'D': 3}
        sameLangTranslations(sourceWord, exampleLattice, result)
        self.assertEqual(result, expResult)
        
    def test_translationPairsToLattice( self ):
        exampleLattice = {'A' : {'Z' : 1}, 'Z' : {'B' : 1}, 'B' : {'Y' : 10}}
        exampleWordList = ['A', 'B', 'Y', 'Z']
        exampleIters = [['A'], ['B']]
        expResult = {'Y': {'Y': 0, 'B': 0, 'A': 0, 'Z': 0}, 
                     'B': {'Y': 10, 'B': 0, 'A': 0, 'Z': 0}, 
                     'A': {'Y': 10, 'B': 1, 'A': 0, 'Z': 1}, 
                     'Z': {'Y': 0, 'B': 1, 'A': 0, 'Z': 0}}
        result = translationPairsToLattice(exampleWordList, exampleLattice, exampleIters)
        self.assertEqual(result, expResult)
        
    def test_constructMasterWordList( self ):
        list1 = [['A', 'B', 'C'], ['A']]
        list2 = [['V', 'W'], ['X', 'Y', 'Z']]
        expResult = ['A', 'B', 'C', 'X', 'Y', 'Z', 'V', 'W']
        result = constructMasterWordList(list1, list2)
        self.assertEqual(result, expResult)
        
    def test_wholeScraper( self ):
        expResult = (13, 10)
        result = generateWordData('boat', 2).shape
        self.assertEqual(result, expResult)
        
if __name__ == '__main__':
    unittest.main()