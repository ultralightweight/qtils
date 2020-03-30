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

import re
import math
from enum import Enum

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

    def __eq__(cls, other):
        """NA should be equal to itself and any subclasses of itself

        >>> NA == NA()
        True
        >>> class MyNA(NA): pass
        >>> MyNA == NA
        True
        >>> MyNA() == NA
        True
        """
        if isinstance(other, type) and issubclass(other, NA):
            return True
        return False


class NA(metaclass=_NAMeta):  # pylint: disable=too-few-public-methods
    """This class represents the **ValueNotAvailable** state.

    This constant is meant to be used when :py:class:`None` has a meaningful value,
    and it can not be used to represent the state of a value being absent.

    Examples:

        ``NA`` is always represented in a short format:

        >>> str(NA)
        '??'
        >>> repr(NA)
        'NA'


        ``NA`` only exsists in class form, no instance can be created from it.

        >>> NA == NA()
        True
        >>> NA is NA()
        True


        Usage example:

        >>> data_from_an_api = {'field1': 'foo', 'field2': None}
        >>> def is_field_present(field_name):
        ...     return data_from_an_api.get(field_name, NA) is not NA
        >>> is_field_present('field1')
        True
        >>> is_field_present('field2')
        True
        >>> is_field_present('field3')
        False

    """

    __repr__ = lambda s: "NA"
    __str__ = lambda s: "??"

    def __new__(cls):
        """No instance should ever be created

        >>> NA() is NA
        True

        """
        return cls


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
class PrettyObject(): # pylint: disable=too-few-public-methods,line-too-long,broad-except
    """Object with pretty self printing ability

    Self-formatting is implemented by overriding the :py:meth:`object.__str__` method.

    Example:

        Simple example with printing fields of the object:

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
        <qtils.formatting.MyObject object at ... hello='world', answer=42>


        This is works automatically for objects with ``__slots__``

        >>> class MySlotObject(PrettyObject):
        ...     __slots__ = [
        ...         'hello',
        ...         'answer',
        ...     ]
        ...     def __init__(self, hello, answer):
        ...         self.hello = hello
        ...         self.answer = answer
        >>> obj = MySlotObject('world', 42)
        >>> print(obj)
        <qtils.formatting.MySlotObject object at ... hello='world', answer=42>



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

        Returning :class:`NA` for non-existent fields:

        >>> class MyObject(PrettyObject):
        ...     __pretty_fields__ = [
        ...         "non_existent",
        ...     ]
        ...
        >>> obj = MyObject()
        >>> print(obj)
        <qtils.formatting.MyObject object at ... non_existent=NA>

        Exceptions encountered during formatting are printed as the value for the field.
        Please note that this can lead to problems with fields expecting a ``float`` or ``int`` value. However,
        exceptions during attribute reading should not happen in the first place.

        >>> class MyObject(PrettyObject):
        ...     __pretty_fields__ = [
        ...         "foo",
        ...     ]
        ...     @property
        ...     def foo(self):
        ...         return non_existent # this will raise an exception
        >>> obj = MyObject()
        >>> print(obj)
        <qtils.formatting.MyObject object at ... foo=NameError("name 'non_existent' is not defined")>

        Descendants of PrettyObject subclasses are inheriting parents' field configurations
        by default.

        >>> class BaseClass(PrettyObject):
        ...     __pretty_fields__ = [
        ...         "foo",
        ...     ]
        ...     def __init__(self, foo, bar):
        ...         self.foo = foo
        ...         self.bar = bar
        ...
        >>> print(BaseClass('hello', 'world'))
        <qtils.formatting.BaseClass object at ... foo='hello'>
        >>>
        >>> class SubClassOne(BaseClass):
        ...     pass
        ...
        >>> print(SubClassOne('hello', 'world'))
        <qtils.formatting.SubClassOne object at ... foo='hello'>


        Subclasses can overwrite inherited field configuration by defining a new field
        configuration

        >>> class SubClassTwo(BaseClass):
        ...     __pretty_fields__ = [
        ...         "bar",
        ...     ]
        >>> print(SubClassTwo('hello', 'world'))
        <qtils.formatting.SubClassTwo object at ... bar='world'>

        Or Subclasses can extend/alter parents field configuration using simple list
        operations.

        >>> class SubClassThree(BaseClass):
        ...     __pretty_fields__ = BaseClass.__pretty_fields__ + [
        ...         "bar",
        ...     ]
        >>> print(SubClassThree('hello', 'world'))
        <qtils.formatting.SubClassThree object at ... foo='hello', bar='world'>

    """

    __pretty_format__ = PRETTY_FORMAT.FULL

    __pretty_field_separator__ = ", "


    @classmethod
    def __parse_pretty_field_def(cls, field_def):
        """Parses a single field definition

        Testing badly formatted field names

        >>> class MyObject(PrettyObject):
        ...     __pretty_fields__ = [
        ...         "a:<asdf",
        ...     ]
        ...     def __init__(self, a): self.a = a
        >>> obj = MyObject('test')
        >>> print(obj)
        Traceback (most recent call last):
        ...
        ValueError: Invalid format specifier
        """
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
        """Returns and caches parsed field definition array

        Testing if everything works if no fields are defined.

        >>> class Obj(PrettyObject):
        ...     def __init__(self, a):
        ...         self.a = a
        >>> obj = Obj(1)
        >>> print(obj)
        <qtils.formatting.Obj object at ...>
        """
        if cls.__dict__.get('__pretty_field_defs__', None) is None:
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
        if cls.__dict__.get('__pretty_format_str__', None) is None:
            field_defs = cls.__get_pretty_field_defs()
            fields = cls.__pretty_field_separator__.join(["{0}={{{0}{1}}}".format(*f) for f in field_defs])
            cls.__pretty_format_str__ = cls.__pretty_format__.format(cls=cls, fields=fields)
        return str(cls.__pretty_format_str__)


    def __str__(self):
        field_defs = self.__get_pretty_field_defs()
        if not field_defs:
            return super().__repr__()
        context = {"__self_id__": id(self), "__self__": self}
        for name, _ in field_defs:
            try:
                value = getattr(self, name, NA)
            except Exception as exc:
                value = exc
            context[name] = value
        return self.__get_pretty_format_str().format(**context)


    # __repr__ = __str__


