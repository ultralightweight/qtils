

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

=========
Overview
=========

Qtils - pronounced as cutieels - is a syntactic sugar library to make sweet Python coding even sweeter.


Dedication
------------

This library is dedicated to **Pál Hubai, Surfy**, my programming Master who spent countless hours answering
my questions, providing code examples, and guiding me towards the right approach when I was learning programming
as a child.


Features 
------------

- Convenient collections `qdict <https://qtils.readthedocs.io/en/latest/apidoc/qtils.html#qtils.collections.qdict>`_, `qlist <https://qtils.readthedocs.io/en/latest/apidoc/qtils.html#qtils.collections.qlist>`_ and `QEnum <https://qtils.readthedocs.io/en/latest/apidoc/qtils.html#qtils.collections.QEnum>`_

- Self-formatting object in `PrettyObject <https://qtils.readthedocs.io/en/latest/apidoc/qtils.html#qtils.formatting.PrettyObject>`_

- Two-way formatter/parser for file sizes, for example '5.4 GB', in `DataSize <https://qtils.readthedocs.io/en/latest/apidoc/qtils.html#qtils.formatting.DataSize>`_

- Weak reference property decorator `weakproperty <https://qtils.readthedocs.io/en/latest/apidoc/qtils.html#qtils.properties.weakproperty>`_

- Cached property decorator `cachedproperty <https://qtils.readthedocs.io/en/latest/apidoc/qtils.html#qtils.properties.cachedproperty>`_

- Class logger decorator `logged <https://qtils.readthedocs.io/en/latest/apidoc/qtils.html#qtils.log_utils.logged>`_

- Common string transformations in `qtils.string_utils <https://qtils.readthedocs.io/en/latest/apidoc/qtils.html#module-qtils.string_utils>`_



Resources
------------

- Documentation is `available online on ReadTheDocs.io <https://qtils.readthedocs.io/en/latest/>`_

- See short examples below
- See more examples  in the `usage examples and tutorials section <https://qtils.readthedocs.io/en/latest/tutorial/index.html>`_

- Sources are available on `GitHub <https://github.com/ultralightweight/qtils>`_
  
- Installer is available on `PyPI <https://pypi.org/project/qtils/>`_

- Migrating from ``sutils``? See the `sutils migration guide <https://qtils.readthedocs.io/en/latest/migration.html>`_.


=======
Usage
=======


Installation 
--------------


Installing the latest release from PyPI using ``pip``:

.. code-block:: bash

    $ pip install qtils


Installing the latest release from PyPI and saving it to ``requirements.txt`` using ``pip``:

.. code-block:: bash

    $ pip install -s requirements.txt qtils



Installing the developer version:

.. code-block:: bash

    $ pip install -e https://github.com/ultralightweight/qtils.git#dev



.. _short_examples:

Examples
-----------


Attribute dictionary
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> from qtils import *

    >>> d = qdict(hello = "world")
    >>> d.hello
    'world'
    >>> d.answer = 42
    >>> d['answer']
    42

See more examples in the `qdict tutorial <https://qtils.readthedocs.io/en/latest/tutorial/collections.html#qdict-usage-examples>`_.



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


See more examples in the `PrettyObject tutorial <https://qtils.readthedocs.io/en/latest/tutorial/formatting.html#self-formatting-objects-using-prettyobject>`_.


Cached property
~~~~~~~~~~~~~~~~~~

.. code-block:: python 

    >>> class DeepThought(object):
    ...     @cachedproperty
    ...     def answer_to_life_the_universe_and_everything(self):
    ...         print('Deep Thought is thinking')
    ...         # Deep Thought: Spends a period of 7.5 million years
    ...         # calculating the answer
    ...         return 42
    ...
    >>> deep_thougth = DeepThought()
    >>> deep_thougth.answer_to_life_the_universe_and_everything     # first call, getter is called
    Deep Thought is thinking
    42
    >>> deep_thougth.answer_to_life_the_universe_and_everything     # second call, getter is not called
    42
    >>> del deep_thougth.answer_to_life_the_universe_and_everything # removing cached value
    >>> deep_thougth.answer_to_life_the_universe_and_everything     # getter is called again
    Deep Thought is thinking
    42

See more examples in the `properties module tutorial <https://qtils.readthedocs.io/en/latest/tutorial/properties.html#cachedproperty-usage-examples>`_.


Formatting and parsing file sizes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> print(DataSize(123000))
    123 k
    >>> DataSize('1.45 megabytes')
    1450000
    >>> DataSize('1T').format(unit="k", number_format="{:,.0f} {}")
    '1,000,000,000 k'


See more examples in the `formatting module tutorial <https://qtils.readthedocs.io/en/latest/tutorial/formatting.html#formatting-and-parsing-file-sizes-using-datasize>`_.


Dynamic module exports
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> from qtils import qlist

    >>> __all__ = qlist()

    >>> @__all__.register
    ... class Foo(object):
    ...     pass


See more examples in the `qlist tutorial <https://qtils.readthedocs.io/en/latest/tutorial/collections.html#qlist-usage-examples>`_.



Adding a class-private logger
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> @logged
    ... class LoggedFoo():
    ...     def __init__(self):
    ...         self.__logger.info("Hello World from Foo!")
    ...


See more examples in the `logging module tutorial <https://qtils.readthedocs.io/en/latest/tutorial/logging.html>`_.


=============
Contribution
=============

- Pull requests are more than welcome! 

- See the `Developer's Guide <https://qtils.readthedocs.io/en/latest/devguide.html>`_ on how to get started with qtils development. 


========
Licence
========

This library is available under `GNU Lesser General Public Licence v3 <https://www.gnu.org/licenses/lgpl>`_.






