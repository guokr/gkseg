#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os
import time
from multiprocessing import Pool

import gkseg

def listdir(currentDir):
    for dirname, dirnames, filenames in os.walk(currentDir):
        for filename in filenames:
            yield os.path.join(dirname, filename)

def seg(rawfile):
    text = '\n'.join(codecs.open(rawfile, 'r', 'utf-8').readlines())
    wds = gkseg.seg(text)
    o = codecs.open(os.path.join('tests/temp', os.path.basename(rawfile)), 'w', 'utf-8')
    o.write(' '.join(wds))
    o.close()

def main():
    gkseg.init('data/model.txt')
    p = Pool(5)
    start = time.time()
    p.map(seg, listdir('tests/text'))
    print '---------------------------------------------------------------'
    print time.time() - start
    print '---------------------------------------------------------------'
    gkseg.destroy()

if __name__ == "__main__":
    main()

