from collections import MutableSequence
from mazin import DIRECTIONS


class CellList(MutableSequence):
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


class Linker(object):
	def __init__(self, cell):
		self.cell = cell

	def __getattr__(self, name):
		if name not in [d.name for d in DIRECTIONS]:
			raise AttributeError
		return getattr(self.cell, name) in self.cell.links

	def __setattr__(self, name, value):
		if name == 'cell':
			self.__dict__[name] = value
			return
		if name not in [d.name for d in DIRECTIONS]:
			raise AttributeError
		target = getattr(self.cell, name)
		if target is None and value:
			# No linking to something that is not there
			raise AttributeError

		linked = target in self.cell.links
		if value and not linked:
			self.cell.links += [target]
		elif not value and linked:
			self.cell.links.remove(target)

	def __call__(self, cell):
		if cell not in self.cell.neighbors:
			raise ValueError
		if cell not in self.cell.links:
			self.cell.links += [cell]


class Cell(object):
	def __init__(self, col, row):
		self.color = (255, 255, 255)
		self.col = col
		self.row = row
		self.north = None
		self.south = None
		self.east = None
		self.west = None
		self.content = '   '
		self.link = Linker(self)
		self.links = CellList(self)
		# FIXME this is sloppy, crossing bounds with the NESW of the cell
		self.neighbors = []

	def __repr__(self):
		return 'Cell(%d, %d)' % (self.col, self.row)

	@property
	def shape(self):
		ret = 0
		for d in DIRECTIONS:
			ret = ret | d.bit if getattr(self, d.name) else ret
		return ret
