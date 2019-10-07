
.. _tut_index:

Tutorials
----------



Convenient collections ``qlists()`` and ``qdict()``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Dynamic module level exports using ``qlist``

.. code-block:: python

    from qtils import qlist

    __all__ = qlist()

    @__all__.register
    class Foo(object):
        pass

    @__all__.register
    def bar():
        pass


Convenient `dot notation` for dictionary element get and set


.. code-block:: python

    from qtils import qdict

    >>> d = qdict(foo="hello", bar="world")
    >>> d.foo = 1234
    >>> d
    {'foo': 1234, 'bar': 'world'}
    >>> d.bar
    'world'



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
    True
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



An enhanced ``QEnum`` that can return it's possible values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~





``weakproperty()`` - A property that keeps ``set()`` values as ``weakref.ref()``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



``cachedproperty()`` - A property that caches return value of first ``get()``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



``logged()`` - A class decorator for beautiful class-specific logging
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



Schedulable ``TaskQueue`` for distributing tasks between a pool of workers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




Common string transformations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


