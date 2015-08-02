from PIL import Image, ImageDraw
from mazin import Grid
from mazin.carvers import btree


def make_grid_image(grid, cell_size=20, hpad=4, vpad=4):
    height = (grid.rows * cell_size) + (2 * vpad)
    width = (grid.cols * cell_size) + (2 * hpad)
    im = Image.new('RGB', (width, height),
            (255, 255, 255))
    draw = ImageDraw.Draw(im)
    for cell in grid.iter_rowcells:
        # Find the inner bounds of the cell
        # 1 - Top Left
        # 2 - Bottom Right
        x1 = hpad + (cell.col * cell_size)
        y1 = (cell.row * cell_size) + vpad
        x2 = hpad + ((cell.col + 1) * cell_size) - 1
        y2 = ((cell.row + 1) * cell_size) + vpad - 1

        draw.rectangle((x1, y1, x2, y2), fill=cell.color)

        # Only if on the edge should a cell draw it's left or top
        if cell.north is None:
            draw.line((x1, y1, x2, y1), fill=(0, 0, 0))
        if cell.west is None:
            draw.line((x1, y1, x1, y2), fill=(0, 0, 0))

        # Cells generally draw the right and below walls
        if cell.east not in cell.links:
            draw.line((x2, y1, x2, y2), fill=(0, 0, 0))
        if cell.south not in cell.links:
            # x1 - 1 makes sure bottom right corners are drawn in
            offset = 0 if cell.west is None else 1
            draw.line((x1 - offset, y2, x2, y2), fill=(0, 0, 0))

    return im


if __name__ == '__main__':
    grid = Grid(5, 5)
    btree(grid, seed=101)
    im = make_grid_image(grid)
    im.save('test_maze.png', "PNG")
