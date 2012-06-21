#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import OptionParser
import gkcrp
import re
import codecs
import subprocess
import os

patsp = re.compile(r'\s+')

def gen(basedir, aspect, trainfile):
    f = codecs.open(trainfile, 'a', 'utf8')
    for text in gkcrp.alltext(basedir, aspect):
        for item in patsp.split(text.text()):
            label = ['s', 'b', 'm', 'e']
            if len(item)>1 and item[-2:]=='\m':
                item = item[:-2]
                label = ['S', 'B', 'M', 'E']
            if len(item) == 0:
                continue
            if len(item) == 1:
                f.write('%s %s\n'%(item, label[0]))
            else:
                f.write('%s %s\n'%(item[0], label[1]))
                for i in item[1:-1]:
                    f.write('%s %s\n'%(i, label[2]))
                f.write('%s %s\n'%(item[-1], label[3]))
    f.close()


def train(trainfile, modelfile):
    subprocess.call(['wapiti/wapiti', 'train', '-p', 'data/pattern.txt', '-1', '5', trainfile, modelfile])

def main():
    usage = "usage: %prog [options] command arg1 arg2 ..."
    parser = OptionParser(usage)
    (options, args) = parser.parse_args()

    if len(args) == 0 or args[0] == 'help':
        print '\n'
        print usage
        print '\n\tgksegt add <basedir> <aspect> <trainfile>'
        print '\t\tgenerate training data based on the inputed corpus and'
        print '\t\tappend them to the specified training file'
        print '\t\t* basedir: the base directory of a corpus'
        print '\t\t* aspect: the specified aspect of a corpus'
        print '\t\t* trainfile: the output file name of the training data'
        print '\n\tgksegt train <trainfile> <modelfile>'
        print '\t\tgenerate model data based on the training file and'
        print '\n\toutput them to the specified model file'
        print '\t\t* trainfile: the input file name of the training data'
        print '\t\t* modelfile: the output file name of the model data'
    elif args[0] == 'add':
        basedir = args[1]
        if not os.path.isdir(basedir):
            raise Exception('basedir is not a directory')
        aspect = args[2]
        trainfile = args[3]
        gen(basedir, aspect, trainfile)
    elif args[0] == 'train':
        trainfile = args[1]
        if not os.path.exists(trainfile):
            raise Exception('trainfile does not exist')
        modelfile = args[2]
        train(trainfile, modelfile)
    else:
        print 'command unknown!'

if __name__ == "__main__":
    main()