# -----------------------------------------------------------------------------
# DataSize Systems
# -----------------------------------------------------------------------------

@__all__.register   # pylint: disable=invalid-name
class DATA_UNIT_SYSTEM(Enum):
    """Data Unit Systems

    Attributes:
        BINARY: Use powers of 2 for magnitudes
        METRIC: Use powers of 10 for magnitudes

    """

    BINARY = 0
    METRIC = 1


# -----------------------------------------------------------------------------
# DataSize Constants
# -----------------------------------------------------------------------------

_DATASIZE_SUFFIXES_AND_PRECISIONS = (
    (
        (('b', "B", "byte"), 0),
        (('K', "KB", "kibibyte"), 0),
        (('M', "MiB", "mebibyte"), 1),
        (('G', "GiB", "gibibyte"), 2),
        (('T', "TiB", "tebibyte"), 2),
        (('P', "PiB", "pebibyte"), 2),
        (('E', "EiB", "exbiytes"), 2),
        (('Z', "YiB", "zebibyte"), 2),
        (('Y', "ZiB", "yobibyte"), 2),
    ),
    (
        (('b', "B", "byte"), 0),
        (('k', "kB", "kilobyte"), 0),
        (('M', "MB", "megabyte"), 1),
        (('G', "GB", "gigabyte"), 2),
        (('T', "TB", "terabyte"), 2),
        (('P', "PB", "petabyte"), 2),
        (('E', "EB", "exabyte"), 2),
        (('Z', "YB", "zettabyte"), 2),
        (('Y', "ZB", "yottabyte"), 2),
    )
)

_DATASIZE_PARSER = re.compile(r'^([\d.,]+)\s*([bkmgtpeyz]?)')

# We create the reverse map of _DATASIZE_SUFFIXES_AND_PRECISIONS in an automatic fashion.

