import unittest

from crossword import Crossword


class CrosswordTestCase(unittest.TestCase):

    def test_crossword_width_needs_to_be_one_or_more(self):
        with self.assertRaises(ValueError) as cm:
            Crossword(0, 10)
        self.assertEqual(str(cm.exception), "Width needs to be at least one")

    def test_crossword_height_needs_to_be_one_or_more(self):
        with self.assertRaises(ValueError) as cm:
            Crossword(10, 0)
        self.assertEqual(str(cm.exception), "Height needs to be at least one")

    def test_crossword_set_and_get_element(self):
        crossword = Crossword(10, 10)
        with self.assertRaises(ValueError) as cm:
            crossword[3, 3] = 'X'
        self.assertEqual(
            str(cm.exception),
            "You cannot assign to a cell directly. "
            "Did you mean puzzle[3, 3].cell = ...?"
        )

    def test_crossword_can_set_dict_as_cell(self):
        crossword = Crossword(3, 3)
        crossword[0, 0] = {'cell': 'A'}
        self.assertEqual(crossword[0, 0].cell, 'A')

    def test_crossword_can_set_attributes_as_needed(self):
        crossword = Crossword(10, 10)
        crossword[3, 3].cell = 'A'
        self.assertEqual(crossword[3, 3].cell, 'A')

    def test_crossword_can_set_consecutive_values(self):
        crossword = Crossword(3, 3)
        crossword[0, 0].cell = 'A'
        self.assertEqual(crossword[0, 0].cell, 'A')
        crossword[0, 0].cell = 'B'
        self.assertEqual(crossword[0, 0].cell, 'B')

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
        crossword.clues.across[2] = "This is an across clue 2"
        crossword.clues.across[3] = "This is an across clue 3"
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
        crossword.clues.across[2] = "This is an across clue"
        crossword.clues.across[3] = "This is an across clue"
        crossword.clues.down[2] = "This is a down clue"
        self.assertEqual(list(crossword.clues.across()), [
            (1, "This is an across clue"),
            (2, "This is an across clue"),
            (3, "This is an across clue"),
        ])
        self.assertEqual(list(crossword.clues.down()), [
            (2, "This is a down clue"),
        ])

    def test_crossword_supports_explicit_iteration(self):
        crossword = Crossword(15, 15)
        for y in range(crossword.height):
            for x in range(crossword.width):
                self.assertEqual(crossword[x, y], {})

        for x, y in crossword.cells:
            self.assertEqual(crossword[x, y], {})

        self.assertEqual(
            len(list(crossword.cells)),
            crossword.width * crossword.height
        )

        with self.assertRaises(AttributeError):
            crossword.cells = None

    def test_crossword_can_be_converted_to_dictionary(self):
        crossword = Crossword(5, 10)
        crossword.meta.creator = "The author"
        crossword.clues.across[1] = "This is a clue"
        self.assertEqual(crossword.content, {
            'width': 5,
            'height': 10,
            'cells': [[{}] * 5] * 10,
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
            },
            'block': None,
            'empty': None,
            'format': {},
        })

    def test_clues_are_sorted_in_numerical_order(self):
        crossword = Crossword(15, 15)
        crossword.clues.across[1] = "Clue 1"
        crossword.clues.across[10] = "Clue 10"
        crossword.clues.across[2] = "Clue 2"
        self.assertEqual(
            list(crossword.clues.across()),
            [
                (1, "Clue 1"),
                (2, "Clue 2"),
                (10, "Clue 10"),
            ]
        )

    def test_clues_are_sorted_in_provided_order_when_not_sorting(self):
        crossword = Crossword(15, 15)
        crossword.clues.across["1"] = "Clue 1"
        crossword.clues.across["10"] = "Clue 10"
        crossword.clues.across["2"] = "Clue 2"
        self.assertEqual(
            list(crossword.clues.across(sort=None)),
            [
                ("1", "Clue 1"),
                ("10", "Clue 10"),
                ("2", "Clue 2"),
            ]
        )

    def test_clues_can_be_sorted_using_function(self):
        crossword = Crossword(15, 15)
        crossword.clues.across[1] = "Clue 1"
        crossword.clues.across[10] = "Clue 10"
        crossword.clues.across[2] = "Clue 2"
        self.assertEqual(
            list(crossword.clues.across(sort=int)),
            [
                (1, "Clue 1"),
                (2, "Clue 2"),
                (10, "Clue 10"),
            ]
        )

    def test_clues_in_both_directions_sorted_with_function(self):
        crossword = Crossword(15, 15)
        crossword.clues.across[1] = "Clue 1"
        crossword.clues.across[10] = "Clue 10"
        crossword.clues.across[2] = "Clue 2"
        crossword.clues.down[1] = "Clue 1"
        crossword.clues.down[10] = "Clue 10"
        crossword.clues.down[2] = "Clue 2"
        self.assertEqual(
            list(crossword.clues.all(sort=int)),
            [
                ('across', 1, "Clue 1"),
                ('across', 2, "Clue 2"),
                ('across', 10, "Clue 10"),
                ('down', 1, "Clue 1"),
                ('down', 2, "Clue 2"),
                ('down', 10, "Clue 10"),
            ]
        )
