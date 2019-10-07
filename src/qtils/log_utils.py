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
Logging Utilities module
=============================


Logging enhancements


Attributes:
    
    LOG_FORMATS: Pre-defined logging formats for convenience.

        Available formats:

        =========================== ===================================================================================
        Name                        Example
        =========================== ===================================================================================
        ``LOG_FORMATS.SHORT``       ``2019-10-10 11:11:11   INFO    mypackage.mymodule.MyClass:      Hello World``
        ``LOG_FORMATS.THREAD``      ``2019-10-10 11:11:11   INFO    [tid:11 (myThread)]    
                                    mypackage.mymodule.MyClass:      Hello World``   
        ``LOG_FORMATS.PROCESS``     ``2019-10-10 11:11:11   INFO    [pid:777]   mypackage.mymodule.
                                    MyClass:      Hello World``
        ``LOG_FORMATS.FULL``        ``2019-10-10 11:11:11   INFO    [pid:777 tid:11(myThread)]  mypackage.
                                    mymodule.MyClass:      Hello World``
        =========================== ===================================================================================


"""



# -------------------------------------------------------------------------------
# imports
# -------------------------------------------------------------------------------

import logging

from .collections import qlist, qdict


# -----------------------------------------------------------------------------
# exports
# -----------------------------------------------------------------------------

__all__ = qlist()


# -----------------------------------------------------------------------------
# LOG_FORMATS
# -----------------------------------------------------------------------------

__all__.append("LOG_FORMATS")
LOG_FORMATS = qdict(
    SHORT="%(asctime)s\t%(levelname)s\t%(name)s:\t%(message)s",
    THREAD="%(asctime)s\t%(levelname)s\t[tid:%(thread)x (%(threadName)s)]\t%(name)s:\t%(message)s",
    PROCESS="%(asctime)s\t%(levelname)s\t[pid:%(process)d]\t%(name)s:\t%(message)s",
    FULL="%(asctime)s\t%(levelname)s\t[pid:%(process)d tid:%(thread)x (%(threadName)s)]\t%(name)s:\t%(message)s",
)



# -----------------------------------------------------------------------------
# _create_class_logger
# -----------------------------------------------------------------------------

def _create_class_logger(cls, channel: str = None, root_channel: str = None, attr_name: str = "__logger"):
    """Create and assign a logger to a class object
    """
    channel = channel or cls.__name__
    root_channel = root_channel if root_channel is not None else cls.__module__
    if root_channel:
        channel = root_channel + '.' + channel
    if attr_name.startswith('__'): 
        attr_name = '_' + cls.__name__ + attr_name
    setattr(cls, attr_name, logging.getLogger(channel))


# -----------------------------------------------------------------------------
# @logged
# -----------------------------------------------------------------------------

@__all__.register
def logged(*args, **kwargs):
    """Decorator to create and assign a logger to a class
    
    Arguments:
        channel (str): Name of the logger, defaults to ``cls.__name__``

        root_channel (str): Prefix to the name of the logger,
            helpful to namespace a large ammount of logged objects.

        attr_name (str): Name of the logger attribute. Defaults
            to ``__logger``. 

            .. note:: Variables begining with double underscore
                are class private variables, meaning they are
                accessible ONLY to methods within the *same* class, 
                and not to descendant classes or from the outside. Read
                more about it in :py:ref:`tut-private` documentation.


    Examples:
        
        Simplest use case, adding a logger to a class:

        >>> @logged
        ... class LoggedFoo():
        ...     def __init__(self):
        ...         self.__logger.info("Hello World!")
        ...
        >>> foo = LoggedFoo()
        >>> # INFO:LoggedFoo:Hello World!     
        >>> #
        >>> # doctest doesn't allow testing logging output, 
        >>> # so just believe me on this one. :) 
        >>> # And also, there are proper test cases in pytest.

        
        Loggers are class-private by default:

        >>> @logged
        ... class LoggedFoo():
        ...     def __init__(self):
        ...         self.__logger.info("Hello World from Foo!")
        ...
        >>> class DescendantFoo(LoggedFoo):
        ...     def __init__(self):
        ...         super().__init__()
        ...         # The following line will fail because
        ...         # it has no access to the parent classes
        ...         # class-private logger.
        ...         self.__logger.info("Hello World from Descendant!") # 
        ...
        >>> foo = DescendantFoo()
        Traceback (most recent call last):
        ...
        AttributeError: 'DescendantFoo' object has no attribute '_DescendantFoo__logger'


        The recommended solution is to create loggers for each subclass. This means 
        their channel will always reflect the class name where the log line is 
        comming from. This is helpful in a large project with complicated inheritance 
        trees. 

        >>> @logged
        ... class LoggedFoo():
        ...     def __init__(self):
        ...         self.__logger.info("Hello World from Foo!")
        ...
        >>> @logged
        ... class DescendantFoo(LoggedFoo):
        ...     def __init__(self):
        ...         super().__init__()
        ...         self.__logger.info("Hello World from Descendant!") # 
        ...
        >>> foo = DescendantFoo()
        >>> # INFO:LoggedFoo:Hello World from Foo!     
        >>> # INFO:DescendantFoo:Hello World from Descendant!
        >>> #
        >>> # Note the Logger Name difference for the two lines.


        The second solution is to create a logger with a non-private attribute name.
        This could be useful for situations when there is a bunch of small descendant
        classes which doesn't need their own logger. This typically happens in
        marshallers when each type has it's own little class for serializing/deserializing.


        >>> @logged(attr_name="logger")
        ... class LoggedFoo():
        ...     def __init__(self):
        ...         self.logger.info("Hello World from Foo!")
        ...
        >>> class DescendantFoo(LoggedFoo):
        ...     def __init__(self):
        ...         super().__init__()
        ...         self.logger.info("Hello World from Descendant!") # 
        ...
        >>> foo = DescendantFoo()
        >>> # INFO:LoggedFoo:Hello World from Foo!     
        >>> # INFO:LoggedFoo:Hello World from Descendant!
        >>>
        >>> # Both logs seem to come from the same line



    """
    if len(args) == 1 and isinstance(args[0], type):
        _create_class_logger(args[0])
        return args[0]
    def _logged(cls):
        _create_class_logger(cls, *args, **kwargs)
        return cls
    return _logged

