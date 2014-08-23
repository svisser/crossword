from puz import Puzzle

from crossword.compat import range
from crossword.core import Crossword


def from_puz(puzzle):
    known_keys = (
        "width",
        "height",
        "author",
        "copyright"
        "title",
        "solution",
    )
    result = Crossword(puzzle.width, puzzle.height)
    result._format_identifier = Crossword.PUZ
    result.meta.creator = puzzle.author
    result.meta.rights = puzzle.copyright
    result.meta.title = puzzle.title

    rows = []
    for i in range(0, len(puzzle.solution), puzzle.width):
        rows.append(puzzle.solution[i:i + puzzle.width])
    for y, row in enumerate(rows):
        for x, cell in enumerate(row):
            result[x, y].cell = None
            result[x, y].solution = cell

    result.block = '.'

    for attr in dir(puzzle):
        if attr in known_keys:
            continue
        if attr.startswith('__'):
            continue
        if callable(getattr(puzzle, attr)):
            continue
        result._format[attr] = getattr(puzzle, attr)

    return result


def to_puz(crossword):
    result = Puzzle()
    result.width = crossword.width
    result.height = crossword.height
    result.author = crossword.meta.creator
    result.copyright = crossword.meta.rights
    result.title = crossword.meta.title

    cells = []
    for row in crossword:
        for cell in row:
            value = None
            if cell.solution is None:
                value = crossword.block if crossword.block else '.'
            else:
                value = cell.solution
            cells.append(value)
    result.solution = ''.join(cells)

    if crossword._format_identifier == Crossword.PUZ:
        for key, value in crossword._format.items():
            setattr(result, key, value)

    return result
