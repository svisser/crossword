crossword
=========

Python library for handling crossword puzzles. This library provides a canonical data structure
that can be used to represent crosswords in your application. It provides a Pythonic way to
perform common operations on the grid, the words and the clues of the puzzle.

The library handles reading and writing to .ipuz files.

## Installation

You can install using pip:

    pip install crossword

## Creating and modifying crosswords

You can create a crossword:

    from crossword import Crossword

    puzzle = Crossword(15, 15)

You can iterate over rows and cells:

    for row in puzzle:
        for cell in row:
            pass

You also iterate using 'cells' (left-to-right, top-to-bottom):

    for x, y in puzzle.cells:
        print(puzzle[x, y])

You can store a string as cell value but you can also specify attributes
to store multiple values (such as cell content, styling and other cell propeties):

    puzzle[x, y] = "A"

    puzzle[x, y].puzzle = " "
    puzzle[x, y].solution = "A"
    puzzle[x, y].style = {'background-color': 'red'}

You can access a metadata attribute:

    creator = puzzle.meta.creator

You can iterate over metadata:

    for key, value in puzzle.meta():
        print(key, value)

You can set a clue for an entry:

    puzzle.clues.across[1] = "This is a clue"
    puzzle.clues.down[2] = "This is a clue"

You can iterate over all clues (first Across, then Down):

    for direction, number, clue in puzzle.clues.all():
        print(direction, number, clue)

You can iterate over clues in a particular direction:

    for number, clue in puzzle.clues.across():
        print(number, clue)
    for number, clue in puzzle.clues.down():
        print(number, clue)

By default these functions iterate over the clues by numerical order
of the specified clue numbers. If you wish to iterate over the clues in the
order that they were inserted you can specify sort=None:

    puzzle.clues.all(sort=None)

You can also specify a function yourself that will be used for sorting:

    puzzle.clues.all(sort=lambda entry: ...)

You can use the following attributes as dictionaries (e.g., for conversion to JSON):

    puzzle.content (the cells, clues and metadata in one dictionary)
    puzzle.clues
    puzzle.clues.across
    puzzle.clues.down
    puzzle.meta

You can use the following constants for values that represent block cells and empty cells:

    puzzle.block
    puzzle.empty

A value of None may indicate that the default value is used (e.g., "#" for blocks in
.ipuz puzzles).

## Reading and writing crosswords

You can read a crossword from an .ipuz file using:

    with open('puzzle.ipuz') as puzzle_file:
        ipuz_dict = ipuz.read(puzzle_file.read())  # may raise ipuz.IPUZException

    puzzle = crossword.from_ipuz(ipuz_dict)

This requires the "ipuz" package to be installed: http://pypi.python.org/pypi/ipuz.

You can write a crossword to an .ipuz file using:

    ipuz_dict = crossword.to_ipuz(puzzle)

    with open('puzzle.ipuz', 'w') as puzzle_file:
        puzzle_file.write(ipuz.write(ipuz_dict))
