#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os.path as path
import yaml
import re

patnl   = re.compile(r'\n')
patmeta = re.compile(r'^(\w+): ([^:]+)$')
patvals = re.compile(r'([^,]+,)*([^,]+)')
patdelm = re.compile(r',')

class Corpus:

    def __init__(self, directory):
        if not(path.exists(directory)):
            raise Exception("directory dose not exists: %s"%directory)
        if not(path.isdir(directory)):
            raise Exception("path is not a directory: %s"%directory)
        self.root = directory

        index = path.join(directory, 'index.txt')
        if not(path.exists(index)):
            raise Exception("index file dose not exists: %s"%index)
        if not(path.isfile(index)):
            raise Exception("index path is not a file: %s"%index)
        self.index = index

        content = '\n'.join(codecs.open(index, 'r', 'utf-8').readlines())
        model = None
        try:
            model = yaml.load(content)
        except BaseException as err:
            raise Exception("error when reading index: %s"%str(err))

        if model['aspects'] != None:
            self.aspects = model['aspects']
        else:
            self.aspects = []

        if model['entries'] != None:
            self.entries = model['entries']
        else:
            self.entries = []

    def aspect(self, name):
        if name not in self.aspects:
            raise Exception("aspect dose not exists: %s"%aspect)
        else:
            for entry in self.entries:
                yield path.join(self.root, name, entry)

    def texts(self, aspect):
        for filename in self.aspect(aspect):
            yield Text(filename)

def valstr(val):
    if isinstance(val, str):
        return val
    elif isinstance(val, list):
        return ' '.join(val)
    else:
        return ''

class Text:

    def __init__(self, filename):
        if not(path.exists(filename)):
            raise Exception("file dose not exists: %s"%filename)
        if not(path.isfile(filename)):
            raise Exception("path is not a file: %s"%filename)
        lines = codecs.open(filename, 'r', 'utf-8').readlines()
        self.metadata = {}
        self.title = ''
        l = len(lines)
        if l == 1:
            self.content = lines[0].strip()
        elif l == 2:
            self.content = '\n'.join((lines[0].strip(), lines[1].strip()))
        else:
            self.title = lines[0].strip()
            idx = 0
            header = True
            while header:
                idx = idx + 1
                line = lines[idx].strip()
                header = re.match(patmeta, line)
                if header:
                    key = header.group(1)
                    values = header.group(2)
                    if re.match(patvals, values) != None:
                        values = re.split(patdelm, values)
                        self.metadata[key] = values
                    else:
                        break
            self.content = '\n'.join(lines[idx:])

    def meta(self, key):
        return self.metadata[key]

    def text(self):
        meta = '\n'.join([valstr(self.metadata[key]) for key in self.metadata])
        return '\n'.join([self.title, meta, self.content])

