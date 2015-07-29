import random
import maze_base
reload(maze_base)


# FIXME should be a decorator that detects noiter
class Carver(object):
	def __call__(self, *args, **kwargs):
		# FIXME ugly!
		iter = 'iter' in kwargs
		grid = args[0]
		if not iter:
			for x in self.carver(*args, iter=False):
				pass
		else:
			return self.carver(grid)

	def carver(self, grid):
		raise NotImplemented


class Btree(Carver):
	def carver(self, grid, iter=False):
		# FIXME bad var name
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
		# FIXME bad var name
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


class Dijkstra(Carver):
	def carver(self, grid, root_cell, iter=False):
		# FIXME should pass the dict, not the grid
		frontier = [root_cell]
		grid.distances[root_cell, root_cell] = 0
		while frontier:
			new_frontier = []
			for cell in frontier:
				if cell == root_cell:
					d = 0
				else:
					d = grid.distances[cell, root_cell]
				for linked in cell.links:
					if (root_cell, linked) not in grid.distances:
						if iter:
							yield linked
						grid.distances[root_cell, linked] = d + 1
						new_frontier += [linked]

			frontier = new_frontier


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
	print sidewinder_grid, '\n'

	root = sidewinder_grid._cells[(0,0)]
	Dijkstra()(sidewinder_grid, root)

	for cell in sidewinder_grid.iter_cells:
		cell.content = '%2d ' % sidewinder_grid.distances[root, cell]
	print sidewinder_grid

# vim:ts=4:noexpandtab
