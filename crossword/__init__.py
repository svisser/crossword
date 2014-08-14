
__title__ = 'crossword'
__version__ = '0.1'
__author__ = 'Simeon Visser'
__license__ = 'MIT'
__copyright__ = 'Copyright 2014 Simeon Visser'

try:
    range = xrange
except NameError:
    pass


class Crossword(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._data = [[None for x in range(width)] for x in range(height)]

    def __getitem__(self, index):
        x, y = index
        return self._data[y][x]

    def __setitem__(self, index, value):
        x, y = index
        self._data[y][x] = value
