import unittest

from crossword import Crossword


class CrosswordTestCase(unittest.TestCase):

    def test_crossword_set_and_get_element(self):
        crossword = Crossword(10, 10)
        crossword[3, 3] = 'A'
        self.assertEqual(crossword[3, 3], 'A')

    def test_crossword_iteration_over_rows_and_columns(self):
        crossword = Crossword(10, 5)
        for row in crossword:
            self.assertEqual(len(row), 10)
        self.assertEqual(len([row for row in crossword]), 5)
