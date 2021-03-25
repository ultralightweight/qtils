..  This file is part of Ulra Light Weight Qtils.

    Ulra Light Weight Qtils is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    Ulra Light Weight Qtils is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with Ulra Light Weight Qtils. If not, see <https://www.gnu.org/licenses/lgpl>.


.. _index:

Welcome to Qtils 0.10.4 documentation!
=======================================

.. image:: _static/qtils-logo.png

Overview
----------

Qtils - pronounced as cutieels - is a syntactic sugar library to make sweet Python coding even sweeter.


Dedication
-------------
This library is dedicated to **Pál Hubai, Surfy**, my programming Master who spent countless hours answering
my questions, providing code examples, and guiding me towards the right approach when I was learning programming
as a child.



Quick links
-------------

- :ref:`tut_index`

- :ref:`apidoc_index`

- :ref:`Full Contents <toc>` 

- :ref:`migration_from_sutils`


Features 
----------

- Convenient collections :class:`qdict <qtils.collections.qdict>`, :class:`qlist <qtils.collections.qlist>` and :class:`QEnum <qtils.collections.QEnum>`

- Self-formatting object in :class:`PrettyObject <qtils.formatting.PrettyObject>`

- Two-way formatter/parser for file sizes, for example '5.4 GB' in :class:`DataSize <qtils.formatting.DataSize>`

- Weak reference property decorator :func:`weakproperty <qtils.properties.weakproperty>`

- Cached property decorator :func:`cachedproperty <qtils.properties.cachedproperty>`

- Class logger decorator :func:`logged <qtils.log_utils.logged>`

- Common string transformations in :mod:`qtils.string_utils`



Installation 
--------------


.. code-block:: bash

    $ pip install qtils



Examples
---------


.. code-block:: python

    >>> from qtils import *


    >>> d = qdict()
    >>> d.hello = "world"
    >>> d.hello
    'world'


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


    >>> print(DataSize(123000))
    123 k
    >>> DataSize('1.45 megabytes')
    1450000


See more examples and usage in :ref:`examples and tutorials <tut_index>`.



Contribution
-------------------

- Pull requests are always welcome!
- Please have a look at the :ref:`developer guide <devguide>` to get started.




Full Contents
--------------------------

.. _toc:


.. toctree::
   :maxdepth: 2

   tutorial/index
   devguide
   apidoc/index
   migration




Indices and tables
--------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
