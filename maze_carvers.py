import random
import maze_base
reload(maze_base)


class Carver(object):
	def __call__(self, grid, iter=False):
		if not iter:
			for x in self.carver(grid, False):
				pass
		else:
			return self.carver(grid)

	def carver(self, grid):
		raise NotImplemented


class Btree(Carver):
	def carver(self, grid, iter=False):
		for cell in grid.iter_rowcells:
			if iter:
				yield cell
			neighbors = []
			if cell.north:
				neighbors += [cell.north]
			if cell.east:
				neighbors += [cell.east]

			if not neighbors:
				continue

			cell.links += [random.choice(neighbors)]


class Sidewinder(Carver):
	def carver(self, grid, iter=False):
		for row in grid.iter_rows:
			run = []
			for cell in row:
				if iter:
					yield cell
				run.append(cell)
				nbound = cell.north is None
				ebound = cell.east is None

				closing = ebound or (not nbound and random.randint(0, 1))
				if closing:
					member = random.choice(run)
					if member.north:
						member.links += [member.north]
						run = []
				else:
					cell.links += [cell.east]


if __name__ == '__main__':
	try:
		import console
		console.clear()
	except ImportError:
		pass

	btree_grid = maze_base.Grid(5, 5)
	Btree()(btree_grid)
	print btree_grid, '\n'

	sidewinder_grid = maze_base.Grid(5, 5)
	Sidewinder()(sidewinder_grid)
	print sidewinder_grid

# vim:ts=4:noexpandtab
