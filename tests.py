import unittest
from mazin import Grid, Cell, _CellList, KeySortingDict
from mazin.carvers import unroll_steps_zero


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
		cl = _CellList(Cell(None, 0, 0))
		cl.append(Cell(None, 1, 1))
		cl.extend([Cell(None, 2, 3)])
		with self.assertRaises(TypeError):
			cl.append(3)
			cl.extend([1, 2, 3])

	def test_cell_shape(self):
		cm = Cell(None, 1, 1)
		ce = Cell(None, 2, 1)
		cs = Cell(None, 1, 2)
		cm.east = ce
		ce.west = cm
		cm.links += [ce]
		self.assertEqual(cm.shape, 2)
		self.assertEqual(ce.shape, 8)
		cm.south = cs
		cs.north = cm
		cm.links += [cs]
		self.assertEqual(cm.shape, 6)
		self.assertEqual(cs.shape, 1)


class TestKeySortingDict(unittest.TestCase):
	def test_ksd_basic(self):
		ksd = KeySortingDict()
		ksd[(2, 2), (1, 1)] = 99
		self.assertEqual(ksd[(1, 1), (2, 2)], 99)


class TestUnroller(unittest.TestCase):
	def test_simple(self):
		@unroll_steps_zero
		def stepper(steps=0):
			for x in range(steps):
				yield 1

		self.assertIsNone(stepper(steps=0))
		self.assertEqual(sum([r for r in stepper(steps=5)]), 5)


def main():
	try:
		import console
		console.clear()
	except ImportError:
		pass

	grid = Grid(4, 4)
	print grid
	unittest.main()


if __name__ == '__main__':
	main()

# vim:ts=4:noexpandtab