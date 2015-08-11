from collections import MutableMapping, defaultdict
from mazin.cell import Cell
from mazin.text import basic_ascii
from mazin import DIRECTIONS
import random


class KeySortingDict(MutableMapping):
    """A dict where the key is passed through sort for getting and setting"""
    def __init__(self):
        self._dict = dict()

    def _keygen(self, key):
        return tuple(sorted(key))

    def __getitem__(self, key):
        key = self._keygen(key)
        return self._dict[key]

    def __setitem__(self, key, value):
        key = self._keygen(key)
        self._dict[key] = value

    def __delitem__(self, key):
        key = self._keygen(key)
        del self._dict[key]

    def __iter__(self):
        return iter(self._dict)

    def __len__(self):
        return len(self._dict)

    def __str__(self):
        return str(self._dict)


class CellSortingDict(KeySortingDict):
    """Only accepts cells as keys"""
    def _keygen(self, k):
        if not isinstance(k, tuple) or not isinstance(k[0], Cell) or \
                not isinstance(k[1], Cell):
            raise TypeError
            # FIXME - return is not acceptable as an argument
        return tuple(sorted(((k[0].col, k[0].row), (k[1].col, k[1].row))))


class Grid(object):
    def __init__(self, cols, rows, mask=None):
        self.cols = cols
        self.rows = rows
        self.mask = mask or defaultdict(lambda: True)
        self.distances = KeySortingDict()
        self._populate()

    def _populate(self):
        self._cells = {}
        for col in range(self.cols):
            for row in range(self.rows):
                if self.mask[(col, row)]:
                    self._cells[(col, row)] = Cell(col, row)

        for col in range(self.cols):
            for row in range(self.rows):
                loc = (col, row)
                if not self.mask[loc]:
                    continue
                cell = self._cells[loc]
                for dcol, drow, dname, dbit in DIRECTIONS:
                    dloc = (col + dcol, row + drow)
                    try:
                        dcell = self._cells[dloc]
                    except KeyError:
                        continue
                    else:
                        cell.neighbors += [dcell]
                        setattr(cell, dname, dcell)

    def __getitem__(self, key):
        print key
        return self._cells[key]

    @property
    def size(self):
        return len(self._cells)

    @property
    def random_cell(self):
        return random.choice(self._cells.values())

    @property
    def iter_rows(self):
        for rn in range(self.rows):
            yield [self._cells[(cn, rn)]
                    for cn in range(self.cols) if self.mask[(cn, rn)]]

    @property
    def iter_rowcells(self):
        for rn in range(self.rows):
            for cn in range(self.cols):
                if self.mask[(cn, rn)]:
                    yield self._cells[(cn, rn)]

    @property
    def iter_cells(self):
        return self._cells.itervalues()

    def __str__(self):
        return basic_ascii(self)
