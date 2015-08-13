from mazin import Cell


def basic_ascii(grid):
    sep = '+' + '---+' * grid.cols
    lines = [sep]
    for rn in range(grid.rows):
        # walls = [' ' if cell.linked(cell.east) else '|'
        #         for cell in row[:-1]]
        # lines.append('|   ' + '   '.join(walls) + '   |')
        line = '|'  # Starting wall
        floors = []
        for cn in range(grid.cols):
            if grid.mask[(cn, rn)]:
                cell = grid[(cn, rn)]
            else:
                cell = Cell(None, cn, rn)
            line += cell.content + (' ' if cell.east in cell.links else '|')
            floors += [' ' * 3 if cell.south in cell.links else '-' * 3]
        lines.append(line)
        if rn == grid.rows - 1:
            lines.append(sep)
            break
        lines.append('+' + '+'.join(floors) + '+')

    return '\n'.join(lines)


def fancy_unicode(grid):
    top = u'\u250c'
    for cn in range(grid.cols):
        cell = grid[(cn, 0)]
        if cell.east in cell.links:
            top += u'\u2500'
        else:
            if cn == grid.cols - 1:
                top += u'\u2510'
            else:
                top += u'\u252c'

    middles = []
    for rn in range(grid.rows - 1):
        row = u''
        for cn in range(grid.cols):
            cell = grid[(cn, rn)]

            if cn == 0:
                if cell.south in cell.links:
                    row += u'\u2502'
                else:
                    row += u'\u251c'

            if cn == grid.cols - 1:
                if cell.south in cell.links:
                    row += u'\u2502'
                else:
                    row += u'\u2524'
                continue

            celld = grid[(cn + 1, rn + 1)]
            ab = cell.east in cell.links
            ac = cell.south in cell.links
            bd = cell.east in celld.links
            cd = cell.south in celld.links
            ul = {
                    (True, True, True, True): u' ',
                    (False, False, False, False): u'\u253c',

                    (True, False, False, False): u'\u252c',
                    (False, True, False, False): u'\u2524',
                    (False, False, True, False): u'\u2534',
                    (False, False, False, True): u'\u251c',

                    (True, True, True, False): u'\u2574',
                    (True, True, False, True): u'\u2577',
                    (True, False, True, True): u'\u2576',
                    (False, True, True, True): u'\u2575',

                    (True, True, False, False): u'\u2510',
                    (True, False, True, False): u'\u2500',
                    (True, False, False, True): u'\u250c',
                    (False, True, False, True): u'\u2502',
                    (False, False, True, True): u'\u2514',
                    (False, True, True, False): u'\u2518',
                }
            row += ul[(ab, bd, cd, ac)]
        middles.append(row)

    bottom = u'\u2514'
    for cn in range(grid.cols):
        cell = grid[(cn, grid.rows - 1)]
        if cell.east in cell.links:
            bottom += u'\u2500'
        else:
            if cn == grid.cols - 1:
                bottom += u'\u2518'
            else:
                bottom += u'\u2534'
    return '\n'.join([top] + middles + [bottom])


def content_distance(grid, root_cell):
    for cell in grid.iter_cells:
        cell.content = '%2d ' % grid.distances[root_cell, cell]
