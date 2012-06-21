#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gkseg.segment.crf import seg as crfseg
from gkseg.segment.crf import init as crfinit
from gkseg.segment.crf import destroy as crfdestroy

def init(model):
    crfinit(model)

def process(text, countErr=False):
    return crfseg(text, countErr)

def seg(text):
    return crfseg(text)[0]

def term(text):
    return crfseg(text)[1]

def label(text):
    return crfseg(text)[2]

def destroy():
    crfdestroy()

