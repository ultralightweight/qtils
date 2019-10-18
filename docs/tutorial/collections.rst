

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

Because :class:`qdict` uses the attribute access to allow access to items, the access to actual 
attributes becomes quite tricky and can result in unexpected behaviour.

This problem is not encoutered during normal use. However, if a new class is to be created to 
inhert from qdict, unexpected things will happen.

 Consider the following example:

.. code-block:: python
    
    # We create a new class based on qdict and declare a class attribute
    # called `a`, a public instance attribute called `b` and a private instance attribute
    # called `_c`

    >>> class MyDict(qdict):
    ...     a = 'initial value'
    ...     def __init__(self, a, b, c):
    ...         # we attempt to overwrite the class attribute to make it an instance attribute
    ...         self.a = a
    ...         # we attempt to store data in self as an instance attribute
    ...         self.b = b
    ...         # we attempt to store data in a private instance variable
    ...         self._c = c
    ...
    >>> md = MyDict('foo', 'bar', 42)

    # all 'attributes' became values in our dictionary
    >>> md                  
    {'a': 'foo', 'b': 'bar', '_c': 42}
    
    # but when we try to read `a` it returns the class attribute
    >>> md.a                
    'initial value'
    
    # when we set 'a' as an instance attribute
    >>> md.a = 'apple'      
    
    # but we have changed the value in the dictionary
    >>> md                  
    {'a': 'apple', 'b': 'bar', '_c': 42}
    >>>
    
    # but accessing it still returns the class attribute
    >>> md.a                
    'initial value'
    
    # reading 'a' with the dictionary API returns the value
    >>> md['a']             
    'apple'
    
    # `b` seems to be working, but it is NOT an attribute
    >>> md.b                
    'bar'
    
    # it is a value in the dictionary
    >>> md['b']             
    'bar'
    
    # when we try to set 'b'
    >>> md.b = 'cat'        
    
    # we are changing the value in the dictionary
    >>> md['b']             
    'cat'
    
    # Same thing applies to `_c`, it seems to be working, 
    >>> md._c               
    42
    
    # still, it is a value in the dictionary
    >>> md['_c']            
    42


To handle a scenario like this we have the ``__qdict_allow_attributes__`` attribute. When it's set
to true, it will allow access to class attributes and private instance attributes (name starting with an
underscore). Please note that there is a performance penalyt to this, because every write will have to 
check if the name exists either as a class attribute or within the instances ``__dict__``. This means two
dictionary lookups for every attribute write. 



.. code-block:: python
    
    # We are using the same class as in the previous example.

    >>> class MyDict(qdict):
    ...     __qdict_allow_attributes__ = True
    ...     a = None
    ...     def __init__(self, a, b, c):
    ...         self.a = a
    ...         self.b = b
    ...         self._c = c
    ...
    >>> md = MyDict('foo', 'bar', 42)
    
    # Only `b` ended up in the dictionary, because it's not private.
    >>> md                  
    {'b': 'bar'}
    
    # reading `a` correctly returns value
    >>> md.a                
    'foo'
    
    # when we set 'a' as an instance attribute
    >>> md.a = 'apple'      
    
    # we actually set an instance attribute
    >>> md                  
    {'b': 'bar'}
    
    # accessing correctly returns the value we set
    >>> md.a                
    'apple'
    
    # reading 'a' with the dictionary API raises KeyError
    >>> md['a']             
    Traceback (most recent call last):
    ...
    KeyError: 'a'
    
    # `b` seems to be working, but it's still NOT an attribute
    >>> md.b                
    'bar'
    
    # it is a value in the dictionary
    >>> md['b']             
    'bar'
    
    # `_c` works as expected
    >>> md._c               
    42
    
    # and it is also NOT in the dictionary
    >>> md['_c']            
    Traceback (most recent call last):
    ...
    KeyError: '_c'




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

The main function of ObjectDict is 

Registering a function with :meth:`ObjectDict.register` decorator:
Registering a class with :meth:`ObjectDict.register` decorator:


.. code-block:: python


    >>> my_dir = ObjectDict()

    >>> @my_dir.register
    ... def foo(self): pass

    >>> my_dir['foo']
    <function foo at ...>


    >>> @my_dir.register
    ... class Bar(object): pass

    >>> my_dir['Bar']
    <class '__main__.Bar'>



.. _tut_qenum:


:class:`QEnum` usage examples
================================


An enhanced ``QEnum`` that can return it's possible values


