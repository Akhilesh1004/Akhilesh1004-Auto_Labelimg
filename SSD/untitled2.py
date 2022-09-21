#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  2 22:00:08 2022

@author: ray
"""


import nltk
from nltk.book import *
nltk.download()
from nltk.corpus import PlaintextCorpusRead
corpus_root = r'C:\Users\User\Downloads'
wordlists = PlaintextCorpusReader(corpus_root, '.*')
wordlists.fileids()
word_raw = wordlists.raw('1364.txt')
word_words = wordlists.words('1364.txt')
word_sents = wordlists.sents('1364.txt')
#word_vocab = wordlists.raw('1364.txt')






