
.. _tut_formatting:

=========================================================
Data formatting and parsing
=========================================================


.. _tut_prettyobject:


Self-formatting objects using :class:`PrettyObject`
=======================================================


``PrettyObject`` - A self-formatting object to be used with ``print()``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
