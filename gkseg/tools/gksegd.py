#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import OptionParser

import gkseg

def main():
    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option("-m", "--model", dest="model",
                      help="the path of the model file")

    (options, args) = parser.parse_args()
    gkseg.api.app.run(options.model)

if __name__ == "__main__":
    main()
