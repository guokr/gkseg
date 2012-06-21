======================================================
GkSeg: yet another Chinese word segmentation package
======================================================

GkSeg is a Chinese word segmentation package shipped by Guokr.com.
It is based on character-based tagging heuristics and CRF algorithm.

Currently it only support Linux platform.

Features
----------

- Precise: > 94%
- Scope: modern Chinese text, and even classic Chinese text(文言文)
- Terms auto-extraction: It can extract important terms from the text
- No dictionaries: See the section for character-based tagging heuristics
- Performance is good: 4 times slower than mmseg, but we support more features
- Training tool for the CRF model is also shipped in the same package

Character-based tagging heuristics
------------------------------------

Character-based tagging heuristics is invented by N. Xue and others, and
published at SIGHAN 2002 [Xue et al., 2002]

The basic idea is to mark each character in a sentence with its kind:

- b: begining character of a word
- m: middle character of a word
- e: end character of a word
- s: single character to form a word

And then using the marked corpus to train the segmentation program.

At conceptual level, we can treat its ability for segmenting from the inner
pattern of Chinese language.

Interestingly, when we use the tool to segment classic Chinese text, it achieved
a good performance. That is to say, the inner pattern of Chinese language is not
vary greatly during the time.

CRF algorithm
---------------

Conditional random fields
( from http://en.wikipedia.org/wiki/Conditional_random_field )

  Conditional random fields (CRFs) are a class of statistical modelling method
  often applied in pattern recognition and machine learning, where they are used
  for structured prediction. Whereas an ordinary classifier predicts a label for
  a single sample without regard to "neighboring" samples, a CRF can take
  context  into account; e.g., the linear chain CRF popular in natural language
  processing predicts sequences of labels for sequences of input samples.

We use wapiti package from LIMSI-CNRS, it is a very neat CRF package
( http://wapiti.limsi.fr/ )

We changed wapiti package a little by our requirements.

Installation
--------------

Please follow below steps:

  git clone git://github.com/guokr/gkseg.git gkseg

  cd gkseg/wapiti

  make

Now it is ready, you can use the tools provided by this package directly.

Usage for the tools
---------------------

All the tools located under the bin directory

gkseg: segment a text into words

- gkseg <text>

gksegd: start a webserver to segment words by restful api

- gksegd

gksegt: trainning the tool

- gksegt add <basedir> <aspect> <trainfile>
- gksegt train <trainfile> <modelfile>

Using the API
---------------

Before using the API, you should intialize the program first, and then perform
the segmentation, and finally destroy the program.

  import gkseg

  text = '话说天下大势，分久必合，合久必分'.decode('utf-8')

  gkseg.init()

  print gkseg.seg(text) #segment the sentence into a list of words

  print gkseg.term(text) #extract the important words from the sentence

  gkseg.destory()

The training process
-------------------------------

Step 1: prepare the training input

- gksegt add <basedir> <aspect> <trainfile>

Here we have

- <basedir>: The base path of the training corpus
- <aspect>: A specified aspect of the training corpus, see below corpus section
- <trainfile>: The target training file

Step 2: training the input file to get the model

- gksegt train <trainfile> <modelfile>

Here we have

- <trainfile>: The training file as input
- <modelfile>: The model file as output

The format of training corpus
-------------------------------



Contributors
--------------

- Mingli Yuan (mountain at github)
- Rui Wang (isnowfy at github)

License
---------

- MIT license for the main part of the project
- wapiti is under its own license
- uthash is under BSD license

