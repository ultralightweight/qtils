# encoding: utf-8
# package: qtils
# author: Daniel Kovacs <github.com/neonihil>
# file-version: 1.0
# licence: MIT <https://opensource.org/licenses/MIT>
# -------------------------------------------------------------------------------
# This file is part of Ulra Light Weight Qtils.
#
# Copyright 2023 Daniel Kovacs
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of 
# this software and associated documentation files (the "Software"), to deal in 
# the Software without restriction, including without limitation the rights to use, 
# copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the 
# Software, and to permit persons to whom the Software is furnished to do so, 
# subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS 
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN 
# AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION 
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# -------------------------------------------------------------------------------


"""
String Utilities 
=============================

Common string transformation and conversation utilities. These are based on taken from
github gists and stack overflow answers. See notes of the origins in the specific functions.



"""



# -------------------------------------------------------------------------------
# imports
# -------------------------------------------------------------------------------

import re

from .collections import qlist


# -----------------------------------------------------------------------------
# exports
# -----------------------------------------------------------------------------

__all__ = qlist()


# -----------------------------------------------------------------------------
# camelize()
# -----------------------------------------------------------------------------

_RE_CAMELIZE = re.compile(r"(?:^|[_-])(.)")

@__all__.register
def camelize(value, uppercase_first_letter=True):
    """
    Convert values to CamelCase.

    See `origin here <https://github.com/jpvanhal/inflection/blob/master/inflection.py>`_


    Arguments:
        value (str): string to convert

        uppercase_first_letter (bool): if set to `True` :func:`camelize` converts
            strings to UpperCamelCase. If set to `False` :func:`camelize` produces
            lowerCamelCase. Defaults to `True`.

    
    Examples:

        >>> camelize('device_type')
        'DeviceType'
        >>> camelize('device-type')
        'DeviceType'
        >>> camelize('device_Type')
        'DeviceType'
        >>> camelize('device type')
        'DeviceType'
        >>> camelize('device_type', False)
        'deviceType'

        :func:`camelize` can be though as a inverse of :func:`underscorize`,
        but not in every case:
    
        >>> camelize(underscorize("IOError"))
        'IoError'
        >>> camelize(underscorize('SomeABTest'))
        'SomeAbTest'

    """
    value = value.replace(' ', '_')
    if uppercase_first_letter:
        return _RE_CAMELIZE.sub(lambda m: m.group(1).upper(), value)
    return value[0].lower() + camelize(value)[1:]


# -----------------------------------------------------------------------------
# underscorize()
# -----------------------------------------------------------------------------

_RE_UNDERCORIZE_1 = re.compile(r"([A-Z]+)([A-Z][a-z])")
_RE_UNDERCORIZE_2 = re.compile(r"([a-z\d])([A-Z])")

@__all__.register
def underscorize(value):
    """Make an underscore, lowercase form from input

    See `origin here <https://github.com/jpvanhal/inflection/blob/master/inflection.py>`_

    Arguments:
        value (str): Value to convert

    Examples:
        >>> underscorize('device')
        'device'
        >>> underscorize('DeviceType')
        'device_type'
        >>> underscorize('deviceType')
        'device_type'
        >>> underscorize('device-type')
        'device_type'
        >>> underscorize('device-Type')
        'device_type'
        >>> underscorize('DeviceTypeWithALotOfThings')
        'device_type_with_a_lot_of_things'

        :func:`underscorize` can be though as a inverse of :func:`camelize`,
        but not in every case:
    
        >>> camelize(underscorize("IOError"))
        'IoError'
        >>> camelize(underscorize('SomeABTest'))
        'SomeAbTest'

    """
    value = _RE_UNDERCORIZE_1.sub(r'\1_\2', value)
    value = _RE_UNDERCORIZE_2.sub(r'\1_\2', value)
    value = value.replace("-", "_").lower()
    return value


# -----------------------------------------------------------------------------
# titleize()
# -----------------------------------------------------------------------------

_RE_TITLEIZE = re.compile(r"([A-Z])")

@__all__.register
def titleize(value):
    """Convert strings to 'Title String'

    Arguments:
        value (str): Value to convert

    Examples:
        
        >>> titleize('device_type')
        'Device Type'
        >>> titleize('device-type')
        'Device Type'
        >>> titleize('deviceType')
        'Device Type'
        >>> titleize('device Type')
        'Device Type'

    """
    value = camelize(value)
    return _RE_TITLEIZE.sub(r" \1", value).strip(' ')


# -----------------------------------------------------------------------------
# firstline()
# -----------------------------------------------------------------------------

@__all__.register
def firstline(value):
    """Returns the first line of a string
    
    >>> text = "This is a long\\nmulti\\nline text with\\nmany line breaks"
    >>> firstline(text)
    'This is a long'

    """
    return value.split('\n', 1)[0] if value else ''



