#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

import gkseg.segment.corrector as corrector
from gkseg.segment.handler import Handler

patnl = re.compile(r'\n')
patsp = re.compile(r'\s+')

def read(result, countErr=False):
    model  = Model(result)
    handler = Handler()
    for ch, label, ctx in model:
        #print ch, label, ''.join(ctx)
        corrector.fix(model, ctx)
        if countErr:
            corrector.countErr(model, model.ctx())
        handler.handle(label, ch)
    handler.flush()
    if countErr:
        return handler.segmented, handler.marked, handler.labeled, model.err
    else:
        return handler.segmented, handler.marked, handler.labeled

class Model:
    def __init__(self, result):
        data  = []
        labels = []
        for line in re.split(patnl, result):
            segs = re.split(patsp, line)
            if len(segs) == 2:
               data.append(segs[0])
               labels.append(segs[1])
        self.data      = data
        self.labels    = labels
        self.length    = len(data)
        self.idx       = 0
        self.err       = {}

    def __iter__(self):
        return self

    def next(self):
        idx = self.idx
        if idx < self.length:
            self.idx = idx + 1
            return self.data[idx], self.labels[idx], self.ctx()
        else:
            raise StopIteration

    def label(self, idx):
        if idx < self.length:
            return self.labels[idx]
        else:
            return ''

    def txt(self, idx):
        if idx < self.length:
            return self.data[idx]
        else:
            return ''

    def ctx(self):
        idx   = self.idx
        last  = self.label(idx - 1)
        cur   = self.label(idx)
        next  = self.label(idx + 1)
        nnext = self.label(idx + 2)
        if idx < self.length - 2 and idx > 1:
            return (last, cur, next, nnext)
        else:
            return None

    def excerpt(self):
        idx   = self.idx
        llast = self.txt(idx - 2)
        last  = self.txt(idx - 1)
        cur   = self.txt(idx)
        next  = self.txt(idx + 1)
        nnext = self.txt(idx + 2)
        nnnext= self.txt(idx + 3)
        return ''.join((llast, last, cur, next, nnext, nnnext))

    def fix(self, cur, next, nnext):
        idx = self.idx
        if idx < self.length - 2:
            self.labels[idx] = cur
            self.labels[idx + 1] = next
            self.labels[idx + 2] = nnext

