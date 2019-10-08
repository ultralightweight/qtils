

.. _tut_collections:

==========================
Working with collections
==========================


.. _tut_qdict:

:class:`qdict` usage examples
===============================


Using `dot notation` to access dictionary elements
----------------------------------------------------

for reading and writing dictionary elements


.. code-block:: python

    >>> from qtils import qdict

    >>> d = qdict(foo="hello", bar="world")
    >>> d.foo = 1234
    >>> d
    {'foo': 1234, 'bar': 'world'}
    >>> d.bar
    'world'




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




:class:`ObjectDict` usage examples
===================================




:class:`QEnum` usage examples
================================


An enhanced ``QEnum`` that can return it's possible values


