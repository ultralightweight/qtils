# encoding: utf-8
# author: Daniel Kovacs <mondomhogynincsen@gmail.com>
# licence: MIT <https://opensource.org/licenses/MIT>
# file: shell.py
# purpose: interactive demo
# version: 1.0


# ---------------------------------------------------------------------------------------
# imports
# ---------------------------------------------------------------------------------------

import sys, os
from pprint import pprint
pp = pprint


# ---------------------------------------------------------------------------------------
# package specific imports
# ---------------------------------------------------------------------------------------

from qtils import *


# ---------------------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------------------

# setup your shell here
# use print() to print help to users


class SomeClass(object): 
    def __del__(self):
        print("SomeClass instance freed")

class Foo(object):
    @weakproperty
    def bar(self, value): pass

value = SomeClass()
foo = Foo()
foo.bar = value
foo.bar
del value
