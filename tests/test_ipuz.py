import unittest

import ipuz

import crossword


class IPUZUnitTest(unittest.TestCase):

    def test_read_first_ipuz_fixture(self):
        with open('fixtures/first.ipuz') as f:
            ipuz_dict = ipuz.read(f.read())

        puzzle = crossword.from_ipuz(ipuz_dict)
        self.assertEqual(puzzle.width, 13)
        self.assertEqual(puzzle.height, 13)
        self.assertEqual(puzzle.meta.creator, "Arthur Wynne")
        self.assertEqual(puzzle.meta.date, "12/21/1913")
        self.assertEqual(puzzle.meta.title, "FUN's Word-Cross Puzzle")
        self.assertEqual(puzzle.clues.across["2-3"], "What bargain hunters enjoy")
        self.assertEqual(puzzle.clues.down["1-32"], "To govern")
        self.assertEqual(puzzle[0, 0].puzzle, None)
        self.assertEqual(puzzle[0, 0].solution, None)
        self.assertEqual(puzzle[6, 0].puzzle, 1)
        self.assertEqual(puzzle[6, 0].solution, "R")

        puzzle[6, 0]['solution'] = "X"
        self.assertEqual(puzzle[6, 0].solution, "X")
        puzzle[6, 0].solution = "Y"
        self.assertEqual(puzzle[6, 0]['solution'], "Y")
        setattr(puzzle[6, 0], "solution", "Z")
        self.assertEqual(puzzle[6, 0].solution, "Z")

    def test_read_example_ipuz_fixture(self):
        with open('fixtures/example.ipuz') as f:
            ipuz_dict = ipuz.read(f.read())

        puzzle = crossword.from_ipuz(ipuz_dict)
        self.assertEqual(puzzle.meta.rights, "2011 Puzzazz")
