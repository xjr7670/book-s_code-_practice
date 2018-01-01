#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 15:02:24 2018

@author: cavin
"""

import nltk
import pprint


# sample files that we use in this chapter
#filename = 'apacheMeetingMinutes.txt'
#filename = 'djangoIRCchat.txt'
#f1ilename = 'gnueIRCsummary.txt'
#filename = 'lkmlEmails.txt'
filename = 'lkmlEmailsReduced.txt'

with open(filename, 'r', encoding='utf8') as sampleFile:
    text = sampleFile.read()

en = {}
try:
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = sent_detector.tokenize(text.strip())
    
    for sentence in sentences:
        tokenized = nltk.word_tokenize(sentence)
        tagged = nltk.pos_tag(tokenized)
        chunked = nltk.ne_chunk(tagged)
        for tree in chunked:
            if hasattr(tree, 'label'):
                ne = ' '.join(c[0] for c in tree.leaves())
                en[ne] = [tree.label(), ' '.join(c[1] for c in tree.leaves())]
except Exception as e:
    print(str(e))

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(en)