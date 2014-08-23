from puz import Puzzle

from crossword.core import Crossword


def from_puz(puzzle):
    result = Crossword(puzzle.width, puzzle.height)
    result.meta.creator = puzzle.author
    result.meta.rights = puzzle.copyright
    result.meta.title = puzzle.title
    return result


def to_puz(crossword):
    pass