_DATASIZE_SUFFIX_TO_MAGNITUDE = tuple(map(
    lambda system: dict(map(
        lambda e: (e[1][0][0].lower()[:1], e[0]),
        enumerate(system)
    )),
    _DATASIZE_SUFFIXES_AND_PRECISIONS
))

_DATASIZE_MAGNITUDE_MULTIPLIER = (
    1024,
    1000,
)


# -----------------------------------------------------------------------------
# DataSize
# -----------------------------------------------------------------------------

@__all__.register
class DataSize(int):
    """Integer object representing data size with two-way conversion ability.

    It stores the data size in bytes as int. It can display the value in different
    units. By default it uses the most suitable unit automatically. This behaviour
    can be changed by calling the :meth:`DataSize.format` directly, or by changing
    the default unit in the ``DEFAULT_UNIT`` class attribute.

    This class supports different systems of units. It supports the ``BINARY``
    system in which a magnitude is ``2**10=1024`` bytes, and the ``METRIC`` system in which
    a magnitude is ``10**3=1000`` bytes. By default it uses the ``METRIC`` system. Read more
    about the topic in the
    `Units of information Wikipedia article <https://en.wikipedia.org/wiki/Units_of_information>`_.


    Examples:

        Pretty printing data size values with automatic unit and
        precision detection:

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

        >>> DataSize('1.45 mebibytes')
        1520435
        >>> DataSize('23.3gib')
        25018184499
        >>> DataSize('1 T', system=DATA_UNIT_SYSTEM.BINARY)
        1099511627776
        >>> DataSize('1,123,456.789 MB', system=0)
        1178029825982


        Comparison of the ``BINARY`` and the ``METRIC`` unit systems:

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

        >>> DataSize('invalid size data')
        Traceback (most recent call last):
        ...
        ValueError: Invalid data size literal: 'invalid size data'


    Formatting can be controlled and customized using the
    :meth:`DataSize.format` method, or by changing the defaults set
    by class attributes.


    Attributes:

        DEFAULT_UNIT_SYSTEM (:class:`DATA_UNIT_SYSTEM`): Binary or Metric system to use, defaults
            to ``DATA_UNIT_SYSTEM.METRIC``

        DEFAULT_UNIT (str): Sets the default unit to use (see more in :meth:`DataSize.format`
            documentation.). ``None`` means automatic unit choice.

        DEFAULT_UNIT_FORMAT (int): Sets the default unit format (see more in :meth:`DataSize.format`
            documentation.)

        DEFAULT_NUMBER_FORMAT (str): Sets the default format string

    """

    DEFAULT_UNIT_SYSTEM = DATA_UNIT_SYSTEM.METRIC

    DEFAULT_UNIT = None                                 # automatic unit choice

    DEFAULT_UNIT_FORMAT = 0                             # single letter

    DEFAULT_NUMBER_FORMAT = "{:.{precision}f} {:}"

    def __new__(cls, value, system=None):
        """Parses input value as file size

        Testing error handling

        >>> DataSize('0..1')
        Traceback (most recent call last):
        ...
        ValueError: Invalid data size literal: '0..1'

        >>> DataSize((1, 2, 3))
        Traceback (most recent call last):
        ...
        ValueError: Invalid data size literal: '(1, 2, 3)'


        """
        if isinstance(value, str):
            value = value.lower()
            if system is None:
                system = DATA_UNIT_SYSTEM.METRIC
                if 'bibyte' in value or 'ib' in value:
                    system = DATA_UNIT_SYSTEM.BINARY
            elif not isinstance(system, DATA_UNIT_SYSTEM):
                system = DATA_UNIT_SYSTEM(system)
            match = _DATASIZE_PARSER.match(value)
            if not match:
                raise ValueError("Invalid data size literal: '{}'".format(value))
            groups = match.groups()
            size = groups[0].replace(',', '')
            try:
                size = float(size)
            except ValueError:
                raise ValueError("Invalid data size literal: '{}'".format(value))
            suffix = groups[1]
            if suffix == "":
                suffix = "b"
            magnitude = _DATASIZE_SUFFIX_TO_MAGNITUDE[system.value][suffix]
            value = size * _DATASIZE_MAGNITUDE_MULTIPLIER[system.value] ** magnitude
        elif isinstance(value, (float, int)):
            pass
        else:
            raise ValueError("Invalid data size literal: '{}'".format(value))
        return super().__new__(cls, value)


    def format(self, unit: str = None, precision: int = None, unit_format: object = None, # pylint: disable=too-many-arguments
               number_format: str = None, system: DATA_UNIT_SYSTEM = None):
        """Returns a formatted data size in str

        Arguments:

            unit (str,int): Unit to use, defaults to ``None``

                - If None, the most suitable unit based on the size will be choosen automatically.

                - Accepts a string with one or more letter SI prefix. For example ``'k'``
                  or ``'kilo'``, ``'G'`` or ``'giga'``, etc.

                - Accepts an integer referring to the SI magnitude, with ``0`` meaning *bytes*
                  and ``8`` meaning *yottabytes*.


            precision (int): How many fraction digits to display after the integers. Defaults to ``None``

                - If ``None``, precision will be chosen automatically based on the unit: 0 for bytes, 1 for kbytes and
                  2 for everything else.

                - Accepts an integer with the desired precision.

                Note: The precision has to be utilized in the number_format string, otherwise it will be
                ignored.


            unit_format (int): Sets how verbose the displayed unit should be. Defaults to ``None``.

                - ``None``: Use value from ``DataSize.DEFAULT_UNIT_FORMAT`` (default behaviour)
                - ``0``: Single letter units, for example: ``b``, ``k``, ``M``, etc.
                - ``1``: Short units, for example: ``B``, ``kB``, ``MB``, etc.
                - ``2``: Verbose units, for example: ``bytes``, ``kilobytes``, ``megabytes``, etc.


            number_format(str): Python format string to be used to format data size. Defaults to ``None``

                ``None``: Use value from ``DataSize.DEFAULT_NUMBER_FORMAT`` (default behaviour)

                Accepts any valid python format string.

                - File size converted to the requested magnitude is supplied as the first positional argument
                - Unit as string is supplied as the second positional argument.
                - Precision is supplied as ``precision`` keyword argument.

                Default format in ``DataSize.DEFAULT_NUMBER_FORMAT`` is: ``{:.{precision}f} {:}``

            system (:class:`DATA_UNIT_SYSTEM`): Unit system to use for formatting. Accepts integers or
                values from the :class:`DATA_UNIT_SYSTEM` Enum. If ``None`` it will use the default value
                from ``DataSize.DEFAULT_UNIT_SYSTEM``.


        Examples:

            Displaying the same :class:`DataSize` with different formatting

            >>> size = DataSize('1.7654321 G')
            >>> size.format()
            '1.77 G'
            >>> size.format(precision=4)
            '1.7654 G'
            >>> size.format(unit='m')
            '1765.4 M'
            >>> size.format(unit='m', precision=2)
            '1765.43 M'
            >>> size.format(unit_format=1)
            '1.77 GB'
            >>> size.format(unit_format=2)
            '1.77 gigabytes'
            >>> size.format(unit='m', precision=0, unit_format=2)
            '1765 megabytes'
            >>> size.format(unit="k", number_format="{:>20,.3f} {}")
            '       1,765,432.100 k'
            >>> size.format(unit="k", number_format="{:>20,.3f} {}", unit_format=2)
            '       1,765,432.100 kilobytes'

            Displaying the same data size using the BINARY unit system:

            >>> size = DataSize('1.7654321 G', system=0)
            >>> size.format(system=0)
            '1.77 G'
            >>> size.format(precision=4, system=0)
            '1.7654 G'
            >>> size.format(unit='m', system=0)
            '1807.8 M'
            >>> size.format(unit=2, system=0)
            '1807.8 M'
            >>> size.format(unit='m', precision=2, system=0)
            '1807.80 M'
            >>> size.format(unit_format=1, system=0)
            '1.77 GiB'
            >>> size.format(unit_format=2, system=0)
            '1.77 gibibytes'
            >>> size.format(unit='m', precision=0, unit_format=2, system=0)
            '1808 mebibytes'
            >>> size.format(unit="k", number_format="{:>20,.3f} {}", system=0)
            '       1,851,189.729 K'
            >>> size.format(unit="k", number_format="{:>20,.3f} {}", unit_format=2, system=0)
            '       1,851,189.729 kibibytes'

            Raises AttributeError if invalid arguments are supplied.

            >>> size.format(unit='l', system=0)
            Traceback (most recent call last):
            ...
            AttributeError: Unknown DataSize unit: 'l'



            Changing the default formatting settings

            >>> sizes = [
            ...     DataSize('208 k'),
            ...     DataSize('1.5 M'),
            ...     DataSize('542 M'),
            ...     DataSize('1.6 G'),
            ... ]
            >>> for size in sizes: print(size)
            208 k
            1.5 M
            542.0 M
            1.60 G
            >>> DataSize.DEFAULT_UNIT_FORMAT = 2
            >>> for size in sizes: print(size)
            208 kilobytes
            1.5 megabytes
            542.0 megabytes
            1.60 gigabytes
            >>> DataSize.DEFAULT_UNIT_FORMAT = 1
            >>> DataSize.DEFAULT_UNIT = "m"
            >>> for size in sizes: print(size)
            0.2 MB
            1.5 MB
            542.0 MB
            1600.0 MB
            >>> DataSize.DEFAULT_NUMBER_FORMAT = "{:>10,.3f} {}"
            >>> for size in sizes: print(size)
                 0.208 MB
                 1.500 MB
               542.000 MB
             1,600.000 MB
            >>> DataSize.DEFAULT_UNIT_SYSTEM = DATA_UNIT_SYSTEM.BINARY
            >>> for size in sizes: print(size)
                 0.198 MiB
                 1.431 MiB
               516.891 MiB
             1,525.879 MiB

            Resetting ``DataSize.DEFAULT_*`` to built-in defaults

            >>> DataSize.DEFAULT_UNIT_SYSTEM = DATA_UNIT_SYSTEM.METRIC
            >>> DataSize.DEFAULT_UNIT = None
            >>> DataSize.DEFAULT_UNIT_FORMAT = 0
            >>> DataSize.DEFAULT_NUMBER_FORMAT = "{:.{precision}f} {:}"

            >>> print(DataSize(0))
            0 b

        """
        system = self.DEFAULT_UNIT_SYSTEM if system is None else system
        if not isinstance(system, DATA_UNIT_SYSTEM):
            system = DATA_UNIT_SYSTEM(system)
        unit = unit or self.DEFAULT_UNIT
        unit_format = unit_format or self.DEFAULT_UNIT_FORMAT
        number_format = number_format or self.DEFAULT_NUMBER_FORMAT
        if unit is None:
            magnitude = int(math.log(int(self), _DATASIZE_MAGNITUDE_MULTIPLIER[system.value])) if self != 0 else 0
        elif isinstance(unit, int):
            magnitude = unit
        else:
            magnitude = _DATASIZE_SUFFIX_TO_MAGNITUDE[system.value].get(unit[:1].lower(), None)
            if not magnitude:
                raise AttributeError("Unknown DataSize unit: '{}'".format(unit))
        if precision is None:
            precision = _DATASIZE_SUFFIXES_AND_PRECISIONS[system.value][magnitude][1]
        unit = _DATASIZE_SUFFIXES_AND_PRECISIONS[system.value][magnitude][0][unit_format]
        size = int(self) / _DATASIZE_MAGNITUDE_MULTIPLIER[system.value] ** (magnitude)
        if size != 1.0 and len(unit) > 3:
            unit += 's'
        return number_format.format(size, unit, precision=precision)


    def __str__(self):
        return self.format()


    def __add__(self, other):
        return DataSize(super().__add__(other))


    def __sub__(self, other):
        return DataSize(super().__sub__(other))


    def __mul__(self, other):
        return DataSize(int(self)*other)


    def __truediv__(self, other):
        """
        >>> DataSize(10) // 3
        3
        """
        return DataSize(super().__truediv__(other))

    def __mod__(self, other):
        """
        >>> DataSize(5) % 3
        2
        """
        return DataSize(super().__mod__(other))



