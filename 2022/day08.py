"""
A tree is visible if all of the other trees between it and an edge of the grid are shorter than it. Only consider trees in the same row or column; that is, only look up, down, left, or right from any given tree.
"""

from functools import lru_cache

MOVES = {
    "left": lambda i, j: (i, j - 1),
    "right": lambda i, j: (i, j + 1),
    "up": lambda i, j: (i - 1, j),
    "down": lambda i, j: (i + 1, j),
}


class Grid(object):
    class InvalidMove(Exception):
        def __init__(self, i, j, dir, message="Invalid Move") -> None:
            self.i = i
            self.j = j
            self.dir = dir
            super().__init__(f"{message}. {i=}, {j=}, {dir=}")

    def __init__(self, grid) -> None:
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])

    def __len__(self):
        return self.rows * self.cols

    def is_valid_cell(self, i, j):
        return not (i < 0 or i > (self.rows - 1) or j < 0 or j > (self.cols - 1))

    def move(self, i, j, dir):
        ni, nj = MOVES[dir](i, j)
        if not self.is_valid_cell(ni, nj):
            raise Grid.InvalidMove(i, j, dir)
        return ni, nj

    def children(self, i, j):
        for dir in MOVES:
            try:
                ni, nj = self.move(i, j, dir)
                yield ni, nj, dir
            except Grid.InvalidMove as e:
                pass


def make_grid(fp):
    grid = []
    for line in fp:
        heights = [int(x) for x in line.strip()]
        grid.append(heights)
    return grid


def print_grid(grid, name="grid", fmt="{x:d}"):
    cols = len(grid[0])
    print(f"=== {name} ===")
    for row in grid:
        print(f"{''.join([fmt.format(x=x) for x in row])}")
    print(f"--- {name} ---")


def find_visible(grid):
    visibility = [[None for x in row] for row in grid]
    rows, cols = len(grid), len(grid[0])
    max_left = [[0 for x in row] for row in grid]
    for i in range(rows):
        for j in range(cols):
            max_left[i][j] = (
                grid[i][j] if j == 0 else max(max_left[i][j - 1], grid[i][j])
            )
            # cell is visible if max_left is lower than cell
            visibility[i][j] = (
                True
                if visibility[i][j] or j == 0 or max_left[i][j - 1] < grid[i][j]
                else None
            )

    max_top = [[0 for x in row] for row in grid]
    for j in range(cols):
        for i in range(rows):
            max_top[i][j] = grid[i][j] if i == 0 else max(max_top[i - 1][j], grid[i][j])
            # cell is visible if max_top is lower than cell
            visibility[i][j] = (
                True
                if visibility[i][j] or i == 0 or max_top[i - 1][j] < grid[i][j]
                else None
            )

    max_right = [[0 for x in row] for row in grid]
    for i in range(rows):
        for j in range(cols - 1, -1, -1):
            max_right[i][j] = (
                grid[i][j] if j == (cols - 1) else max(max_right[i][j + 1], grid[i][j])
            )
            # cell is visible if max_right is lower than cell
            visibility[i][j] = (
                True
                if visibility[i][j]
                or j == (cols - 1)
                or max_right[i][j + 1] < grid[i][j]
                else None
            )

    max_bottom = [[0 for x in row] for row in grid]
    for j in range(cols):
        for i in range(rows - 1, -1, -1):
            max_bottom[i][j] = (
                grid[i][j] if i == (rows - 1) else max(max_bottom[i + 1][j], grid[i][j])
            )
            # cell is visible if max_bottom is lower than cell
            visibility[i][j] = (
                True
                if visibility[i][j]
                or i == (rows - 1)
                or max_bottom[i + 1][j] < grid[i][j]
                else None
            )

    num_visible = 0
    for i in range(rows):
        for j in range(cols):
            visibility[i][j] = visibility[i][j] if visibility[i][j] else False
            num_visible += visibility[i][j]

    # print_grid(visibility, name="visibility")
    return num_visible


