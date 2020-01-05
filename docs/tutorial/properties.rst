
.. _tut_properties:

=======================
Property decorators
=======================


.. _tut_weakproperty:

:func:`weakproperty` usage examples
====================================


What is a weakproperty?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When a python variable is assigned to an ``object`` in python, the reference count of ``object`` is 
increased by 1. When an object's reference count reaches zero, the python runtime will free the object. 
Freeing an object means calling it's destructor method ``__del__``, and freeing the memory used by the 
object. An object's reference count (or refcount) can be queried using the built-in
function :py:func:`sys.getrefcount`.

In cases when there is a circular reference, neither the destructor will be called nor memory will be released. A circular reference is when
object A refers to object B, and object B refers to object A. For example:


.. code-block:: python


    >>> class MyObject(object):
    ...     def __del__(self):
    ...         print( self, "__del__ called")
    ...
    >>> a = MyObject()
    >>> 
    # if we delete variable `a`, the object will be released
    >>> del a
    <__main__.MyObject object at ...> __del__ called
    >>> a = MyObject()
    >>> b = MyObject()
    >>>
    # We refer object `b` from object `a`
    >>> a.b = b
    >>>
    # And we refer object `a` from object `b`
    >>> b.a = a
    >>>
    # We remove both objects
    >>> del a
    >>> del b
    >>>
    # No destructor was called! Our objects are still in the memory.
    # We can confirm by executing the garbage collection explicitly
    >>> import gc
    >>> gc.collect()
    <__main__.MyObject object at ...> __del__ called
    <__main__.MyObject object at ...> __del__ called
    ...



It practice, these objects will be deleted eventually because there is a garbage collector in python, and it will 
find and release unused objects. However, the automatic garbage collection will be executed at arbitrary times, 
and that can cause really hard-to-find problems. (Ask the Java developers how happy they are when the JVM starts
doing a full GC cycle and the whole application is blocked for minutes... :) )

The solution is to program with a forward object-ownership scheme (parent always owns child), and use weak references for any back-reference.
A weak reference can refer to an object wihout increasing the refered object's reference count::

    >>> import weakref
    >>>
    >>> a = MyObject()
    >>> b = MyObject()
    >>>
    # We refer object `b` from object `a`
    >>> a.b = b
    >>>
    # And we create a weak reference from object `a` from object `b`
    >>> b.a = weakref.ref(a)
    >>>
    # Let's have a look at the reference
    >>> b.a 
    <weakref at ...; to 'MyObject' at ...>
    >>>

    # Now we attempt to delete object ``a``
    >>> del a
    <__main__.MyObject object at ...> __del__ called
    >>>
    # The destructor was executed, object `a` is now released
    >>>

    # Let's have a look at the reference in object `b`
    >>> b.a
    <weakref at ...; dead>
    >>>
    # The reference object still there, but it's now dead, meaning it's 
    # former target has been released.
    # 
    # Now, `b` object should be released, because `a`, (and the reference
    # to `b` in `a`) is gone released.
    >>> del b
    <__main__.MyObject object at ...> __del__ called



Using the :func:`weakproperty` decorator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This function takes a method as an input and returns a property which will store the
value assigned to it as a :py:class:`weakref.ref` to the value. When accessing the property, 
the referred object is returned.

Using the :func:`weakproperty` decorator:


.. code-block:: python

    >>> from qtils import weakproperty

    >>> class Foo(object):
    ...     @weakproperty
    ...     def bar(self, value): pass
    >>>

is the equivalent of wrapping the weak reference with the following property implementation::

    >>> import weakref

    >>> class Foo(object):
    ...     @property
    ...     def bar(self, value): 
    ...         return self._bar() if self._bar is not None else None
    ...     @bar.setter
    ...     def bar(self, value): 
    ...         if value is not None:
    ...             value = weakref.ref(value)
    ...         self._bar = value
    >>>



Parent-Child example
~~~~~~~~~~~~~~~~~~~~~~

The parent-child scenario is fairly common in frameworks. Think about accessing nodes in a parsed XML tree,
marshaling JSON data to python objects and vice-versa, or registering handlers in a webserver, or a database 
connection and it's cursors, or handlers of a CLI framework, etc.

Sometimes the child needs data from it's parent. In this case, the child object will receive its parent's
pointer and save it in ``self.parent``. This is a circular reference, and will cause these objects not to be
released automatically as we expect.

Consider the following example:

.. code-block:: python

        >>> from qtils import weakproperty
        >>> import sys

        >>> class Parent(object): 
        ...     def __init__(self):
        ...         self.children = []
        ...
        ...     def get_child(self):
        ...         child = Child(self)
        ...         self.children.append(child)
        ...         return child
        ...
        ...     def __del__(self):
        ...         print( self, "__del__ called")

        >>> class Child(object):
        ...     def __init__(self, parent):
        ...         self.parent = parent
        ...
        ...     def __del__(self):
        ...         print( self, "__del__ called")

        >>> parent = Parent()
        >>> original_refcount = sys.getrefcount(parent)
        >>> child = parent.get_child()
        >>>

        # Reference count of parent is now increased by one
        >>> original_refcount + 1 == sys.getrefcount(parent) 
        True
        
        # Let's attempt to free the parent object
        >>> del parent
        >>> 
        # No calls were made to parent.__del__` because it's still 
        # referred by `child.parent`. We free the child...
        >>> del child
        >>>
        # ... and nothing was released because we have created a circular 
        # reference with `child.parent`. We can release these objects
        # only by calling the garbage collection directly (or waiting for
        # it to be executed auto-magically)
        >>> import gc
        >>> gc.collect()
        <__main__.Parent object at ...> __del__ called
        <__main__.Child object at ...> __del__ called
        ...
        >>>


In the second example we use the weakproperty decorator to create the child.parent property.

.. code-block:: python

        >>> from qtils import weakproperty

        >>> class Parent(object): 
        ...     def __init__(self):
        ...         self.children = []
        ...
        ...     def get_child(self):
        ...         child = Child(self)
        ...         self.children.append(child)
        ...         return child
        ...
        ...     def __del__(self):
        ...         print( self, "__del__ called")

        >>> class Child(object):
        ...     def __init__(self, parent):
        ...         self.parent = parent
        ...
        ...     @weakproperty
        ...     def parent(self, value): 
        ...         pass
        ...
        ...     def __del__(self):
        ...         print( self, "__del__ called")

        >>> parent = Parent()
        >>> original_refcount = sys.getrefcount(parent)
        >>> child = parent.get_child()
        >>>
        # Reference count of parent is NOT increased
        >>> original_refcount == sys.getrefcount(parent)
        True
        
        # the property returns the parent object transparently
        >>> child.parent   
        <__main__.Parent object at ...>
        >>>
        # And the weakref object stored in a private variable
        >>> child._parent 
        <weakref at ... to 'Parent' at ...>

        >>>
        # The child is owned by it's parent, removing our `child`
        # variable won't free the Child object.
        >>> del child
        >>>

        # There is only 1 strong reference to the parent: the `parent` 
        # variable, because all the children's references to the parent
        # are weak references. 
        # Removing the `parent` variable will cause the complete object 
        # tree to be released.
        >>> del parent
        <__main__.Parent object at ...> __del__ called
        <__main__.Child object at ...> __del__ called




.. _tut_cachedproperty:

:func:`cachedproperty()` usage examples
=========================================


A property that caches return value of first ``get()``

.. code-block:: python 

    >>> from qtils import cachedproperty

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

See the API reference `here <https://qtils.readthedocs.io/en/latest/apidoc/qtils.properties.html#qtils.properties.cachedproperty>`__.


