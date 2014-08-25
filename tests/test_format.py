import unittest

import ipuz
import puz

import crossword


class FormatUnitTest(unittest.TestCase):

    def test_to_ipuz_only_include_ipuz_specific_data(self):
        puz_object = puz.read('fixtures/puz/chronicle_20140815.puz')
        puzzle = crossword.from_puz(puz_object)
        ipuz_dict = crossword.to_ipuz(puzzle)
        self.assertNotIn('puzzletype', ipuz_dict)
        self.assertNotIn('fileversion', ipuz_dict)
        self.assertNotIn('extensions', ipuz_dict)

    def test_to_puz_only_include_puz_specific_data(self):
        with open('fixtures/ipuz/example.ipuz') as f:
            ipuz_dict = ipuz.read(f.read())

        puzzle = crossword.from_ipuz(ipuz_dict)
        puz_object = crossword.to_puz(puzzle)
        self.assertFalse(hasattr(puz_object, "kind"))

    def test_to_puz_only_works_if_numbering_system_matches(self):
        with open('fixtures/ipuz/first.ipuz') as f:
            ipuz_dict = ipuz.read(f.read())

        puzzle = crossword.from_ipuz(ipuz_dict)
        with self.assertRaises(crossword.CrosswordException):
            puz_object = crossword.to_puz(puzzle)
