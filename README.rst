crossword
=========

.. image:: https://pypip.in/version/crossword/badge.svg
    :target: https://pypi.python.org/pypi/crossword/
    :alt: Latest Version

.. image:: https://pypip.in/download/crossword/badge.svg
    :target: https://pypi.python.org/pypi/crossword/
    :alt: Downloads

.. image:: https://pypip.in/py_versions/crossword/badge.svg
    :target: https://pypi.python.org/pypi/crossword/
    :alt: Supported Python versions

.. image:: https://pypip.in/license/crossword/badge.svg
    :target: https://pypi.python.org/pypi/crossword/
    :alt: License

Python library for handling crossword puzzles. This library provides a canonical data structure
that can be used to represent crosswords in your application. It provides a Pythonic way to
perform common operations on the grid, the words and the clues of the puzzle.

The library is intended for American crossword style puzzles, such as the New York Times
crossword, though variations within reason will also be supported.

The library handles reading and writing to .ipuz files.


Installation
------------

You can install using pip:

.. code-block:: bash

    $ pip install crossword


Creating and modifying crosswords
---------------------------------

You can create a crossword:

.. code:: python

    from crossword import Crossword

    puzzle = Crossword(15, 15)

You can iterate over rows and cells:

.. code:: python

    for row in puzzle:
        for cell in row:
            pass

You also iterate using 'cells' (left-to-right, top-to-bottom):

.. code:: python

    for x, y in puzzle.cells:
        print(puzzle[x, y])

You can store a string as cell value but you can also specify attributes
to store multiple values (such as cell content, styling and other cell propeties):

.. code:: python

    puzzle[x, y] = "A"

    puzzle[x, y].puzzle = " "
    puzzle[x, y].solution = "A"
    puzzle[x, y].style = {'background-color': 'red'}

You can access a metadata attribute:

.. code:: python

    creator = puzzle.meta.creator

Each puzzle has the attributes specified in the Dublin Core Metadata Element Set,
Version 1.1, which include creator, date, description, identifier and title. By default
these attributes have the value None.

You can iterate over metadata:

.. code:: python

    for key, value in puzzle.meta():
        print(key, value)

You can set a clue for an entry:

.. code:: python

    puzzle.clues.across[1] = "This is a clue"
    puzzle.clues.down[2] = "This is a clue"

You can iterate over all clues (first Across, then Down):

.. code:: python

    for direction, number, clue in puzzle.clues.all():
        print(direction, number, clue)

You can iterate over clues in a particular direction:

.. code:: python

    for number, clue in puzzle.clues.across():
        print(number, clue)
    for number, clue in puzzle.clues.down():
        print(number, clue)

By default these functions iterate over the clues by numerical order
of the specified clue numbers. If you wish to iterate over the clues in the
order that they were inserted you can specify sort=None:

.. code:: python

    puzzle.clues.all(sort=None)

You can also specify a function yourself that will be used for sorting:

.. code:: python

    puzzle.clues.all(sort=lambda entry: ...)

You can use the following attributes as dictionaries (e.g., for conversion to JSON):

.. code:: python

    puzzle.content (the cells, clues and metadata in one dictionary)
    puzzle.clues
    puzzle.clues.across
    puzzle.clues.down
    puzzle.meta

You can use the following constants for values that represent block cells and empty cells:

.. code:: python

    puzzle.block
    puzzle.empty

A value of None may indicate that the default value is used (e.g., "#" for blocks in
.ipuz puzzles).

Reading and writing crosswords
------------------------------

You can read a crossword from an .ipuz file using:

.. code:: python

    with open('puzzle.ipuz') as puzzle_file:
        ipuz_dict = ipuz.read(puzzle_file.read())  # may raise ipuz.IPUZException

    puzzle = crossword.from_ipuz(ipuz_dict)

This requires the "ipuz" package to be installed: https://pypi.python.org/pypi/ipuz.

You can write a crossword to an .ipuz file using:

.. code:: python

    ipuz_dict = crossword.to_ipuz(puzzle)

    with open('puzzle.ipuz', 'w') as puzzle_file:
        puzzle_file.write(ipuz.write(ipuz_dict))


Contributing
------------

Contributions are very welcome. If you've found an issue or if you'd like to
suggest a feature please open a ticket at: https://github.com/svisser/crossword/issues.

You should create a virtual environment first before installing the
packages as described below. This keeps the dependencies separate from other Python packages
on your system. See: https://pypi.python.org/pypi/virtualenv.

You can install the packages needed for developing and testing this library by running:

.. code-block:: bash

    $ pip install -r dev-requirements.txt

There are also various tests included. You can run these with:

.. code-block:: bash

    $ tox

This will run the tests in various Python versions to ensure that the library
works properly in each of them.

Ideas for new features
----------------------

* Add support for Across Lite .puz files (https://github.com/alexdej/puzpy)
* Add support for Crossword Compiler .ccw files (http://crossword-compiler.com)
* Add support for CrossDown .xwd files (http://www.crossdown.com/)
* Add support for XPF files (http://www.xwordinfo.com/XPF/)
