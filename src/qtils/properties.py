# encoding: utf-8
# package: qtils
# author: Daniel Kovacs <github.com/neonihil>
# file-version: 1.0
# licence: LGPL-v3

# -------------------------------------------------------------------------------
# Licence
# -------------------------------------------------------------------------------
# This file is part of Ulra Light Weight Qtils.
#
# Ulra Light Weight Qtils is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# Ulra Light Weight Qtils is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Ulra Light Weight Qtils. If not, see <https://www.gnu.org/licenses/lgpl>.
# -------------------------------------------------------------------------------


"""
Properties module
===================


This module contains enhanced property implementations.



"""


# -------------------------------------------------------------------------------
# imports
# -------------------------------------------------------------------------------

import weakref

from .collections import qlist


# -----------------------------------------------------------------------------
# exports
# -----------------------------------------------------------------------------

__all__ = qlist()


# -----------------------------------------------------------------------------
# @weakproperty
# -----------------------------------------------------------------------------

@__all__.register
def weakproperty(setter):
    """Returns a property that stores values as :py:class:`weakref.Ref()`

    The weakref object is stored as ``'_' + setter.__name__``

    Args:
        setter (function): setter function (can be an empty function)

    Returns:
        returns property instance

    Example:

    >>> import sys
    >>> class SomeClass(object): pass
    >>> class Foo(object):
    ...     @weakproperty
    ...     def bar(self, value): pass
    ...
    >>> some_obj = SomeClass()
    >>> original_refcount = sys.getrefcount(some_obj)
    >>> foo = Foo()
    >>> foo.bar = some_obj  # Reference count should not increase because some_obj is weak referenced.
    >>> original_refcount == sys.getrefcount(some_obj)
    True
    >>> foo._bar # weakref object stored as private variable
    <weakref at ... to 'SomeClass' at ...>
    
    """
    name = setter.__name__
    def _getter(self):
        value = getattr(self, "_" + name, None)
        return value() if isinstance(value, weakref.ref) else value
    def _setter(self, value):
        ref = weakref.ref(value) if value is not None else None
        setattr(self, '_' + name, ref)
        setter(self, value)
    return property(_getter, _setter)


# -----------------------------------------------------------------------------
# cachedproperty
# -----------------------------------------------------------------------------    

@__all__.register
def cachedproperty(getter=None, setter=None, deleter=None, varname=None):
    """Returns a property that caches first return of getter until a del is called.

    Args:
        getter (function): Getter function
        setter (function): Setter function
        deleter (function): Deleter function
        varname (str): Variable name to store cached data at, defaults to ``getter.__name__``
    Returns:
        return (property): property object with caching ability

    Example:

    >>> class Foo(object):
    ...     @cachedproperty
    ...     def bar(self):
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

    """
    varname_ = varname
    def _cachedproperty(getter):
        varname = varname_ or ('_' + getattr(getter, "__name__"))
        def _getter(self):
            value = getattr(self, varname, None)
            if value is None:
                value = getter(self)
                setattr(self, varname, value)
            return value
        def _setter(self, value):
            setattr(self, varname, value)
        def _deleter(self):
            setattr(self, varname, None)
        return property(_getter, setter or _setter, deleter or _deleter)
    if getter:
        return _cachedproperty(getter)
    return _cachedproperty