def find_visible_rec(grid):
    visibility = [[False for x in row] for row in grid]
    rows, cols = len(grid), len(grid[0])

    @lru_cache(maxsize=None)
    def dfs(i, j, dir):
        if i < 0 or i > (rows - 1) or j < 0 or j > (cols - 1):
            return -1, -1

        ni, nj = MOVES[dir](i, j)
        max_n, ndir_visible = dfs(ni, nj, dir)
        if max_n < grid[i][j]:
            visibility[i][j] = True
        # if max_n == -1:  # Edge
        #     ndir_visible = 0
        # elif grid[ni][nj] >= grid[i][j]:  # Same or taller neighbor
        #     ndir_visible = 1
        # else:  # Shorter neighbor
        #     ndir_visible += 1

        if max_n == -1 or grid[ni][nj] < grid[i][j]:
            ndir_visible += 1
        else:
            ndir_visible = 1
        return max(max_n, grid[i][j]), ndir_visible

    num_visible = 0
    scenic_score = [[1] * cols for i in range(rows)]
    max_scenic = -1
    for i in range(rows):
        for j in range(cols):
            for dir in ["up", "down", "left", "right"]:
                max_n, ndir_visible = dfs(i, j, dir)
                scenic_score[i][j] *= ndir_visible
                # if i > 0 and i < (rows - 1) and j > 0 and j < (cols - 1):
                #     print(
                #         f"{i=}, {j=}, {dir=}, {max_n=}, {ndir_visible=}, {scenic_score[i][j]=}"
                #     )
            max_scenic = max(max_scenic, scenic_score[i][j])
            num_visible += visibility[i][j]

    # print_grid(visibility, name="visibility")
    # print_grid(scenic_score, name="scenic_score", fmt=" {x:^4d} ")
    return num_visible, max_scenic


def get_max_scenic(grid):
    rows, cols = len(grid), len(grid[0])

    def is_valid_ij(i, j):
        return not (i < 0 or i > (rows - 1) or j < 0 or j > (cols - 1))

    def find_next_ge(i, j, dir):
        move = MOVES[dir]
        out = {}
        stack = []
        ni, nj = i, j
        last = (ni, nj)
        while is_valid_ij(ni, nj):
            while stack and grid[stack[-1][0]][stack[-1][1]] <= grid[ni][nj]:
                li, lj = stack.pop()
                out[(li, lj)] = (ni, nj)
            stack.append((ni, nj))
            last = (ni, nj)
            ni, nj = move(ni, nj)
        # print(f"{i=}, {j=}, {dir=}, {out=}")
        num_ge = dict()
        ni, nj = i, j
        while is_valid_ij(ni, nj):
            num_ge[(ni, nj)] = 0
            if (ni, nj) in out:
                gi, gj = out[(ni, nj)]
            else:
                gi, gj = last
            num_ge[(ni, nj)] = abs(ni - gi) + abs(nj - gj)
            ni, nj = move(ni, nj)
        # print(f"{i=}, {j=}, {dir=:<10}, {sorted(num_ge.items())=}")
        return num_ge

    scenic_score = [[1] * cols for i in range(rows)]
    max_scenic = -1
    for i in range(rows):
        j = 0
        num_ge = find_next_ge(i, j, "right")
        for j in range(cols):
            scenic_score[i][j] *= num_ge[(i, j)]
        j = cols - 1
        num_ge = find_next_ge(i, j, "left")
        for j in range(cols):
            scenic_score[i][j] *= num_ge[(i, j)]

    for j in range(cols):
        i = 0
        num_ge = find_next_ge(i, j, "down")
        for i in range(rows):
            scenic_score[i][j] *= num_ge[(i, j)]
        i = rows - 1
        num_ge = find_next_ge(i, j, "up")
        for i in range(rows):
            scenic_score[i][j] *= num_ge[(i, j)]


    max_scenic = max(sum(scenic_score, []))
    # print_grid(scenic_score, name="scenic_score", fmt=" {x:^4d} ")
    return max_scenic


def find_accessible(grid):
    accessibility = [[None for x in row] for row in grid]
    rows, cols = len(grid), len(grid[0])

    def check(i, j):
        if accessibility[i][j] is not None:
            return accessibility[i][j]
        if i == 0 or i == (rows - 1) or j == 0 or j == (cols - 1):
            # Mark edges as visible
            accessibility[i][j] = True
            return accessibility[i][j]
        for ni, nj in [
            (i - 1, j),  # Up
            (i + 1, j),  # Down
            (i, j - 1),  # Left
            (i, j + 1),  # Right
        ]:
            if ni < 0 or ni >= rows or nj < 0 or nj >= cols:
                # Skip invalid neighbor
                continue
            if grid[ni][nj] < grid[i][j] and check(ni, nj):
                # Neighbor less than curr and visible then curr is visible
                accessibility[i][j] = True
                return accessibility[i][j]
        accessibility[i][j] = False
        return accessibility[i][j]

    num_visible = 0
    for i, row in enumerate(grid):
        for j, col in enumerate(row):
            if check(i, j):
                num_visible += 1
    print_grid(accessibility, name="accessibility")
    return num_visible


with open("day08.txt") as fp:
    grid = make_grid(fp)
    # print_grid(grid)
    num_visible = find_visible(grid)
    print(f"{num_visible=}")
    num_visible, max_scenic = find_visible_rec(grid)
    print(f"{num_visible=}, {max_scenic=}")

    max_scenic = get_max_scenic(grid)
    print(f"{max_scenic=}")



        