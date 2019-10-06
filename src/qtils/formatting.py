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
Formatting module
===================


This module contains formatting helpers.

Attributes:
    PRETTY_FORMAT: Format string presets to be used for :class:`PrettyObject` class attribute 
        ``__pretty_format__``. Presets are accessible as attributes, for example ``PRETTY_FORMAT.FULL``.

        Available presets:

        =========================== ===================================================================================
        Name                        Example
        =========================== ===================================================================================
        ``PRETTY_FORMAT.FULL``      ``<mypackage.mysubmodule.MyObject object at 0x000000000 answer=42, hello='world'>``
        ``PRETTY_FORMAT.BRIEF``     ``<MyObject object at 0x000000000 answer=42, hello='world'>``
        ``PRETTY_FORMAT.SHORT``     ``<MyObject 0x000000000 answer=42, hello='world'>``
        ``PRETTY_FORMAT.MINIMAL``   ``<MyObject answer=42, hello='world'>``
        =========================== ===================================================================================


"""


# -------------------------------------------------------------------------------
# imports
# -------------------------------------------------------------------------------

from .collections import qlist, qdict


# -----------------------------------------------------------------------------
# exports
# -----------------------------------------------------------------------------

__all__ = qlist()


# ---------------------------------------------------------------------------------------------------------
# NA
# ---------------------------------------------------------------------------------------------------------

class _NAMeta(type):
    __repr__ = lambda s: "NA"
    __str__ = lambda s: "??"

    __instance = None


class NA(metaclass=_NAMeta):
    """This class represents the 'Not Available' value. 

    Can be usefull when a need to return that there is no value for the function,
    but None is also considered as a meaningfull value.

    """

    __repr__ = lambda s: "NA"
    __str__ = lambda s: "??"

    def __new__(cls):
        return cls

    def __eq__(self, other):
        if isinstance(other, NA):
            return True
        if isinstance(other, type) and issubclass(other, NA):
            return True
        return False

# NA = NAMeta("NA", (_NA,), {})

__all__.append("NA")


# -----------------------------------------------------------------------------
# format_filesize()
# -----------------------------------------------------------------------------

PRETTY_FORMAT = qdict(
    FULL="<{cls.__module__}.{cls.__name__} object at 0x{{__self_id__:02x}} {fields}>",
    BRIEF="<{cls.__name__} object at 0x{{__self_id__:02x}} {fields}>",
    SHORT="<{cls.__name__} 0x{{__self_id__:02x}} {fields}>",
    MINIMAL="<{cls.__name__} {fields}>",
)

__all__.append("PRETTY_FORMAT")


# -----------------------------------------------------------------------------
# PrettyObject
# -----------------------------------------------------------------------------    

@__all__.register
class PrettyObject(): # pylint: disable=too-few-public-methods,line-too-long
    """Object with pretty self printing ability

    Self-formatting is implemented by overriding the :py:meth:`object.__str__` method. 

    Example:
        
        Simple example with printing fields of the object:

        >>> class MyObject(PrettyObject):
        ...     __pretty_format__ = PRETTY_FORMAT.BRIEF
        ...     __pretty_fields__ = [
        ...         'hello',
        ...         'answer',
        ...     ]
        ...     def __init__(self, hello, answer):
        ...         self.hello = hello
        ...         self.answer = answer
        >>> obj = MyObject('world', 42)
        >>> print(obj)
        <MyObject object at ... hello='world', answer=42>


    Implementation Notes:
    
    A class level format string is created  from the ``__pretty_format__`` and ``__pretty_fields`` 
    class attributes. This class-level format is saved in the ``__pretty_format_str__`` class 
    attribute.

    Object formatting happens when :meth:`PrettyObject.__str__` is called, for example when
    the object instance is being printed. During this formatting :py:func:`getattr` is used to
    get values for all the fields in ``__pretty_fields__``. Then the class-level format string
    in ``__pretty_format_str__`` will be formatted to create the object's pretty string.

    .. note:: 

        Because of the getattr calls during formatting, printing a PrettyObject() can 
        cause side-effects in case properties that are executing calls in their getter 
        functions are referred in the ``__pretty_fields__``.

    Use the following class level attributes in descendant classes to configure the formatting:

    Attributes:    
        __pretty_format__ (str): Format string for the object to be used with :py:meth:`str.format`.
            Defaults to ``PRETTY_FORMAT.FULL`` which is: 
            ``<{cls.__module__}.{cls.__name__} object at 0x{{__self_id__:02x}} {fields}>``
            
            Values available for py:meth:`str.format` in the creation of the class-level format string:

            - ``cls``: Class which is being formatted
            - ``fields``: Format placeholders of the individual fields

            Values available for py:meth:`str.format` at object level formatting. These fields needs to 
            be double escaped, for example: ``{{__self_id__}}``.

            - ``__self__``: Object instance being formatted
            - ``__self_id__``: id(self) of the object being formatted


        __pretty_field_separator__ (str): Separator used to join the individual fields, defaults to ``', '``
        
        __pretty_fields__ (list): Object attribute names to be included when printing the objects. Default to None.
            This attribute **must** be declared in descendant classes. 

            List should contain attribute names. Each attribute with be read using ``getattr(self, name, NA)``, 
            please consider side-effects when listing properties with complicated getter functions.

            Advanced string formatting defined :pep:`3101` can be applied to each field.

            Examples:

            =============================== =========================================================================
            Field format string             Description
            =============================== =========================================================================
            ``'my_field'``                  Format the field's value with :py:meth:`object.repr`, default behaviour.
            ``'my_field:>10,.2f'``          Format string to be 10 digits wide and align to left, use ``,`` as 
                                            thousand separator and use 2 digit precision.
            ``'my_field!s'``                Use ``str(my_field)`` to format field value. This will return 
                                            ``my_field=foo`` instead of ``my_field='foo'``. Note the missing single 
                                            quotes around ``foo``
            =============================== =========================================================================


    Examples:

        Creating table-like formatting using tab ``\\t`` as field separator and fixed width fields.

        >>> class MathConstant(PrettyObject):
        ...     __pretty_format__ = PRETTY_FORMAT.MINIMAL
        ...     __pretty_field_separator__ = "\t"
        ...     __pretty_fields__ = [
        ...         "name!s:<20",
        ...         "symbol!s:<5",
        ...         "description!s:<50",
        ...         "value:>10.6f",
        ...     ]
        ...     def __init__(self, name, symbol, description, value):
        ...         self.name = name
        ...         self.symbol = symbol
        ...         self.description = description
        ...         self.value = value
        ...
        >>> math_constants = [
        ...     MathConstant("Archimedes constant", "π", "Circumference to diameter ratio of a circle", 3.1415926535),
        ...     MathConstant("Euler's number", "e", "Exponential growth constant", 2.7182818284),
        ...     MathConstant("Pythagoras constant", "√2", "The square root of 2", 1.414213562373095),
        ... ]
        >>> for mc in math_constants:
        ...     print(mc)
        <MathConstant name=Archimedes constant   symbol=π      description=Circumference to diameter ratio of a circle         value=  3.141593>
        <MathConstant name=Euler's number        symbol=e      description=Exponential growth constant                         value=  2.718282>
        <MathConstant name=Pythagoras constant   symbol=√2     description=The square root of 2                                value=  1.414214>


    """

    __pretty_format__ = PRETTY_FORMAT.FULL

    __pretty_field_separator__ = ", "


    @classmethod 
    def __parse_pretty_field_def(cls, field_def):
        if '!' in field_def:
            field_def = field_def.split('!', 1)
            field_def[1] = '!' + field_def[1]
            return field_def
        if ':' in field_def:
            field_def = field_def.split(':', 1)
            field_def[1] = ':' + field_def[1]
            return field_def
        return field_def, "!r"


    @classmethod
    def __get_pretty_field_defs(cls):
        if getattr(cls, '__pretty_field_defs__', None) is None:
            fields = getattr(cls, '__pretty_fields__', None)
            if not fields:
                fields = getattr(cls, '__slots__', None)
            if not fields:
                cls.__pretty_field_defs__ = False
                return False
            cls.__pretty_field_defs__ = list(map(cls.__parse_pretty_field_def, fields))
        return cls.__pretty_field_defs__


    @classmethod
    def __get_pretty_format_str(cls):
        """
        Returns:
            return (str): Formattable string with field names
        """
        if getattr(cls, '__pretty_format_str__', None) is None:
            field_defs = cls.__get_pretty_field_defs()
            if not field_defs:
                cls.__pretty_format_str__ = False
                return False
            fields = cls.__pretty_field_separator__.join(["{0}={{{0}{1}}}".format(*f) for f in field_defs])
            cls.__pretty_format_str__ = cls.__pretty_format__.format(cls=cls, fields=fields)
        return str(cls.__pretty_format_str__)


    def __str__(self):
        field_defs = self.__get_pretty_field_defs()
        if not field_defs:
            return super(PrettyObject, self).__repr__()
        context = {"__self_id__": id(self), "__self__": self}
        for name, _ in field_defs:
            try:
                value = getattr(self, name, NA)
            except Exception as exc:
                value = exc
            context[name] = value
        return self.__get_pretty_format_str().format(**context)


    __repr__ = __str__


# -----------------------------------------------------------------------------
# format_filesize()
# -----------------------------------------------------------------------------

_FORMAT_FILESIZE_PRECISIONS = (
    ('bytes', 0),
    ('k', 0),
    ('M', 1),
    ('G', 2),
    ('T', 2),
    ('P', 2),
    ('E', 2),
    ('Y', 2),
    ('Z', 2),
)

@__all__.register
def format_filesize(size: int, precision: int = None):
    """Returns a :py:class:`float` value formatted as file size in string
    """
    prec = 0
    unit = _FORMAT_FILESIZE_PRECISIONS[0]
    for unit, prec in _FORMAT_FILESIZE_PRECISIONS:
        if size < 1024.0:
            break
        size /= 1024.0
    return "{:3.{prec}f} {}".format(size, unit, prec=precision if precision is not None else prec)


