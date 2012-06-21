#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ctypes import *
from datetime import datetime

import codecs
import os
import os.path as path
import threading

import gkseg.seg.reader as reader

wapiti = path.join('wapiti', 'libwapiti.so')
cdll.LoadLibrary(wapiti)
libwapiti = CDLL(wapiti)
libwapiti.label_init.argtypes = [c_char_p]
libwapiti.label_init.restype = c_void_p
libwapiti.label_paths.argtypes = [c_int]
libwapiti.label_paths.restype = c_void_p
libwapiti.label_in.argtypes = [c_int, c_char_p]
libwapiti.label_in.restype = c_void_p
libwapiti.label_do.argtypes = [c_int]
libwapiti.label_do.restype = c_void_p
libwapiti.label_out.argtypes = [c_int, c_char_p]
libwapiti.label_out.restype = c_void_p
libwapiti.label_free.argtypes = [c_int]
libwapiti.label_free.restype = c_void_p

def init(modelpath):
    if modelpath == None:
        modelpath = 'data/model.txt'
    libwapiti.label_init(modelpath)

def seg(text, countErr=False):
    pid = os.getpid()
    tid = threading.current_thread().ident
    msd = datetime.now().microsecond
    key = hash(hash(pid) + hash(tid) + hash(msd))

    text = codecs.encode('\n'.join(text), 'utf-8')
    strin  = create_string_buffer(text)
    strout = create_string_buffer('\000' * (2 * len(text)))

    result = ''
    try:
        libwapiti.label_paths(key)
        libwapiti.label_in(key, strin)
        libwapiti.label_do(key)
        libwapiti.label_out(key, strout)
        libwapiti.label_free(key)
        result = codecs.decode(strout.value, 'utf-8')
    except BaseException as err:
        print 'err: %s'%str(err)

    return reader.read(result, countErr)

def destroy():
    libwapiti.label_destroy()
