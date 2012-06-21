#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os
import time

import gkseg

def listdir(currentDir):
    for dirname, dirnames, filenames in os.walk(currentDir):
        for filename in filenames:
            yield os.path.join(dirname, filename)

def main():
    gkseg.init('data/model.txt')
    count = 0
    length = 0
    start = time.time()
    for rawfile in listdir('tests/text'):
        text = '\n'.join(codecs.open(rawfile, 'r', 'utf-8').readlines())
        (wds, terms, labeled, err) = gkseg.process(text, True)
        count = count + len(err)
        length = length + len(wds)
    print '---------------------------------------------------------------'
    print float(count)/length
    print '---------------------------------------------------------------'
    gkseg.destroy()

if __name__ == "__main__":
    main()
