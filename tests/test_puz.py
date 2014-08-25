import unittest

import crossword

import puz


class PUZUnitTest(unittest.TestCase):

    def test_read_puz_to_crossword(self):
        puz_object = puz.read('fixtures/chronicle_20140815.puz')
        puzzle = crossword.from_puz(puz_object)
        self.assertEqual(
            puzzle.meta.title,
            'Que Pasa? - August 15, 2014'
        )
        self.assertEqual(
            puzzle.meta.creator,
            'by Ian Livengood / Edited by Brad Wilber '
        )
        self.assertEqual(puzzle.block, '.')
        self.assertEqual(puzzle.clues.across[67], 'Jupiter, but not Zeus')
        self.assertEqual(puzzle.clues.down[60], 'Cadenza automaker')

    def test_read_puz_locked_puzzle(self):
        puz_object = puz.read('fixtures/nyt_locked.puz')
        puzzle = crossword.from_puz(puz_object)
        for x, y in puzzle.cells:
            self.assertEqual(puzzle[x, y].cell, None)
        self.assertEqual(puzzle[0, 0].solution, 'B')
        self.assertEqual(puzzle[14, 14].solution, 'N')

    def test_read_and_write_round_trip(self):
        puz_object = puz.read('fixtures/chronicle_20140815.puz')
        puzzle = crossword.from_puz(puz_object)
        new_puz_object = crossword.to_puz(puzzle)
        for attr in dir(puz_object):
            if not callable(getattr(puz_object, attr)):
                self.assertEqual(
                    getattr(puz_object, attr),
                    getattr(new_puz_object, attr)
                )
