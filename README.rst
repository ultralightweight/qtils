

.. image:: https://qtils.readthedocs.io/en/latest/_images/qtils-logo.png

------

.. image:: https://img.shields.io/github/v/tag/ultralightweight/qtils  
    :target: http://github.com/ultralightweight/qtils
    :alt: GitHub tag (latest SemVer)

.. image:: https://travis-ci.org/ultralightweight/qtils.svg?branch=master
    :target: https://travis-ci.org/ultralightweight/qtils
    :alt: Travis CI build status

.. image:: https://coveralls.io/repos/github/ultralightweight/qtils/badge.svg?branch=master
    :target: https://coveralls.io/github/ultralightweight/qtils?branch=master
    :alt: Code Coverage

.. image:: https://readthedocs.org/projects/qtils/badge/?version=latest  
    :target: https://qtils.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://img.shields.io/pypi/v/qtils
    :target: https://pypi.org/project/qtils/
    :alt: PyPI

.. image:: https://img.shields.io/github/issues-raw/ultralightweight/qtils
    :target: https://github.com/ultralightweight/qtils/issues
    :alt: GitHub issues


Overview
----------

Qtils - pronounces as `cuteels` - is a syntactic sugar library to make sweet Python coding even sweeter.


Dedication
-------------
This library is dedicated to **Pál Hubai, Surfy**, my programming Master who spent countless hours answering
my questions, providing code examples, and guiding me towards the right approach when I was learning programming
as a child. *Thank you!*



Documentation
-------------

- Documentation is available at https://qtils.readthedocs.io/en/latest/

- See examples and usage in `examples and tutorials <https://qtils.readthedocs.io/en/latest/tutorial/index.html>`_


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

Qtils is available in PyPI:

.. code-block:: bash

    $ pip install qtils



Examples
-------------------


Attribute dictionary
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> from qtils import *

    >>> d = qdict()
    >>> d.hello = "world"
    >>> d.hello
    'world'
    >>> d.answer = 42
    >>> d['answer']
    42

    
Objects with self-formatting capability
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> class MyObject(PrettyObject):
    ...     __pretty_fields__ = [
    ...         'hello',
    ...         'answer',
    ...     ]
    ...     def __init__(self, hello, answer):
    ...         self.hello = hello
    ...         self.answer = answer
    >>> obj = MyObject('world', 42)
    >>> print(obj)
    <__main__.MyObject object at ... hello='world', answer=42>


Cached property
~~~~~~~~~~~~~~~~~~

.. code-block:: python 

    >>> class Foo(object):
    ...     @cachedproperty
    ...     def bar(self):
    ...         # doing some super computation-intensive thing here
    ...         print('getter called')
    ...         return "hello world"
    ...
    >>> obj = Foo()
    >>> obj.bar     # first call, getter is called
    getter called
    'hello world'
    >>> obj.bar     # second call, getter is not called
    'hello world'
    >>> del obj.bar # removing cached value
    >>> obj.bar     # getter is called again
    getter called
    'hello world'


Formatting and parsing file sizes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> print(DataSize(123000))
    123 k
    >>> DataSize('1.45 megabytes')
    1450000
    >>> DataSize('1T').format(unit="k", number_format="{:,.0f} {}")
    '1,000,000,000 k'



Adding a class-private logger
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> @logged
    ... class LoggedFoo():
    ...     def __init__(self):
    ...         self.__logger.info("Hello World from Foo!")
    ...


See more examples and usage in `examples and tutorials <https://qtils.readthedocs.io/en/latest/tutorial/index.html>`_.


Contribution
--------------

Pull requests are always welcome.









