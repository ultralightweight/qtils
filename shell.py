# encoding: utf-8
# author: Daniel Kovacs <mondomhogynincsen@gmail.com>
# license: MIT <https://opensource.org/licenses/MIT>
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


# class MyObject(PrettyObject):
#     __pretty_fields__ = [
#         ":.",
#     ]
#     def __init__(self, a): self.a = a
# obj = MyObject('test')
# print(obj)


def foo(**kwargs):
    kwargs = qdict(kwargs)
    kwargs.arg1
    kwargs.arg2 


def foo():
    pass

import json

data = qdict(bar='hello', foo=qdict(cat='grumpy', bunny="bugs"), answer=42)

print( json.dumps(data) )


api_result = '{"bar": "hello", "foo": {"answer": 42}, [ {"name": "cat grumpy", "meme_score": }, "bunny": "bugs"}, }'

api_url = "https://api.imgflip.com/get_memes"

api_response = """
{ 
  "success":true,
  "data":{ 
    "memes":[ 
      { 
        "id":"112126428",
        "name":"Distracted Boyfriend",
        "url":"https://i.imgflip.com/1ur9b0.jpg",
        "width":1200,
        "height":800,
        "box_count":3
      },
      { 
        "id":"181913649",
        "name":"Drake Hotline Bling",
        "url":"https://i.imgflip.com/30b1gx.jpg",
        "width":1200,
        "height":1200,
        "box_count":2
      },
      { 
        "id":"87743020",
        "name":"Two Buttons",
        "url":"https://i.imgflip.com/1g8my4.jpg",
        "width":600,
        "height":908,
        "box_count":2
      }
    ]
  }
}"""


api_response = """
{ 
  "success":true,
  "memes":[ 
    { 
      "name":"Distracted Boyfriend",
      "url":"https://i.imgflip.com/1ur9b0.jpg"
    },
    { 
      "name":"Drake Hotline Bling",
      "url":"https://i.imgflip.com/30b1gx.jpg"
    },
    { 
      "name":"Two Buttons",
      "url":"https://i.imgflip.com/1g8my4.jpg"
    }
  ]
}
"""

api_data = qdict.convert(json.loads(api_response))

if api_data.success:
    for meme in api_data.memes:
        print( meme.name, meme.url )





