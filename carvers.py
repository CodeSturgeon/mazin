import random
from functools import wraps
import mazin


def unroll_steps_zero(f):
	@wraps(f)
	def wrapper(*args, **kwargs):
		if 'steps' in kwargs and kwargs['steps'] != 0:
			return f(*args, **kwargs)
		else:
			for x in f(*args, **kwargs):
				pass
	return wrapper


@unroll_steps_zero
def btree(grid, seed=None, steps=0):
	r = random.Random()
	if seed:
		r.seed(seed)
	for cell in grid.iter_rowcells:
		if steps:
			yield cell
		neighbors = []
		if cell.north:
			neighbors += [cell.north]
		if cell.east:
			neighbors += [cell.east]

		if not neighbors:
			continue

		cell.links += [r.choice(neighbors)]


@unroll_steps_zero
def sidewinder(grid, seed=None, steps=0):
	r = random.Random()
	if seed:
		r.seed(seed)
	for row in grid.iter_rows:
		run = []
		for cell in row:
			if steps:
				yield cell
			run.append(cell)
			nbound = cell.north is None
			ebound = cell.east is None

			closing = ebound or (not nbound and r.randint(0, 1))
			if closing:
				member = r.choice(run)
				if member.north:
					member.links += [member.north]
					run = []
			else:
				cell.links += [cell.east]


# FIXME should this really be here?
@unroll_steps_zero
def dijkstra(grid, root_cell, steps=0):
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
					# FIXME this will not work for multi-cell need a seen=set()
					if (root_cell, linked) not in grid.distances:
						if iter:
							yield linked
						grid.distances[root_cell, linked] = d + 1
						new_frontier += [linked]

			frontier = new_frontier


# FIXME should this really be here?
def colorize_distance(grid, root_cell):
		max_distance = max(grid.distances.values())
		step_size = 220 / max_distance
		for cell in grid.iter_cells:
			cell.color = (
					0,
					35 + (200 - (step_size * grid.distances[root_cell, cell])),
					0
				)


# FIXME should this really be here?
def content_distance(grid, root_cell):
	for cell in grid.iter_cells:
		cell.content = '%2d ' % grid.distances[root_cell, cell]


if __name__ == '__main__':
	try:
		import console
		console.clear()
	except ImportError:
		pass

	btree_grid = mazin.Grid(5, 5)
	btree(btree_grid, seed=5)
	print btree_grid, '\n'

	sidewinder_grid = mazin.Grid(5, 5)
	sidewinder(sidewinder_grid, seed=5)
	print sidewinder_grid, '\n'

	root = sidewinder_grid._cells[(0, 0)]
	dijkstra(sidewinder_grid, root)
	content_distance(sidewinder_grid, root)

	print sidewinder_grid

# vim:ts=4:noexpandtab
