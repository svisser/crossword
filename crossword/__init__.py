
__title__ = 'crossword'
__version__ = '0.1'
__author__ = 'Simeon Visser'
__license__ = 'MIT'
__copyright__ = 'Copyright 2014 Simeon Visser'

try:
    range = xrange
except NameError:
    pass

try:
    unicode
except NameError:
    unicode = str


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

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError

    def __setattr__(self, name, value):
        self[name] = value


class CrosswordClues(dict):

    def __init__(self):
        self['across'] = {}
        self['down'] = {}

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError

    def all(self):
        for number, clue in self.across.items():
            yield 'across', number, clue
        for number, clue in self.down.items():
            yield 'down', number, clue


class Crossword(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._data = [[None for x in range(width)] for x in range(height)]
        self.meta = CrosswordMetadata()
        self.clues = CrosswordClues()

    @property
    def cells(self):
        for y in range(self.height):
            for x in range(self.width):
                yield x, y

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
                result.append(unicode(cell) if cell is not None else ' ')
            result.append(u'\n')
        return u''.join(result)
