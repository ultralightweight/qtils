
.. _tut_formatting:

=========================================================
Data formatting and parsing
=========================================================


.. _tut_prettyobject:


Self-formatting objects using :class:`PrettyObject`
=======================================================


``PrettyObject`` - A self-formatting object to be used with ``print()``
--------------------------------------------------------------------------

Ever been looking for an easy way to ``print`` an object and see it's internal state? Look no further!

.. code-block:: python

    from qtils import PrettyObject


    class MyPrettyObject(PrettyObject):

        __pretty_fields__ = ['foo', 'bar']

        def __init__(self, foo):
            self.foo = foo

        @property
        def bar(self):
            return self.foo*2


    obj = MyPrettyObject('hello')
    print( obj )


You can customize the format of the class and the individual fields too:


.. code-block:: python

    from qtils import PrettyObject


    class MyPrettyObject(PrettyObject):

        __pretty_fields__ = ['foo', 'bar']

        def __init__(self, foo):
            self.foo = foo

        @property
        def bar(self):
            return foo*2


    obj1 = MyPrettyObject('hello')
    print( obj1 )



Creating table-like formatting
--------------------------------

Creating table-like formatting using tab ``\\t`` as field separator and fixed width fields.


.. code-block:: python
    
    >>> from qtils import PrettyObject, PRETTY_FORMAT

    >>> class MathConstant(PrettyObject):
    ...     __pretty_format__ = PRETTY_FORMAT.MINIMAL
    ...     __pretty_field_separator__ = "    " # should be a tab but it fails in doctest
    ...     __pretty_fields__ = [
    ...         "name!r:<23",
    ...         "symbol!s:<5",
    ...         "value:>10.6f",
    ...     ]
    ...     def __init__(self, name, symbol, value):
    ...         self.name = name
    ...         self.symbol = symbol
    ...         self.value = value
    ...
    >>> math_constants = [
    ...     MathConstant("Archimedes constant", "π", 3.1415926535),
    ...     MathConstant("Euler's number", "e", 2.7182818284),
    ...     MathConstant("Pythagoras constant", "√2", 1.414213562373095),
    ... ]
    >>> for mc in math_constants:
    ...     print(mc)
    <MathConstant name='Archimedes constant'      symbol=π        value=  3.141593>
    <MathConstant name="Euler's number"           symbol=e        value=  2.718282>
    <MathConstant name='Pythagoras constant'      symbol=√2       value=  1.414214>


tabs:
    
                    



.. _tut_datasize:

Formatting and parsing file sizes using :class:`DataSize`
============================================================

Integer object representing data size with two-way conversion ability.

It stores the data size in bytes as int. It can display the value in different
units. By default it uses the most suitable unit automatically. This behaviour
can be changed by calling the :meth:`DataSize.format` directly, or by changing
the default unit in the ``DEFAULT_UNIT`` class attribute.

This class supports different systems of units. It supports the ``BINARY``
system in which a magnitude is ``2**10=1024`` bytes, and the ``METRIC`` system in which
a magnitude is ``10**3=1000`` bytes. By default it uses the ``METRIC`` system. Read more
about the topic in the
`Units of information Wikipedia article <https://en.wikipedia.org/wiki/Units_of_information>`_.



Pretty printing data size values with automatic unit and
precision detection:

.. code-block:: python

    >>> from qtils import DataSize

    >>> print(DataSize(123000))
    123 k
    >>> print(DataSize(123456000))
    123.5 M
    >>> print(DataSize(23*10**8))
    2.30 G
    >>> print(DataSize(1000**8))
    1.00 Y


Parsing data sizes from strings using the ``METRIC`` unit system (default
behaviour):

.. code-block:: python

    >>> DataSize('256')
    256
    >>> DataSize('1.45 megabytes')
    1450000
    >>> DataSize('23.3G')
    23300000000
    >>> DataSize('1 T')
    1000000000000
    >>> DataSize('1,123,456.789 MB')
    1123456789000


Parsing data sizes using the ``BINARY`` unit system:

.. code-block:: python

    >>> from qtils import DATA_UNIT_SYSTEM

    >>> DataSize('1.45 mebibytes')
    1520435
    >>> DataSize('23.3gib')
    25018184499
    >>> DataSize('1 T', system=DATA_UNIT_SYSTEM.BINARY)
    1099511627776
    >>> DataSize('1,123,456.789 MB', system=0)
    1178029825982


Comparison of the ``BINARY`` and the ``METRIC`` unit systems:

.. code-block:: python

    >>> binary_1k = DataSize("1 KiB")
    >>> metric_1k = DataSize("1 kB")
    >>> binary_1k
    1024
    >>> metric_1k
    1000
    >>> binary_1k.format(system=DATA_UNIT_SYSTEM.BINARY)
    '1 K'
    >>> metric_1k.format(system=DATA_UNIT_SYSTEM.BINARY)
    '1000 b'


:class:`DataSize` works as a regular ``int``:

.. code-block:: python

    >>> size = DataSize('1 M') + DataSize('500k')
    >>> size
    1500000
    >>> print(size)
    1.5 M
    >>> size * 2.5
    3750000
    >>> print(size * 2.5)
    3.8 M
    >>> size / 3
    500000
    >>> print(size - 500000)
    1.0 M


Throws :py:class:`ValueError` exception if data can not be parsed:

.. code-block:: python

    >>> DataSize('invalid size data')
    Traceback (most recent call last):
    ...
    ValueError: Invalid data size literal: 'invalid size data'



.. _tut_values:


Working with "Not Available" values
=====================================


A value to represent `not available`: ``NA``
------------------------------------------------


What happens if None is actually a meaningful value, but you need to model a situation when even None 
wasn't supplied? I know what you think... why would anybody end up in a situation like that? I agree, but 
unfortunately not every API is under the control of sane people, so we just need to cope with it.


.. code-block:: python

    >>> from qtils import NA
    >>> 
    >>> value = None
    >>> value is NA
    False
    >>> value == True
    False
    >>> value == False
    False
    >>> value = NA
    >>> value is None
    False
    >>> value == NA
    True
    >>> value is NA
    True
    >>> value == True
    False
    >>> value == False
    False
