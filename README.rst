

.. image:: https://qtils.readthedocs.io/en/latest/_images/qtils-logo.png

------

.. image:: https://img.shields.io/github/v/tag/ultralightweight/qtils  
    :alt: GitHub tag (latest SemVer)

.. image:: https://travis-ci.org/ultralightweight/qtils.svg?branch=master
    :target: https://travis-ci.org/ultralightweight/qtils
    :alt: Travis CI build status

.. image:: https://coveralls.io/repos/github/ultralightweight/qtils/badge.svg?branch=master
    :target: https://coveralls.io/github/ultralightweight/qtils?branch=master

.. image:: https://readthedocs.org/projects/qtils/badge/?version=latest  
    :target: https://qtils.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://img.shields.io/pypi/v/qtils  
    :target: https://pypi.org/project/qtils/
    :alt: PyPI

.. image:: https://img.shields.io/github/issues-raw/ultralightweight/qtils
    :alt: GitHub issues


Overview
----------

Qtils - pronounces as `cuteels` - is a syntactic sugar library to make sweet Python coding even sweeter.


Dedication
-------------
This library is dedicated to Pál Hubai a.k.a. Surfy my programming Master, who thought me how to code when I was a child.


Documentation
-------------

Documentation is available at https://qtils.readthedocs.io/en/latest/


Features 
----------

- Convenient collections `qdict <https://qtils.readthedocs.io/en/latest/apidoc/qtils.html#qtils.collections.qdict>`_, `qlist <https://qtils.readthedocs.io/en/latest/apidoc/qtils.html#qtils.collections.qlist>`_ and `QEnum <https://qtils.readthedocs.io/en/latest/apidoc/qtils.html#qtils.collections.QEnum>`_

- Self-formatting object in `PrettyObject <https://qtils.readthedocs.io/en/latest/apidoc/qtils.html#qtils.formatting.PrettyObject>`_

- Two-way formatter/parser for file sizes, for example '5.4 GB', in `DataSize <https://qtils.readthedocs.io/en/latest/apidoc/qtils.html#qtils.formatting.DataSize>`_

- Weak reference property decorator `weakproperty <https://qtils.readthedocs.io/en/latest/apidoc/qtils.html#qtils.properties.weakproperty>`_

- Cached property decorator `cachedproperty <https://qtils.readthedocs.io/en/latest/apidoc/qtils.html#qtils.properties.cachedproperty>`_

- Class logger decorator `logged <https://qtils.readthedocs.io/en/latest/apidoc/qtils.html#qtils.log_utils.logged>`_

- Common string transformations in `qtils.string_utils <https://qtils.readthedocs.io/en/latest/apidoc/qtils.html#module-qtils.string_utils>`_



Installation 
--------------


.. code-block:: bash

    $ pip install qtils



Quick Examples
-------------------


.. code-block:: python

    >>> from qtils import *


    >>> d = qdict()
    >>> d.hello = "world"
    >>> d.hello
    'world'


    >>> class MyObject(PrettyObject):
    ...     __pretty_format__ = PRETTY_FORMAT.BRIEF
    ...     __pretty_fields__ = [
    ...         'hello',
    ...         'answer',
    ...     ]
    ...     def __init__(self, hello, answer):
    ...         self.hello = hello
    ...         self.answer = answer
    >>> obj = MyObject('world', 42)
    >>> print(obj)
    <MyObject object at ... hello='world', answer=42>


    >>> print(DataSize(123000))
    123 k
    >>> DataSize('1.45 megabytes')
    1450000


See more examples and usage in `examples and tutorials <https://qtils.readthedocs.io/en/latest/tutorial/index.html>`.

