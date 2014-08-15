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

    def test_crossword_can_get_set_metadata(self):
        crossword = Crossword(1, 1)
        self.assertEqual(len(crossword.meta), 15)

        crossword.meta['creator'] = 'A'
        self.assertEqual(crossword.meta.creator, 'A')

        crossword.meta.creator = 'B'
        self.assertEqual(crossword.meta.creator, 'B')

        setattr(crossword.meta, 'creator', 'C')
        self.assertEqual(crossword.meta['creator'], 'C')
        self.assertEqual(getattr(crossword.meta, 'creator'), 'C')

        with self.assertRaises(AttributeError):
            self.crossword.meta.doesnotexist
