

.. _tut_collections:

==========================
Working with collections
==========================


.. _tut_qdict:

:class:`qdict` usage examples
===============================


Using `dot notation` to access dictionary elements
----------------------------------------------------

Qdict allows reading and writing dictionary elements as if they were attributes.


.. code-block:: python

    >>> from qtils import *

    >>> d = qdict(hello = "world")
    >>> d.hello
    'world'
    >>> d.answer = 42
    >>> d['answer']
    42
    >>> d
    {'hello': 'world', 'answer': 42}



Dealing with keyword argument dictionaries
-----------------------------------------------

Accessing 

.. code-block:: python

    >>> from qtils import *
    
    >>> def foo(**kwargs): pass
    


Working with complex data from API endpoints in JSON/YAML
---------------------------------------------------------------

Data from an API endpoint can be marshalled into a ``qdict`` object tree, allowing convenient access 
to objects within the response.

Let's load up some memes from imgflip using and endpoint, and list what we got.
(The response shown in the example below was altered for readibility reasons)


.. code-block:: python

    >>> import json
    >>> from qtils import *

    # Loading up memes from https://api.imgflip.com/get_memes 
    # with requests to api_response variable with something like:
    # api_response = requests.get(https://api.imgflip.com/get_memes).text
    # The api_response will look something like this:
    >>> api_response = """  
    ... { 
    ...   "success":true,
    ...   "memes":[ 
    ...     { 
    ...       "name":"Distracted Boyfriend",
    ...       "url":"https://i.imgflip.com/1ur9b0.jpg"
    ...     },
    ...     { 
    ...       "name":"Drake Hotline Bling",
    ...       "url":"https://i.imgflip.com/30b1gx.jpg"
    ...     },
    ...     { 
    ...       "name":"Two Buttons",
    ...       "url":"https://i.imgflip.com/1g8my4.jpg"
    ...     }
    ...   ]
    ... }
    ... """
    
    # Loading the data into a qdict tree.
    >>> api_data = qdict.convert(json.loads(api_response))
    
    # The data from the API can be used as any other python object
    >>> if api_data.success:
    ...     for meme in api_data.memes:
    ...         print( "{:<30}{}".format( meme.name, meme.url ) )
    Distracted Boyfriend          https://i.imgflip.com/1ur9b0.jpg
    Drake Hotline Bling           https://i.imgflip.com/30b1gx.jpg
    Two Buttons                   https://i.imgflip.com/1g8my4.jpg
    




Caveats 
----------

Keeping qdict subclass private variables accessible.


.. code-block:: python

    >>> class MyDict(qdict):
    ...     a = 'initial value'
    ...     def __init__(self, a, b):
    ...         self.a = a
    ...         self._b = b
    ...
    >>> md = MyDict('foo', 42)
    >>> md
    {'a': 'foo'}
    >>> md.a          # returns the class attribute
    'initial value'
    >>> md._b
    42
    >>> md.a = 'bar'
    >>> md
    {'a': 'bar'}
    >>> md.a          # still returns the class attribute
    'initial value'

    >>> class MyDict(qdict):
    ...     __qdict_allow_attributes__ = True
    ...     a = None
    ...     def __init__(self, a, b):
    ...         self.a = a
    ...         self._b = b
    ...
    >>> md = MyDict('foo', 42)
    >>> md
    {}
    >>> md.a
    'foo'
    >>> md._b
    42
    >>> md.a = 'bar'
    >>> md
    {}
    >>> md.a
    'bar'



.. _tut_qlist:

:class:`qlist` usage examples
================================


Marking objects as public in a module
--------------------------------------

When importing ``*`` from a module, python will import all names which are not private (starting 
with an ``_`` underscore). This behaviour can be controlled by explicitly defining 
what needs to be exported using the :py:ref:`__all__<tut-pkg-import-star>` magic variable. This 
variable must be a list of strings. Each string must match an existing object's name in the module.

By convention, the ``__all__`` keyword must sit in the beginning of the module. It is sometimes quite
cumbersome to keep it sync with the names of the classes and functions in the module that are
defined later. This is especially true during early development stages. 

Wouldn't it be nice if there was a way to simply mark objects which we want to export form a module? 
The qlist class has a :meth:`qlist.register` method which can be used as a decorator on functions 
and classes. It will add the object's ``__name__`` to itself, and return the object unchanged.

Consider the following example:


.. code-block:: python

    >>> from qtils import qlist

    >>> __all__ = qlist()

    >>> @__all__.register
    ... class Foo(object):
    ...     pass

    >>> # Some class we don't want in the convenience API
    >>> class ANotPrivateButRarelyUsedClass(): pass

    >>> @__all__.register
    ... def bar():
    ...     pass
    
    >>> print(__all__)
    ['Foo', 'bar']



.. _tut_object_dict:

:class:`ObjectDict` usage examples
===================================



.. _tut_qenum:


:class:`QEnum` usage examples
================================


An enhanced ``QEnum`` that can return it's possible values


