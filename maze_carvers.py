import random
import maze_base
reload(maze_base)


def btree(grid, iter):
	for row in grid.iter_rows:
		for cell in row:
			if iter:
				yield cell
			neighbors = []
			if cell.north:
				neighbors.append(cell.north)
			if cell.east:
				neighbors.append(cell.east)

			if not neighbors:
				continue
			cell.link(random.choice(neighbors))


def sidewinder(grid, iter=False):
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
					member.link(member.north)
					run = []
			else:
				cell.link(cell.east)


if __name__ == '__main__':
	try:
		import console
		console.clear()
	except ImportError:
		pass

	btree_grid = maze_base.Grid(5, 5)
	try:
		btree(btree_grid, False).next()
	except StopIteration:
		pass

	sidewinder_grid = maze_base.Grid(5, 5)
	try:
		sidewinder(sidewinder_grid, False).next()
	except StopIteration:
		pass

	print btree_grid
	print
	print sidewinder_grid

# vim:ts=4:noexpandtab
