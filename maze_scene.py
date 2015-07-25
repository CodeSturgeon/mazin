from scene import *
import maze_base
reload(maze_base)
import maze_carvers
reload(maze_carvers)

class GridScene(Scene):

	def __init__(self, carver, cols=None, rows=None, cell_size=None):
		self.cell_size = cell_size
		self.carver = carver
		self.cols = cols
		self.rows = rows
		super(GridScene, self).__init__()

	def setup(self):
		if (self.cols or self.rows) and (self.cell_size is None):
			
			if self.cols:
				max_width = int(self.size.w / (self.cols + 1))
			else:
				max_width = 99999

			if self.rows:
				max_height = int(self.size.h / (self.rows + 1))
			else:
				max_height = 99999

			self.cell_size = max_height if max_height < max_width else max_width
			
		if self.cols is self.rows is self.cell_size is None:
			self.cell_size = 20

		if self.cols is None:
			max_cols = int(self.size.w / self.cell_size) - 1
			self.cols = max_cols

		if self.rows is None:
			max_rows = int(self.size.h / self.cell_size) - 1
			self.rows = max_rows

		self.hpad = (self.size.w - (self.cols * self.cell_size))/2
		self.vpad = (self.size.h - (self.rows * self.cell_size))/2
		self.grid = maze_base.Grid(self.cols, self.rows)

		self.itr = self.carver(self.grid, True)

		self.delay = 0.00001
		self.acc = float(self.delay + 1)

	def draw(self):

		self.acc += self.dt
		if self.acc > self.delay:
			self.acc = 0
			try:
				self.next_cell = self.itr.next()
			except StopIteration:
				self.next_cell = None

		background(255, 255, 255)
		stroke(0 ,0 ,0)
		stroke_weight(1)
		fill(1, 0, 0)

		for cell in self.grid.iter_cells:
			x1 = self.hpad + (cell.col * self.cell_size)
			y1 = (self.size.h - (cell.row * self.cell_size)) - self.vpad
			x2 = self.hpad + ((cell.col + 1) * self.cell_size)
			y2 = (self.size.h - ((cell.row + 1) * self.cell_size)) - self.vpad
			
			if cell is self.next_cell:
				rect(x1, y2, self.cell_size, self.cell_size)

			if cell.north is None:
				line(x1, y1, x2, y1)
			if cell.west is None:
				line(x1, y1, x1, y2)

			if cell.east not in cell.links:
				line(x2, y1, x2, y2)
			if cell.south not in cell.links:
				line(x1, y2, x2, y2)


scene = GridScene(maze_carvers.btree, 10)
run(scene)

# vim:ts=4:noexpandtab
