.. qtils documentation master file, created by
   sphinx-quickstart on Fri Oct  4 20:15:21 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Welcome to Qtils's documentation!
=================================

.. image:: _static/qtils-logo.png

Overview
----------

Qtils - pronounces as `cuteels` - is a syntactic sugar library to make sweet Python coding even sweeter.


Dedication
-------------
This library is dedicated to Pál Hubai, Surfy my programming Master, who thought me how to code and guided me when I was a child.


Quick links
-------------

- :ref:`Contents <toc>` 

- API Reference of the :mod:`qtils` module.

- :ref:`Examples and tutorials <tut_index>`



Features 
----------

- Convenient collections :class:`qtils.collections.qdict`, :class:`qtils.collections.qlist` and :class:`qtils.collections.QEnum`

- Self-formatting object in :class:`qtils.formatting.PrettyObject`

- Two-way formatter/parser for file sizes, for example '5.4 GB') in :class:`qtils.formatting.DataSize`

- Weak reference property decorator :func:`qtils.properties.weakproperty`

- Cached property decorator :func:`qtils.properties.cachedproperty`

- Class logger decorator :func:`qtils.log_utils.logged`

- Common string transformations in :mod:`qtils.string_utils`



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


See more examples and usage in :ref:`examples and tutorials <tut_index>`.



Contribution
-------------------

PullRequests are always welcome.


Full Contents
--------------------------

.. toctree::
   :maxdepth: 2

   tutorial/index
   apidoc/qtils



Indices and tables
--------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
