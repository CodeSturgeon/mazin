N = NORTH = 0x1
E = EAST = 0x2
S = SOUTH = 0x4
W = WEST = 0x8

DIRECTIONS = (
		(0, -1, 'north', NORTH),
		(1, 0, 'east', EAST),
		(0, 1, 'south', SOUTH),
		(-1, 0, 'west', WEST),
	)

from mazin.cell import Cell  # noqa
from mazin.grid import Grid  # noqa

# vim:ts=4:noexpandtab
