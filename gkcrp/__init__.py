#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gkcrp.corpus as corpus

def load(basedir):
    return corpus.Corpus(basedir)

def alltext(basedir, aspect):
    return corpus.Corpus(basedir).texts(aspect)
