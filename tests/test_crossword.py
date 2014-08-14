import unittest

from crossword import Crossword


class CrosswordTestCase(unittest.TestCase):

    def test_basic_crossword_set_and_get_element(self):
        c = Crossword(10, 10)
        c[3, 3] = 'A'
        self.assertEqual(c[3, 3], 'A')
