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
Check out the examples for this module in :ref:`tut_collections`.

"""


# -------------------------------------------------------------------------------
# imports
# -------------------------------------------------------------------------------

from enum import Enum


# -----------------------------------------------------------------------------
# qlist
# -----------------------------------------------------------------------------

class qlist(list):
    """Simple list with convenience functions.

    Example:

        >>> l = qlist(['foo', 'bar'])
        >>> l.get(3, "not found")
        'not found'


    See more usage examples in :ref:`tut_qlist`.

    """


    def get(self, index: int, default=None):
        """Return an ``index``-th element from the list
        or return ``default`` if not found.

        Args:
            index (int): Index of the element to return
            default (object): Value to return if ``index`` is not found, defaults to None
        Returns:
            Return (object): ``self[index]`` or ``default``

        Example:

            >>> l = qlist(['foo', 'bar'])
            >>> l.get(0)
            'foo'
            >>> l.get(3, "not found")
            'not found'
            
        """
        if (index < 0) or (index >= len(self)):
            return default
        return self[index]


    def register(self, obj: object):
        """Add ``obj.__name__`` to the list and return ``obj``. 

        This function is meant to be used for dynamically composing the ``__all__`` 
        list for a python module.

        Args:
            obj (object): Any object with ``__name__`` attribute, typically a :py:class:`function` or :py:class:`type`
        Returns:
            Return (object): returns ``obj``

        Example:

            >>> __all__ = qlist()
            >>> @__all__.register
            ... def foo(): pass
            >>> @__all__.register
            ... class Bar(object): pass
            >>> __all__
            ['foo', 'Bar']

        """
        self.append(obj.__name__)
        return obj


# -----------------------------------------------------------------------------
# exports
# -----------------------------------------------------------------------------

__all__ = qlist()
__all__.register(qlist)


# -----------------------------------------------------------------------------
# qdict
# -----------------------------------------------------------------------------

@__all__.register
class qdict(dict):
    """
    Simple attribute dictionary with recursive update and other convenience functions.

    Example:

        >>> d = qdict( foo='hello', bar='world' )
        >>> d
        {'foo': 'hello', 'bar': 'world'}
        >>> d.foo
        'hello'
        >>> d.answer = 42
        >>> d
        {'foo': 'hello', 'bar': 'world', 'answer': 42}
    
    See more usage examples in :ref:`tut_qdict`.

    """

    __qdict_allow_attributes__ = False

    @classmethod
    def convert(cls, source: dict):
        """Returns a deepcopy of ``source`` with instances of :class:`dict` converted to 
        :py:class:`qdict` in values. It also processes elements in :py:class:`list` values.
        
        Args:
            source (:py:class:`dict`): Source dictionary
        Returns:
            (:class:`qdict`): Copy of source

        Example:

            >>> d = dict(a=1,b=dict(c=2,d=dict(),e=[dict(f=3,g=(dict(h=4)))]))
            >>> q = qdict.convert(d)
            >>> isinstance(q.b,qdict)
            True
            >>> isinstance(q.b.d,qdict)
            True
            >>> isinstance(q.b.e[0],qdict)
            True
            >>> isinstance(q.b.e[0].g,qdict)
            True


        """
        self = cls(source)
        for key, value in self.items():
            if isinstance(value, dict) and not isinstance(value, qdict):
                self[key] = cls.convert(value)
            elif isinstance(value, list):
                for index, item in enumerate(value):
                    if isinstance(item, dict) and not isinstance(item, qdict):
                        value[index] = cls.convert(item)
        return self


    def __getattr__(self, key):
        if not key in self:
            raise AttributeError(key)
        return self[key]


    def __setattr__(self, key, value):
        """Keeping qdict subclass private variables accessible.
    
        >>> class MyDict(qdict):
        ...     a = 'initial value'
        ...     def __init__(self, a, b):
        ...         self.a = a
        ...         self._b = b
        ...
        >>> md = MyDict('foo', 42)
        >>> md
        {'a': 'foo', '_b': 42}
        >>> md.a          # returns the class attribute
        'initial value'
        >>> md._b
        42
        >>> md.a = 'bar'
        >>> md
        {'a': 'bar', '_b': 42}
        >>> md.a          # still returns the class attribute
        'initial value'

        >>> class MyDict(qdict):
        ...     __qdict_allow_attributes__ = True
        ...     a = None
        ...     def __init__(self, a, b):
        ...         self.a = a
        ...         self._b = b
        ...
        >>> md = MyDict('foo', 42)
        >>> md
        {}
        >>> md.a
        'foo'
        >>> md._b
        42
        >>> md.a = 'bar'
        >>> md
        {}
        >>> md.a
        'bar'

        """
        if (self.__qdict_allow_attributes__ and
                (key.startswith('_') or key in self.__dict__ or key in self.__class__.__dict__)
           ):
            object.__setattr__(self, key, value)
            return
        self[key] = value


    def copy(self):
        """Returns a shallow copy of itself

        >>> my_dict = qdict(a=1,b=2)
        >>> copy_dict = my_dict.copy()
        >>> my_dict is copy_dict
        False
        >>> my_dict == copy_dict
        True

        """
        return qdict(self)

    def __add__(self, other):
        """Supports the `+` operand for two dictionaries
        
        Example:

            >>> dict1 = qdict(a=1,b=2)
            >>> dict2 = qdict(c=3,b=4)
            >>> dict1 + dict2
            {'a': 1, 'b': 4, 'c': 3}

        """
        res = self.copy()
        res.update(other)
        return res


    def _update_recursively_add_keys(self, other: dict, convert: bool):
        """

        Non-converting with only qdict:

        >>> dict1 = qdict(a=1, b=2, c=qdict(d=3, e=4, f=qdict(g=5, h=6)))
        >>> dict2 = qdict(a=10, c=qdict(d=20, f=qdict(g=30, i=40), j=50), k=60)
        >>> dict1._update_recursively_add_keys(dict2, False)
        {'a': 10, 'b': 2, 'c': {'d': 20, 'e': 4, 'f': {'g': 30, 'h': 6, 'i': 40}, 'j': 50}, 'k': 60}

        Non-converting with dict in other:

        >>> dict1 = qdict(a=1, b=2, c=qdict(d=3, e=4, f=qdict(g=5, h=6)))
        >>> dict2 = dict(a=10, c=dict(d=20, f=dict(g=30, i=40), j=50), k=60)
        >>> dict1._update_recursively_add_keys(dict2, False)
        {'a': 10, 'b': 2, 'c': {'d': 20, 'e': 4, 'f': {'g': 30, 'h': 6, 'i': 40}, 'j': 50}, 'k': 60}

        Non-converting with dict in self:

        >>> dict1 = qdict(a=1, b=2, c=dict(d=3, e=4, f=dict(g=5, h=6)))
        >>> dict2 = dict(a=10, c=dict(d=20, f=dict(g=30, i=40), j=50), k=60)
        >>> dict1._update_recursively_add_keys(dict2, False)
        {'a': 10, 'b': 2, 'c': {'d': 20, 'e': 4, 'f': {'g': 30, 'i': 40}, 'j': 50}, 'k': 60}

        Converting with dict in self:

        >>> dict1 = qdict(a=1, b=2, c=dict(d=3, e=4, f=dict(g=5, h=6)))
        >>> dict2 = dict(a=10, c=dict(d=20, f=dict(g=30, i=40), j=50), k=60)
        >>> dict1._update_recursively_add_keys(dict2, True)
        {'a': 10, 'b': 2, 'c': {'d': 20, 'e': 4, 'f': {'g': 30, 'h': 6, 'i': 40}, 'j': 50}, 'k': 60}

        """
        for key, other_value in other.items():
            if convert and isinstance(other_value, dict) and not isinstance(other_value, qdict):
                other_value = qdict(other_value)
            if isinstance(other_value, dict) and (key in self):
                current_value = self[key]
                if convert and isinstance(current_value, dict) and not isinstance(current_value, qdict):
                    current_value = qdict(current_value)
                    self[key] = current_value
                if isinstance(current_value, qdict):
                    current_value._update_recursively_add_keys(other_value, convert)
                    continue
                if isinstance(current_value, dict):
                    current_value.update(other_value)
                    continue
            self[key] = other_value
        return self


    def _update_recursively_fix_keys(self, other: dict, convert: bool):
        """

        Non-converting with only qdict:

        >>> dict1 = qdict(a=1, b=2, c=qdict(d=3, e=4, f=qdict(g=5, h=6)))
        >>> dict2 = qdict(a=10, c=qdict(d=20, f=qdict(g=30, i=40), j=50), k=60)
        >>> dict1._update_recursively_fix_keys(dict2, False)
        {'a': 10, 'b': 2, 'c': {'d': 20, 'e': 4, 'f': {'g': 30, 'h': 6}}}

        Non-converting with dict in other:

        >>> dict1 = qdict(a=1, b=2, c=qdict(d=3, e=4, f=qdict(g=5, h=6)))
        >>> dict2 = dict(a=10, c=dict(d=20, f=dict(g=30, i=40), j=50), k=60)
        >>> dict1._update_recursively_fix_keys(dict2, False)
        {'a': 10, 'b': 2, 'c': {'d': 20, 'e': 4, 'f': {'g': 30, 'h': 6}}}

        Non-converting with dict in self:

        >>> dict1 = qdict(a=1, b=2, c=dict(d=3, e=4, f=dict(g=5, h=6)))
        >>> dict2 = dict(a=10, c=dict(d=20, f=dict(g=30, i=40), j=50), k=60)
        >>> dict1._update_recursively_fix_keys(dict2, False)
        {'a': 10, 'b': 2, 'c': {'d': 20, 'e': 4, 'f': {'g': 30, 'i': 40}, 'j': 50}}

        Converting with dict in self:

        >>> dict1 = qdict(a=1, b=2, c=dict(d=3, e=4, f=dict(g=5, h=6)))
        >>> dict2 = dict(a=10, c=dict(d=20, f=dict(g=30, i=40), j=50), k=60)
        >>> dict1._update_recursively_fix_keys(dict2, True)
        {'a': 10, 'b': 2, 'c': {'d': 20, 'e': 4, 'f': {'g': 30, 'h': 6}}}

        """
        for key, current_value in self.items():
            if convert and isinstance(current_value, dict) and not isinstance(current_value, qdict):
                current_value = qdict(current_value)
                self[key] = current_value
            if not key in other:
                continue
            other_value = other[key]
            if convert and isinstance(other_value, dict) and (not isinstance(other_value, qdict)):
                other_value = qdict(other_value)
            if isinstance(current_value, qdict):
                current_value._update_recursively_fix_keys(other_value, convert)
            elif isinstance(current_value, dict):
                current_value.update(other_value)
            else:
                self[key] = other_value
        return self


    def update(self, other: dict, recursive: bool = False, add_keys: bool = True, convert: bool = False):
        """Extended version inherited :py:meth:`dict.update` with recursion, key restriction and
        conversion support. 

        .. note:: 
            Please note recursion *will only work as expected* if all dictionaries 
            in ``self`` are :class:`qdict` instances. Use ``convert=True`` to for on-the-fly conversion 
            of :py:class:`dict` instances to :class:`qdict` instances.

        Args:
            other (:py:class:`dict`): other to copy values from to ``self``
            recursive (bool): Recursively update ``dict()`` values, defaults to False
            add_keys (bool): Add keys that are in `other` but not in `self`, default to True
            convert (bool): Convert encountered ``dict()`` to ``qdict()``, defaults to False
        Returns:
            :class:`qdict`: returns self

        Examples:

            Default behaviour is the same as inherited :py:meth:`dict.update`, non-recursive
            update with adding new keys.

            >>> my_dict = qdict(a=1, b=qdict(c=10, d=20))
            >>> my_dict.update(dict(b=dict(e=100, f=200), g=300))
            {'a': 1, 'b': {'e': 100, 'f': 200}, 'g': 300}

            Non-recursively update ``self`` from ``other`` without adding new keys. Note
            that the second level dictionary is *replaced* by the new one, so the new 
            keys are added implicitly.

            >>> my_dict = qdict(a=1, b=qdict(c=10, d=20))
            >>> my_dict.update(dict(b=dict(c=5, e=100), f=200), add_keys=False)
            {'a': 1, 'b': {'c': 5, 'e': 100}}


            Recursively update ``self`` from ``other``.

            >>> my_dict = qdict(a=1, b=qdict(c=10, d=20))
            >>> my_dict.update(dict(b=dict(c=5, e=100), f=200), recursive=True)
            {'a': 1, 'b': {'c': 5, 'd': 20, 'e': 100}, 'f': 200}

            Recursively update **existing keys** in ``self`` with values from ``other``:

            >>> my_dict = qdict(a=1, b=qdict(c=10, d=20))
            >>> my_dict.update(dict(b=dict(c=5, e=100), f=200), recursive=True, add_keys=False)
            {'a': 1, 'b': {'c': 5, 'd': 20}}
            
            It will not do anything if the ``other`` is not a dict instance.

            >>> my_dict = qdict(a=1)
            >>> my_dict.update(None)
            {'a': 1}
            >>> my_dict.update(1234)
            {'a': 1}


        """
        if not isinstance(other, dict):
            return self
        if recursive:
            if add_keys:
                return self._update_recursively_add_keys(other, convert)
            return self._update_recursively_fix_keys(other, convert)
        if add_keys:
            super(qdict, self).update(other)
            return self
        for key in self:
            self[key] = other.get(key, self[key])
        return self


# -----------------------------------------------------------------------------
# ObjectDict
# -----------------------------------------------------------------------------

@__all__.register
class ObjectDict(qdict):
    """Dictionary with decorators to append objects with ``__name__`` 
    attribute which are typically classes or functions. 

    This class is intended to be used for meta programming tasks, like implementing
    the request handler function registration in a web server framework.
    
    
    Examples:

        Registering a function with :meth:`ObjectDict.register` decorator:

        >>> my_dir = ObjectDict()
        >>> @my_dir.register
        ... def foo(self): pass
        >>> my_dir['foo']
        <function foo at ...>

        Registering a class with :meth:`ObjectDict.register` decorator:

        >>> @my_dir.register
        ... class Bar(object): pass
        >>> my_dir['Bar']
        <class 'qtils.collections.Bar'>
    
        See more usage examples in :ref:`tut_object_dict`.

    """

    def register(self, obj):
        """Decorator to append an object with ``__name__`` to
        the dictionary.

        Args:
            obj (object): Any object with ``__name__`` attribute, typically a :py:class:`function` or :py:class:`type`
        Returns:
            Return (object): returns ``obj``

        """
        self[obj.__name__] = obj
        return obj

    def register_module(self, module):
        """Append all classes from a python module to the dictionary

        Args:
            module (:py:class:`module`): A python module object

        Example:

            >>> my_dir = ObjectDict()
            >>> import datetime
            >>> my_dir.register_module(datetime)
            >>> my_dir['datetime']
            <class 'datetime.datetime'>

        """
        for name in dir(module):
            value = getattr(module, name)
            if isinstance(value, type):
                self.register(value)


# ---------------------------------------------------------------------------------------------------------
# SmartEnum
# ---------------------------------------------------------------------------------------------------------

@__all__.register
class QEnum(Enum):
    """Enumeration with introspection capability

    Example:

        >>> class MyEnum(QEnum):
        ...     KEY_A = "hello"
        ...     KEY_B = "world"
        ...
        >>> MyEnum.keys()
        ['KEY_A', 'KEY_B']
        >>> MyEnum.values()
        ['hello', 'world']

    See more usage examples in :ref:`tut_qenum`.

    """

    @classmethod
    def keys(cls):
        """Returns available keys as a list of strings
        """
        return [str(i.name) for i in cls]

    @classmethod
    def values(cls):
        """Returns available values as a list of strings
        """
        return [str(i.value) for i in cls]






