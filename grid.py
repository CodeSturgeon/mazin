from collections import MutableMapping, defaultdict
from mazin.cell import Cell
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
		return self.basic_ascii()
		# return self.fancy_unicode()

	def basic_ascii(self):
		sep = '+' + '---+' * self.cols
		lines = [sep]
		for rn in range(self.rows):
			# walls = [' ' if cell.linked(cell.east) else '|'
			# 		for cell in row[:-1]]
			# lines.append('|   ' + '   '.join(walls) + '   |')
			line = '|'  # Starting wall
			floors = []
			for cn in range(self.cols):
				if self.mask[(cn, rn)]:
					cell = self._cells[(cn, rn)]
				else:
					cell = Cell(None, cn, rn)
				line += cell.content + (' ' if cell.east in cell.links else '|')
				floors += [' ' * 3 if cell.south in cell.links else '-' * 3]
			lines.append(line)
			if rn == self.rows - 1:
				lines.append(sep)
				break
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
