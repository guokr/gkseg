from flask import Flask
from flask import request

import codecs
import json

import gkseg

app = Flask(__name__)
app.debug = True

def run(model='data/model.txt'):
    gkseg.init(model)

@app.route('/segmt', methods=['POST'])
def segmt():
    return json.dumps(gkseg.seg(codecs.decode(request.data, 'utf-8')))

@app.route('/term', methods=['POST'])
def term():
    return json.dumps(gkseg.term(codecs.decode(request.data, 'utf-8')))

if __name__ == '__main__':
    run(model)
