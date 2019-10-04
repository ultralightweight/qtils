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


# -------------------------------------------------------------------------------
# imports
# -------------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# qlist
# -----------------------------------------------------------------------------

class qlist(list):
    """
    Basic ``list`` with a couple shorthands.
    
    """

    def get( self, index, default = None ):
        """Return an ``index``-th element from the list
        or return ``default`` if not found.

        :param index: Index of the element to return
        :param default: Value to return if ``index`` not found.

        >>> l = qlist(['foo', 'bar'])
        >>> l.get(0)
        'foo'
        >>> l.get(3, "not found")
        'not found'
        """
        if (index < 0) or ( index >= len(self) ):
            return default
        return self[index]
        

    def register( self, item ):
        """Add ``item.__name__`` to the list and return 
        ``item``. This function is meant to be used for 
        dynamically composing the ``__all__`` list for a python 
        mudule.

        >>> __all__ = qlist()
        >>> @__all__.register
        ... def foo(): pass
        >>> @__all__.register
        ... class Bar(object): pass
        >>> __all__
        ['foo', 'Bar']

        """
        self.append( item.__name__ )
        return item


    def __str__(self):
        """TODO: Document or remove me
        """
        return '[' + ', '.join([str(i) for i in self]) + ']'



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
    Simple attribute dictionary with a couple shorthands.

    Typical usage:
            
    >>> d = qdict( foo='hello', bar='world' )
    >>> d
    {'foo': 'hello', 'bar': 'world'}
    >>> d.foo
    'hello'
    >>> d.answer = 42
    >>> d
    {'foo': 'hello', 'bar': 'world', 'answer': 42}

    """

    # def __init__(self, *args, **kw):
    #     super(qdict,self).__init__( *args, **kw )


    def __getattr__(self, key):
        if not key in self:
            raise AttributeError(key)
        return self[key]


    def __setattr__(self, key, value):
        if key.startswith('_') or key in self.__dict__ or key in self.__class__.__dict__:
            return super(qdict, self).__setattr__(key, value)
        self[key] = value


    def copy(self, add=None):
        """Returns a shallow copy of self
        """
        res = qdict()
        res.update( self, False )
        if add:
            res.update( add )
        return res

        
    def __add__(self, other):
        """Supports the `+` operand for two dictionaries

        >>> d1 = qdict(a=1,b=2)
        >>> d2 = qdict(c=3,b=4)
        >>> d1 + d2
        {'a': 1, 'b': 4, 'c': 3}

        """
        res = self.copy()
        res.update( other )
        return res


    def update(self, other, recursive=False, add_keys=True, convert=False):
        """Extended version inherited :py:meth:`dict.update` with recursion, key restriction and conversion support.
    
        Args:
            other (:py:class:`dict`): other to copy values from to ``self``
            recursive (bool): Recursively update ``dict()`` values, defaults to True
            add_keys (bool): Add keys that are in `other` but not in `self`, default to True
            convert (bool): Convert encountered ``dict()`` to ``qdict()``, defaults to False
        Returns:
            :class:`qdict`: returns self

        Default behaviour is the same as the inherited :py:meth:`dict.update`:

        >>> my_dict = qdict(a=1, b=qdict(c=10, d=20))
        >>> my_dict.update(dict(b=dict(c=5, e=100), f=200))
        {'a': 1, 'b': {'c': 5, 'e': 100}, 'f': 200}

        Recursively update ``self`` from ``other``. Please note: this *works only* if all dictionaries in ``self`` are 
        :class:`qdict` instances. Use ``convert=True`` to enforce on-the-fly conversion of :py:class:`dict` to :class:`qdict`.

        >>> my_dict = qdict(a=1, b=qdict(c=10, d=20))
        >>> my_dict.update(dict(b=dict(c=5, e=100), f=200), recursive=True)
        {'a': 1, 'b': {'c': 5, 'd': 20, 'e': 100}, 'f': 200}

        Recursively update **only** existing keys in ``self`` with values from ``other``:

        >>> my_dict = qdict(a=1, b=qdict(c=10, d=20))
        >>> my_dict.update(dict(b=dict(c=5, e=100), f=200), recursive=True, add_keys=False)
        {'a': 1, 'b': {'c': 5, 'd': 20}}

        """
        if not isinstance(other, dict): return self
        if not recursive:
            if add_keys:
                super(qdict,self).update(other)
                return self
            for k in self:
                self[k] = other.get(k,self[k])
            return self
        if add_keys:
            for k, nv in other.items():
                if convert and isinstance(nv, dict) and (not isinstance(nv, qdict)):
                    nv_ = qdict()
                    nv_.update(nv, recursive=recursive, add_keys=add_keys, convert=convert)
                    nv = nv_
                if isinstance(nv, dict) and (k in self):
                    cv = self[k]
                    if isinstance(cv, dict) and convert:
                        cv = qdict(cv)
                        self[k] = cv
                    if isinstance(cv, qdict):
                        cv.update(nv, recursive=recursive, add_keys=add_keys, convert=convert)
                        continue
                    if isinstance(cv, dict):
                        cv.update(nv)
                        continue
                if convert and isinstance(nv, list):
                    for i in range(len(nv)):
                        if isinstance(nv[i], qdict): continue
                        if isinstance(nv[i], dict):
                            nnv = qdict()
                            nnv.update(nv[i], recursive=recursive, add_keys=add_keys, convert=convert)
                            nv[i] = nnv
                self[k] = nv
            return self
        for k, cv in self.items():
            try:
                nv = other[k]
            except KeyError:
                continue
            if convert and isinstance(nv, dict) and (not isinstance(nv, qdict)):
                nv = qdict(nv)
            if isinstance(cv, qdict):
                cv.update(nv, recursive=recursive, add_keys=add_keys, convert=convert)
            elif isinstance(cv, dict):
                cv.update(nv)
            else:
                self[k] = nv
        return self


