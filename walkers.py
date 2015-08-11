from mazin.carvers import unroll_steps_zero

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
