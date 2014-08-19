# -*- coding: utf-8 -*-
import collections
import sys

__title__ = 'crossword'
__version__ = '0.1.1'
__author__ = 'Simeon Visser'
__email__ = 'simeonvisser@gmail.com'
__license__ = 'MIT'
__copyright__ = 'Copyright 2014 Simeon Visser'

PY3 = sys.version_info[0] == 3

if PY3:
    range = range
    str = str
else:
    range = xrange
    str = unicode


class CrosswordCell(dict):

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError

    def __setattr__(self, name, value):
        self[name] = value


class CrosswordMetadata(dict):

    def __init__(self):
        # Dublin Core Metadata Element Set, Version 1.1
        self['contributor'] = None
        self['coverage'] = None
        self['creator'] = None
        self['date'] = None
        self['description'] = None
        self['format'] = None
        self['identifier'] = None
        self['language'] = None
        self['publisher'] = None
        self['relation'] = None
        self['rights'] = None
        self['source'] = None
        self['subject'] = None
        self['title'] = None
        self['type'] = None

    def __call__(self):
        for item in sorted(self.items()):
            yield item

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError

    def __setattr__(self, name, value):
        self[name] = value


class CrosswordDirectionClues(collections.OrderedDict):

    def __init__(self, *args, **kwargs):
        super(CrosswordDirectionClues, self).__init__(*args, **kwargs)

    def __call__(self, sort=int):
        if sort is not None:
            items = sorted(self.items(), key=lambda item: sort(item[0]))
        else:
            items = self.items()
        for item in items:
            yield item


class CrosswordClues(dict):

    ACROSS = 'across'

    DOWN = 'down'

    def __init__(self):
        self._directions = (CrosswordClues.ACROSS, CrosswordClues.DOWN)
        for direction in self._directions:
            self[direction] = CrosswordDirectionClues()

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError

    def all(self, sort=int):
        for direction in self._directions:
            for number, clue in self[direction](sort=sort):
                yield direction, number, clue


class Crossword(object):

    def __init__(self, width, height):
        if width <= 0:
            raise ValueError("Width needs to be at least one")
        if height <= 0:
            raise ValueError("Height needs to be at least one")
        self.width = width
        self.height = height
        self._data = [[None for _ in range(width)] for _ in range(height)]
        self.meta = CrosswordMetadata()
        self.clues = CrosswordClues()
        self._format = {}  # file format-specific data
        self.block = None
        self.empty = None

    @property
    def cells(self):
        for y in range(self.height):
            for x in range(self.width):
                yield x, y

    @property
    def content(self):
        return {
            'width': self.width,
            'height': self.height,
            'cells': self._data,
            'metadata': self.meta,
            'clues': {
                'across': self.clues.across,
                'down': self.clues.down,
            },
            'block': self.block,
            'empty': self.empty,
            'format': self._format,
        }

    def __getitem__(self, index):
        if isinstance(index, tuple):
            x, y = index
            return self._data[y][x]
        return self._data[index]

    def __setitem__(self, index, value):
        x, y = index
        self._data[y][x] = value

    def __str__(self):
        result = []
        for row in self:
            for cell in row:
                result.append(str(cell) if cell is not None else u' ')
            result.append(u'\n')
        return u''.join(result)


def from_ipuz(ipuz_dict):
    known_keys = (
        "dimensions",
        "editor",
        "author",
        "date",
        "notes",
        "uniqueid",
        "publisher",
        "copyright",
        "title",
        "block",
        "empty",
        "clues",
        "puzzle",
        "solution",
    )
    crossword = Crossword(
        ipuz_dict['dimensions']['width'],
        ipuz_dict['dimensions']['height']
    )
    crossword.meta.contributor = ipuz_dict.get('editor')
    crossword.meta.creator = ipuz_dict.get('author')
    crossword.meta.date = ipuz_dict.get('date')
    crossword.meta.description = ipuz_dict.get('notes')
    crossword.meta.identifier = ipuz_dict.get('uniqueid')
    crossword.meta.publisher = ipuz_dict.get('publisher')
    crossword.meta.rights = ipuz_dict.get('copyright')
    crossword.meta.title = ipuz_dict.get('title')
    crossword.block = ipuz_dict.get('block')
    crossword.empty = ipuz_dict.get('empty')

    for number, clue in ipuz_dict.get('clues', {}).get('Across', []):
        crossword.clues.across[number] = clue
    for number, clue in ipuz_dict.get('clues', {}).get('Down', []):
        crossword.clues.down[number] = clue

    for x, y in crossword.cells:
        crossword[x, y] = CrosswordCell()

    for key in ('puzzle', 'solution'):
        entry = ipuz_dict.get(key)
        for x, y in crossword.cells:
            crossword[x, y][key] = entry[y][x] if entry is not None else None

    for key, value in ipuz_dict.items():
        if key not in known_keys:
            crossword._format[key] = value

    return crossword


def to_ipuz(crossword):
    ipuz_dict = {
        "version": "http://ipuz.org/v1",
        "dimensions": {
            "width": crossword.width,
            "height": crossword.height,
        },
        "puzzle": [
            [getattr(cell, "puzzle", None) for cell in row]
            for row in crossword._data
        ],
        "solution": [
            [getattr(cell, "solution", None) for cell in row]
            for row in crossword._data
        ],
    }
    if crossword.meta.creator is not None:
        ipuz_dict["author"] = crossword.meta.creator
    if crossword.meta.rights is not None:
        ipuz_dict["copyright"] = crossword.meta.rights
    if crossword.meta.date is not None:
        ipuz_dict["date"] = crossword.meta.date
    if crossword.meta.contributor is not None:
        ipuz_dict["editor"] = crossword.meta.contributor
    if crossword.meta.description is not None:
        ipuz_dict["notes"] = crossword.meta.description
    if crossword.meta.publisher is not None:
        ipuz_dict["publisher"] = crossword.meta.publisher
    if crossword.meta.identifier is not None:
        ipuz_dict["uniqueid"] = crossword.meta.identifier
    if crossword.meta.title is not None:
        ipuz_dict["title"] = crossword.meta.title
    if crossword.block is not None:
        ipuz_dict["block"] = crossword.block
    if crossword.empty is not None:
        ipuz_dict["empty"] = crossword.empty

    across_clues = [list(item) for item in crossword.clues.across()]
    down_clues = [list(item) for item in crossword.clues.down()]
    if across_clues or down_clues:
        ipuz_dict["clues"] = {}
        if across_clues:
            ipuz_dict["clues"]['Across'] = across_clues
        if down_clues:
            ipuz_dict["clues"]['Down'] = down_clues

    ipuz_dict.update(crossword._format)
    return ipuz_dict
