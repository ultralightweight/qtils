
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




.. _tut_values:

Working with values
======================


A value to represent `not available`: ``NA``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
