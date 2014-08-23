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
        self.assertEqual(
            puzzle.clues.across["2-3"],
            "What bargain hunters enjoy"
        )
        self.assertIsNone(puzzle.block)
        self.assertIsNone(puzzle.empty)

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
        self.assertEqual(puzzle.empty, "0")

    def test_read_and_write_round_trip(self):
        with open('fixtures/example.ipuz') as f:
            ipuz_dict = ipuz.read(f.read())

        puzzle = crossword.from_ipuz(ipuz_dict)
        new_ipuz_dict = crossword.to_ipuz(puzzle)
        for key, value in ipuz_dict.items():
            self.assertEqual(value, new_ipuz_dict[key])
        for key, value in new_ipuz_dict.items():
            if key in ipuz_dict:
                self.assertEqual(value, ipuz_dict[key])
            else:
                self.assertIsNone(value)

    def test_read_example_may_not_have_solution(self):
        with open('fixtures/example.ipuz') as f:
            ipuz_dict = ipuz.read(f.read())

        del ipuz_dict["solution"]
        puzzle = crossword.from_ipuz(ipuz_dict)
        self.assertEqual(puzzle[0, 0].puzzle, 1)
        self.assertEqual(puzzle[0, 0].solution, None)

    def test_read_example_may_not_have_all_cells_defined(self):
        with open('fixtures/example.ipuz') as f:
            ipuz_dict = ipuz.read(f.read())

        ipuz_dict["puzzle"] = [row[:5] for row in ipuz_dict["puzzle"]]
        ipuz_dict["solution"] = [row[:5] for row in ipuz_dict["solution"]]
        puzzle = crossword.from_ipuz(ipuz_dict)
        self.assertEqual(puzzle[10, 10].puzzle, None)
        self.assertEqual(puzzle[10, 10].solution, None)

    def test_read_example_may_not_have_clues(self):
        with open('fixtures/example.ipuz') as f:
            ipuz_dict = ipuz.read(f.read())

        del ipuz_dict["clues"]["Across"]
        del ipuz_dict["clues"]["Down"]
        puzzle = crossword.from_ipuz(ipuz_dict)
        self.assertEqual(list(puzzle.clues.across()), [])
        self.assertEqual(list(puzzle.clues.down()), [])

    def test_write_to_ipuz_only_includes_empty_block(self):
        with open('fixtures/example.ipuz') as f:
            ipuz_dict = ipuz.read(f.read())

        puzzle = crossword.from_ipuz(ipuz_dict)
        puzzle.block = None
        puzzle.empty = None
        new_ipuz_dict = crossword.to_ipuz(puzzle)
        self.assertNotIn("empty", new_ipuz_dict)
        self.assertNotIn("block", new_ipuz_dict)

    def test_empty_puzzles_has_mostly_mandatory_ipuz_elements(self):
        puzzle = crossword.Crossword(15, 15)
        ipuz_dict = crossword.to_ipuz(puzzle)
        self.assertEqual(ipuz_dict, {
            "version": "http://ipuz.org/v1",
            "dimensions": {
                "width": 15,
                "height": 15,
            },
            "puzzle": [[None for _ in range(15)] for _ in range(15)],
            "solution": [[None for _ in range(15)] for _ in range(15)]
        })

    def test_from_ipuz_raise_exception_for_non_crossword(self):
        ipuz_dict = {
            "kind": ["http://ipuz.org/sudoku#1"],
        }
        with self.assertRaises(crossword.CrosswordException):
            crossword.from_ipuz(ipuz_dict)
