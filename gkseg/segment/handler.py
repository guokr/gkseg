#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Handler:
    def __init__(self):
        self.segmented = []
        self.marked    = []
        self.labeled   = []
        self.word      = ''
        self.nmcnt     = 0
        self.mkcnt     = 0

    def add(self, ch):
        self.word  = self.word + ch
        self.nmcnt = self.nmcnt + 1
    def mark(self, ch):
        self.word  = self.word + ch
        self.mkcnt = self.mkcnt + 1
    def flush(self):
        if self.word != '':
            self.segmented.append(self.word)
            if self.mkcnt > self.nmcnt:
                self.marked.append(self.word)
                self.labeled.append(self.word + '\m')
            else:
                self.labeled.append(self.word)
        self.word  = ''
        self.nmcnt = 0
        self.mkcnt = 0

    def s(self, ch):
        self.flush()
        self.add(ch)
        self.flush()

    def e(self, ch):
        self.add(ch)
        self.flush()

    def b(self, ch):
        self.flush()
        self.add(ch)

    def m(self, ch):
        self.add(ch)

    def S(self, ch):
        self.flush()
        self.mark(ch)
        self.flush()

    def E(self, ch):
        self.mark(ch)
        self.flush()

    def B(self, ch):
        self.flush()
        self.mark(ch)

    def M(self, ch):
        self.mark(ch)

    def handle(self, label, ch):
        if label == 's':
            self.s(ch)
        elif label == 'e':
            self.e(ch)
        elif label == 'b':
            self.b(ch)
        elif label == 'm':
            self.m(ch)
        elif label == 'S':
            self.S(ch)
        elif label == 'E':
            self.E(ch)
        elif label == 'B':
            self.B(ch)
        elif label == 'M':
            self.M(ch)

