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
    start = time.time()
    for rawfile in listdir('tests/text'):
        text = '\n'.join(codecs.open(rawfile, 'r', 'utf-8').readlines())
        wds = gkseg.seg(text)
        o = codecs.open(os.path.join('tests/temp', os.path.basename(rawfile)), 'w', 'utf-8')
        o.write(' '.join(wds))
        o.close()
        count = count + 1
    print '---------------------------------------------------------------'
    print time.time() - start
    print count
    print '---------------------------------------------------------------'
    gkseg.destroy()

if __name__ == "__main__":
    main()
