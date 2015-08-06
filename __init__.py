import unittest
import random
from collections import MutableSequence, MutableMapping

N = NORTH = 0x1
E = EAST = 0x2
S = SOUTH = 0x4
W = WEST = 0x8

DIRECTIONS = (NORTH, EAST, SOUTH, WEST)


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
		return tuple(sorted(((k[0].col, k[0].row), (k[1].col, k[1].row))))


class _CellList(MutableSequence):
	def __init__(self, cell, *args):
		self.cell = cell
		self._list = list()
		self.extend(list(args))

	def _check(self, value):
		if not isinstance(value, Cell):
			raise TypeError('Not a Cell: %s' % value)

	def __len__(self):
		return len(self._list)

	def __getitem__(self, i):
		return self._list[i]

	def __delitem__(self, i):
		del self._list[i]

	def __setitem__(self, i, v):
		self._check(v)
		self._list[i] = v

	def insert(self, i, v, bidirection=True):
		self._check(v)
		if bidirection:
			v.links.insert(0, self.cell, bidirection=False)
		self._list.insert(i, v)

	def __str__(self):
		return str(self._list)


class Cell(object):
	def __init__(self, grid, col, row):
		self.grid = grid
		self.color = (255, 255, 255)
		self.col = col
		self.row = row
		self.north = None
		self.south = None
		self.east = None
		self.west = None
		self.content = '   '
		self.links = _CellList(self)
		# FIXME this is sloppy, crossing bounds with the NESW of the cell
		self.neighbors = []

	def __repr__(self):
		return 'Cell(%d, %d)' % (self.col, self.row)

	@property
	def shape(self):
		ret = 0
		ret = ret | NORTH if self.north in self.links else ret
		ret = ret | EAST if self.east in self.links else ret
		ret = ret | SOUTH if self.south in self.links else ret
		ret = ret | WEST if self.west in self.links else ret
		return ret


class Grid(object):
	def __init__(self, cols, rows):
		self.cols = cols
		self.rows = rows
		self.distances = CellSortingDict()
		self._cells = {}
		for col in range(cols):
			for row in range(rows):
				self._cells[(col, row)] = Cell(self, col, row)

		for col, row in self._cells:
			loc = (col, row)
			cell = self._cells[loc]
			if row > 0:
				cell.north = self._cells[(col, row - 1)]
				cell.neighbors += [self._cells[(col, row - 1)]]
			if row < self.rows - 1:
				cell.south = self._cells[(col, row + 1)]
				cell.neighbors += [self._cells[(col, row + 1)]]
			if col > 0:
				cell.west = self._cells[(col - 1, row)]
				cell.neighbors += [self._cells[(col - 1, row)]]
			if col < self.cols - 1:
				cell.east = self._cells[(col + 1, row)]
				cell.neighbors += [self._cells[(col + 1, row)]]


	def __getitem__(self, key):
		print key
		return self._cells[key]

	@property
	def size(self):
		return self.rows * self.cols

	@property
	def random_cell(self):
		return random.choice(self._cells.values())

	@property
	def iter_rows(self):
		for rn in range(self.rows):
			yield [self._cells[(cn, rn)] for cn in range(self.cols)]

	@property
	def iter_rowcells(self):
		for rn in range(self.rows):
			for cn in range(self.cols):
				yield self._cells[(cn, rn)]

	@property
	def iter_cells(self):
		return self._cells.itervalues()

	def __str__(self):
		return self.basic_ascii()
		# return self.fancy_unicode()

	def basic_ascii(self):
		sep = '+' + '---+' * self.cols
		lines = [sep]
		for row in self.iter_rows:
			# walls = [' ' if cell.linked(cell.east) else '|'
			# 		for cell in row[:-1]]
			# lines.append('|   ' + '   '.join(walls) + '   |')
			line = '|'  # Starting wall
			for cell in row:
				line += cell.content + (' ' if cell.east in cell.links else '|')
			lines.append(line)
			if row == self.rows - 1:
				lines.append(sep)
				break
			floors = [' ' * 3 if cell.south in cell.links else '-' * 3
					for cell in row]
			lines.append('+' + '+'.join(floors) + '+')

		return '\n'.join(lines)

	def fancy_unicode(self):
		top = u'\u250c'
		for cn in range(self.cols):
			cell = self._cells[(cn, 0)]
			if cell.east in cell.links:
				top += u'\u2500'
			else:
				if cn == self.cols - 1:
					top += u'\u2510'
				else:
					top += u'\u252c'

		middles = []
		for rn in range(self.rows - 1):
			row = u''
			for cn in range(self.cols):
				cell = self._cells[(cn, rn)]

				if cn == 0:
					if cell.south in cell.links:
						row += u'\u2502'
					else:
						row += u'\u251c'

				if cn == self.cols - 1:
					if cell.south in cell.links:
						row += u'\u2502'
					else:
						row += u'\u2524'
					continue

				celld = self._cells[(cn + 1, rn + 1)]
				ab = cell.east in cell.links
				ac = cell.south in cell.links
				bd = cell.east in celld.links
				cd = cell.south in celld.links
				ul = {
						(True, True, True, True): u' ',
						(False, False, False, False): u'\u253c',

						(True, False, False, False): u'\u252c',
						(False, True, False, False): u'\u2524',
						(False, False, True, False): u'\u2534',
						(False, False, False, True): u'\u251c',

						(True, True, True, False): u'\u2574',
						(True, True, False, True): u'\u2577',
						(True, False, True, True): u'\u2576',
						(False, True, True, True): u'\u2575',

						(True, True, False, False): u'\u2510',
						(True, False, True, False): u'\u2500',
						(True, False, False, True): u'\u250c',
						(False, True, False, True): u'\u2502',
						(False, False, True, True): u'\u2514',
						(False, True, True, False): u'\u2518',
					}
				row += ul[(ab, bd, cd, ac)]
			middles.append(row)

		bottom = u'\u2514'
		for cn in range(self.cols):
			cell = self._cells[(cn, self.rows - 1)]
			if cell.east in cell.links:
				bottom += u'\u2500'
			else:
				if cn == self.cols - 1:
					bottom += u'\u2518'
				else:
					bottom += u'\u2534'
		return '\n'.join([top] + middles + [bottom])

# vim:ts=4:noexpandtab
