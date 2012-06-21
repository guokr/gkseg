#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import OptionParser

import codecs
import gkseg

def main():
    usage = "usage: %prog [options] text"
    parser = OptionParser(usage)
    parser.add_option("-m", "--model", dest="model",
                      help="the path of the model file")

    (options, args) = parser.parse_args()
    if len(args) >= 1:
        gkseg.init(options.model)
        print ' '.join(gkseg.seg(codecs.decode(args[0], 'utf-8')))
    else:
        print 'error: input text should not be empty.'

if __name__ == "__main__":
    main()
