from PIL import Image, ImageDraw
from mazin import Grid
from mazin.carvers import btree


def make_grid_image(grid, cell_size=20, hpad=10, vpad=10):
    height = (grid.rows * cell_size) + (2 * vpad)
    width = (grid.cols * cell_size) + (2 * hpad)
    im = Image.new('RGB', (width, height),
            (0, 0, 0))
    draw = ImageDraw.Draw(im)
    for cell in grid.iter_cells:
        x1 = hpad + (cell.col * cell_size)
        y1 = (cell.row * cell_size) + vpad
        x2 = hpad + ((cell.col + 1) * cell_size)
        y2 = ((cell.row + 1) * cell_size) + vpad

        if cell.north is None:
            draw.line((x1, y1, x2, y1))
        if cell.west is None:
            draw.line((x1, y1, x1, y2))

        if cell.east not in cell.links:
            draw.line((x2, y1, x2, y2))
        if cell.south not in cell.links:
            draw.line((x1, y2, x2, y2))

    return im


if __name__ == '__main__':
    grid = Grid(10, 10)
    btree(grid)
    im = make_grid_image(grid)
    im.save('test_maze.png', "PNG")
