from collections import namedtuple

Direction = namedtuple('Direction', 'col row name bit')

N = NORTH = 0x1
E = EAST = 0x2
S = SOUTH = 0x4
W = WEST = 0x8

DIRECTIONS = (
        Direction(0, -1, 'north', NORTH),
        Direction(1, 0, 'east', EAST),
        Direction(0, 1, 'south', SOUTH),
        Direction(-1, 0, 'west', WEST),
    )

from mazin.cell import Cell  # noqa
from mazin.grid import Grid  # noqa
