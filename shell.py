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

# class Foo(PrettyObject):
#     __pretty_fields__ = ['a', 'b']
#     def __init__(self, a, b, c):
#         self.a = a
#         self.b = b
#         self.c = c
# foo = Foo('hello world', 42.123456, [1,2,3])
# print(foo)


# class MyObject(PrettyObject):
#     # __pretty_format__ = PRETTY_FORMAT.BRIEF
#     # __pretty_fields__ = [
#     #     'hello',
#     #     'answer',
#     # ]
#     def __init__(self, hello, answer):
#         self.hello = hello
#         self.answer = answer
# obj = MyObject('world', 42)
# print(obj)


class MyObject(PrettyObject):
    __pretty_fields__ = [
        ":.",
    ]
    def __init__(self, a): self.a = a
obj = MyObject('test')
print(obj)


