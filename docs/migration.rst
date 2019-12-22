
.. _migration_from_sutils:

======================================================================
Migrating from `sutils` to `qtils`
======================================================================


1. Change `requirements.txt`
=============================

- Remove any reference to `sutils`. It will be very likely referred using the github address.
- Simply add `qtils` instead
 

2. Uninstall `sutils`, install `qtils`
========================================

The cleanest way of doing this is to recreate the virtualenv. If you are on `gpf` it should be as simple as::

    make clean
    make deps


If you don't want to do that for some reason (you should have no good reason though), then use pip::

    pip uninstall sutils
    pip install qtils


3. Changing references in the source code
==================================================================

Search and replace `sutils` to `qtils` in your python sources using your favorite text editor.


4. Fixing API changes
==================================================================

.. note::
    
    This section is a work-in-progress, more steps might be added in an on-going fashion.


--------------
PrettyObject
--------------

Referencing pretty format presets
-----------------------------------

Change old API::

    PrettyObject.__PRETTY_FORMATS__.short


To new API::

    PRETTY_FORMAT.SHORT


Regex for find and replace::

    # find: 
    PrettyObject.__PRETTY_FORMATS__.([a-z]+)

    # replace with:
    PRETTY_FORMAT.\U$1


--------------
Logging
--------------

Referencing logging format presets
-----------------------------------

Change old API:

.. code-block:: python

    LOG_FORMATS.process


To new API:


.. code-block:: python

    LOG_FORMATS.PROCESS


Regex for find and replace::

    # find: 
    LOG_FORMATS.([a-z]+)

    # replace with:
    LOG_FORMATS.\U$1


--------------
`file_size()`
--------------

The file_size function was replaced with the more versatile DataSize class.


Change old API::

    print(file_size(1234))


To new API::

    print(DataSize(1234))


Regex for find and replace::

    # find: 
    file_size

    # replace with:
    DataSize



