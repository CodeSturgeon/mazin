import random
from functools import wraps
from mazin import Grid

CARVERS = ['btree', 'aldous_broder', 'wilson', 'sidewinder', 'wilsons']


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
def btree(grid, steps=0):
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

        cell.links += [random.choice(neighbors)]


@unroll_steps_zero
def aldous_broder(grid, steps=0):
    cell = grid._cells[(
            random.randint(0, grid.cols - 1),
            random.randint(0, grid.rows - 1)
        )]
    unvisited = grid.size - 1

    while unvisited > 0:
        if steps > 0:
            yield cell
        neighbor = random.choice(cell.neighbors)

        if not neighbor.links:
            cell.links += [neighbor]
            unvisited -= 1

        cell = neighbor


@unroll_steps_zero
def sidewinder(grid, steps=0):
    for row in grid.iter_rows:
        run = []
        for cell in row:
            if steps:
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


@unroll_steps_zero
def wilsons(grid, steps=0):
    unvisited = grid._cells.values()
    first = random.choice(unvisited)
    unvisited.remove(first)

    while unvisited:
        cell = random.choice(unvisited)
        path = [cell]

        while cell in unvisited:
            if steps:
                yield cell
            cell = random.choice(cell.neighbors)

            if cell in path:
                position = path.index(cell)
                path = path[0:position]
            path.append(cell)

        while path:
            cell = path.pop(0)
            if path:
                cell.links += [path[0]]
                unvisited.remove(cell)


if __name__ == '__main__':
    from mazin.walkers import dijkstra
    from mazin.text import content_distance
    try:
        import console
        console.clear()
    except ImportError:
        pass

    random.seed(5)
    btree_grid = Grid(5, 5)
    btree(btree_grid)
    print btree_grid, '\n'

    sidewinder_grid = Grid(5, 5)
    sidewinder(sidewinder_grid)
    print sidewinder_grid, '\n'

    aldous_broder_grid = Grid(5, 5)
    aldous_broder(aldous_broder_grid)
    print aldous_broder_grid

    root = sidewinder_grid._cells[(0, 0)]
    dijkstra(sidewinder_grid, root)
    content_distance(sidewinder_grid, root)

    print sidewinder_grid

    wilsons_grid = Grid(5, 5)
    wilsons(wilsons_grid)
    print wilsons_grid, '\n'
