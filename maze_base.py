import unittest
import random
from collections import MutableSequence


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


class Cell (object):
	def __init__(self, grid, col, row):
		self.grid = grid
		self.col = col
		self.row = row
		self.north = None
		self.south = None
		self.east = None
		self.west = None
		self.content = '   '
		self.links = _CellList(self)

	def __repr__(self):
		return 'Cell(%d, %d)' % (self.col, self.row)


class Grid(object):
	def __init__(self, cols, rows):
		self.cols = cols
		self.rows = rows
		self._cells = {}
		for col in range(cols):
			for row in range(rows):
				self._cells[(col, row)] = Cell(self, col, row)

		for col, row in self._cells:
			loc = (col, row)
			if row > 0:
				self._cells[loc].north = self._cells[(col, row - 1)]
			if row < self.rows - 1:
				self._cells[loc].south = self._cells[(col, row + 1)]
			if col > 0:
				self._cells[loc].west = self._cells[(col - 1, row)]
			if col < self.cols - 1:
				self._cells[loc].east = self._cells[(col + 1, row)]

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
			if cell.linked(cell.east):
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
					if cell.linked(cell.south):
						row += u'\u2502'
					else:
						row += u'\u251c'

				if cn == self.cols - 1:
					if cell.linked(cell.south):
						row += u'\u2502'
					else:
						row += u'\u2524'
					continue

				celld = self._cells[(cn + 1, rn + 1)]
				ab = cell.linked(cell.east)
				ac = cell.linked(cell.south)
				bd = cell.east.linked(celld)
				cd = cell.south.linked(celld)
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
			if cell.linked(cell.east):
				bottom += u'\u2500'
			else:
				if cn == self.cols - 1:
					bottom += u'\u2518'
				else:
					bottom += u'\u2534'
		return '\n'.join([top] + middles + [bottom])


class GridTest(unittest.TestCase):
	def test_size(self):
		grid = Grid(5, 5)
		self.assertTrue(len(grid._cells) == 5 * 5)
		self.assertEqual(grid.size, 5 * 5)

	def test_top_left_corner(self):
		grid = Grid(5, 5)
		self.assertIsNone(grid._cells[(0, 0)].north)
		self.assertIsNone(grid._cells[(0, 0)].west)
		self.assertIsNotNone(grid._cells[(0, 0)].south)
		self.assertIsNotNone(grid._cells[(0, 0)].east)

	def test_bottom_right_corner(self):
		grid = Grid(5, 5)
		self.assertIsNotNone(grid._cells[(4, 4)].north)
		self.assertIsNotNone(grid._cells[(4, 4)].west)
		self.assertIsNone(grid._cells[(4, 4)].south)
		self.assertIsNone(grid._cells[(4, 4)].east)

	def test_random_cell(self):
		grid = Grid(5, 5)
		cell1 = grid.random_cell
		cell2 = grid.random_cell
		cell3 = grid.random_cell
		self.assertIsInstance(cell1, Cell)
		self.assertIsInstance(cell2, Cell)
		self.assertIsInstance(cell3, Cell)


class CellTest(unittest.TestCase):

	def test_cell_list(self):
		cl = _CellList()
		cl.append(Cell(None, 1, 1))
		cl.extend([Cell(None, 2, 3)])
		with self.assertRaises(TypeError):
			cl.append(3)
			cl.extend([1, 2, 3])


if __name__ == '__main__':
	try:
		import console
		console.clear()
	except ImportError:
		pass

	grid = Grid(4, 4)
	print grid
	unittest.main()

# vim:ts=4:noexpandtab
