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

        self.assertEqual(list(crossword.meta()), [
            ('contributor', None),
            ('coverage', None),
            ('creator', 'C'),
            ('date', None),
            ('description', None),
            ('format', None),
            ('identifier', None),
            ('language', None),
            ('publisher', None),
            ('relation', None),
            ('rights', None),
            ('source', None),
            ('subject', None),
            ('title', None),
            ('type', None),
        ])

        with self.assertRaises(AttributeError):
            crossword.meta.doesnotexist

    def test_crossword_can_get_set_clues(self):
        crossword = Crossword(1, 1)
        crossword.clues.across[1] = "The clue"
        self.assertEqual(crossword.clues.across[1], "The clue")
        self.assertEqual(len(crossword.clues.across), 1)

        self.assertEqual(len(crossword.clues.down), 0)
        crossword.clues.down[1] = "Other clue"
        self.assertEqual(crossword.clues.down[1], "Other clue")
        self.assertEqual(crossword.clues.across[1], "The clue")

        self.assertEqual(crossword.clues.across, {
            1: "The clue",
        })
        self.assertEqual(crossword.clues.down, {
            1: "Other clue",
        })

        with self.assertRaises(AttributeError):
            crossword.clues.doesnotexist

    def test_crossword_can_iterate_over_all_clues(self):
        crossword = Crossword(5, 5)
        crossword.clues.across[1] = "This is an across clue 1"
        crossword.clues.across[3] = "This is an across clue 3"
        crossword.clues.across[2] = "This is an across clue 2"
        crossword.clues.down[2] = "This is a down clue"
        clues = list(crossword.clues.all())
        self.assertEqual(clues, [
            ('across', 1, "This is an across clue 1"),
            ('across', 2, "This is an across clue 2"),
            ('across', 3, "This is an across clue 3"),
            ('down', 2, "This is a down clue"),
        ])

    def test_crossword_can_iterate_over_clues_of_direction(self):
        crossword = Crossword(5, 5)
        crossword.clues.across[1] = "This is an across clue"
        crossword.clues.down[2] = "This is a down clue"
        self.assertEqual(list(crossword.clues.across()), [
            (1, "This is an across clue"),
        ])
        self.assertEqual(list(crossword.clues.down()), [
            (2, "This is a down clue"),
        ])

    def test_crossword_supports_explicit_iteration(self):
        crossword = Crossword(15, 15)
        for y in range(crossword.height):
            for x in range(crossword.width):
                self.assertEqual(crossword[x, y], None)

        for x, y in crossword.cells:
            self.assertEqual(crossword[x, y], None)

        self.assertEqual(len(list(crossword.cells)), crossword.width * crossword.height)

        with self.assertRaises(AttributeError):
            crossword.cells = None

    def test_crossword_can_be_converted_to_json(self):
        crossword = Crossword(5, 10)
        crossword.meta.creator = "The author"
        crossword.clues.across[1] = "This is a clue"
        self.assertEqual(crossword.json, {
            'width': 5,
            'height': 10,
            'cells': [[None] * 5] * 10,
            'metadata': {
                'contributor': None,
                'coverage': None,
                'creator': "The author",
                'date': None,
                'description': None,
                'format': None,
                'identifier': None,
                'language': None,
                'publisher': None,
                'relation': None,
                'rights': None,
                'source': None,
                'subject': None,
                'title': None,
                'type': None,
            },
            'clues': {
                'across': {
                    1: "This is a clue",
                },
                'down': {},
            }
        })
