import matplotlib.pyplot as plt


def plot_grid(grid, cols, rows, start=None, title=""):
    tmp = None
    if start:
        tmp = grid[start[1]][start[0]]
        grid[start[1]][start[0]] = 2
    plt.pcolormesh(grid, edgecolors="w", linewidth=1, cmap="gnuplot", vmin=0, vmax=2)
    if start:
        grid[start[1]][start[0]] = tmp
    ax = plt.gca()
    ax.set_aspect("equal")
    ax.invert_yaxis()
    plt.title(f"{(cols, rows)=}, {start=}. {title}")
    plt.show()


def make_path(points):
    N = len(points)
    for i, (x, y) in enumerate(points):
        yield (x, y)
        if i < N - 1:
            # one point left at-least
            grad = (points[i + 1][0] - x, points[i + 1][1] - y)
            grad = tuple(0 if g == 0 else int(g / abs(g)) for g in grad)

            def update(x, y):
                return x + grad[0], y + grad[1]

            (x, y) = update(x, y)
            while (x, y) != points[i + 1]:
                yield (x, y)
                (x, y) = update(x, y)


def set_grid(grid, points, minx):
    for i, (x, y) in enumerate(points):
        # print(f"> {i=}, {(x, y)=}, {(x-minx)=}")
        grid[y][x - minx] = 1
        if i == 0:
            continue
        px, py = points[i - 1]
        dx, dy = x - px, y - py
        sdx, sdy = [0 if v == 0 else int(v / abs(v)) for v in [dx, dy]]

        # print(f"> {(x, y)=}, {(px, py)=}, {(dx, dy)=}, {(sdx, sdy)=}")

        # Only iterate till one less point as curr point alread set
        if dx != 0:
            for xi in range(px + sdx, x, sdx):
                grid[py][xi - minx] = 1
        if dy != 0:
            for yi in range(py + sdy, y, sdy):
                grid[yi][px - minx] = 1


def parse_grid(fp, start):
    grid_range = [
        [float("inf"), float("-inf")],  # x-range
        [float("inf"), float("-inf")],  # y-range
    ]

    all_points = []
    for line in fp:
        # 0 = air, 1 = rock, 2 sand
        points = [
            tuple(int(x) for x in point.split(","))
            for point in line.strip().split(" -> ")
        ]
        for i in range(2):
            grid_range[i][0] = min(points[0][i], grid_range[i][0], points[-1][i])
            grid_range[i][1] = max(points[0][i], grid_range[i][1], points[-1][i])
        all_points.append(points)

    print(f"{grid_range=}")
    for i in range(2):
        grid_range[i][0] -= 1  # include one less than lower range
        grid_range[i][1] += 1  # include one more than higher range
    print(f"{grid_range=}")

    # Set min y to 0
    grid_range[1][0] = 0
    print(f"{grid_range=}")

    minx, miny = [int(grid_range[i][0]) for i in range(2)]

    cols, rows = [int(r[1] - r[0] + 1) for r in grid_range]
    print(f"{(cols, rows)=}, {(minx, miny)=}")

    grid = [[0] * cols for _ in range(rows)]

    print(f"{len(grid)=}, {len(grid[0])=}")

    for points in all_points:
        # print(f"{points=}")
        for x, y in make_path(points):
            grid[y][x - minx] = 1
        # set_grid(grid, points, minx)
        # break

    start = tuple(v - mv for v, mv in zip(start, (minx, miny)))
    return grid, cols, rows, start


def get_sand_dest(grid, start, cols, rows):
    nx, ny = start
    steps = 0
    while nx > 0 and nx < cols - 1 and ny < rows - 1:
        steps += 1
        # plot_grid(grid, cols, rows, start=(nx, ny), title=f"{steps=}")
        # print(f">> {(nx, ny)=}")
        if grid[ny + 1][nx] == 0:
            # move down
            ny += 1
        elif grid[ny + 1][nx - 1] == 0:
            # move left down
            ny += 1
            nx -= 1
        elif grid[ny + 1][nx + 1] == 0:
            # move right down
            ny += 1
            nx += 1
        else:
            # sand comes to rest
            # print(f">> {(nx, ny)=}. Rest.")
            return (nx, ny, False)
    # print(f">> {(nx, ny)=}. Flows.")
    return (nx, ny, True)  # Flows


def get_units_till_flow(grid, start, cols, rows):
    units = 0
    (nx, ny, flows) = get_sand_dest(grid, start, cols, rows)
    while not flows and (nx, ny) != start:
        units += 1
        # try:
        # print(f"> {units=}, {(nx, ny)=}, {grid[ny][nx]=}")
        # except IndexError as e:
        #     print(f"> Error: {units=}, {(nx, ny)=}, {(cols, rows)=}. {e}")
        #     raise

        grid[ny][nx] = 2  # 2 for sand
        (nx, ny, flows) = get_sand_dest(grid, start, cols, rows)
        # if units == 30:
        #     break
    if (nx, ny) == start:
        units += 1
        grid[ny][nx] = 2  # 2 for sand
        print(f"{(nx, ny)=} == {start=}. Source blocked.")
    return units


def grid_with_floor(grid, start, cols, rows, pad_cols=100):
    rows = rows + 1
    cols = pad_cols + cols + pad_cols
    start = (pad_cols + start[0], start[1])
    grid = [[0] * pad_cols + row + [0] * pad_cols for row in grid] + [[1] * cols]
    return (grid, start, cols, rows)


from utils import DayInfo

day_info = DayInfo(__file__)


for input_file in day_info.input_files[:]:
    print(f"==== {input_file.name=} ====")
    packets = []
    start = (500, 0)
    with open(input_file) as fp:
        grid, cols, rows, start = parse_grid(fp, start)
        print(f"{start=}")
        plot_grid(grid, cols, rows, start=start)
        units = get_units_till_flow(grid, start, cols, rows)
        print(f"{units=}")
        plot_grid(grid, cols, rows, start=None, title=f"{units=}")
    with open(input_file) as fp:
        start = (500, 0)
        grid, cols, rows, start = parse_grid(fp, start)
        # Pad cols can be at max = rows as the 2* height of the cave is what the max width the sand can fill
        grid, start, cols, rows = grid_with_floor(
            grid, start, cols, rows, pad_cols=rows
        )
        print(f"{start=}")
        plot_grid(grid, cols, rows, start=start)
        units = get_units_till_flow(grid, start, cols, rows)
        print(f"{units=}")
        plot_grid(grid, cols, rows, start=None, title=f"{units=}")


def test_grid_with_floor():
    with open(day_info.input_files[0]) as fp:
        grid, cols, rows, start = parse_grid(fp, (500, 0))
        grid, start, cols, rows = grid_with_floor(grid, start, cols, rows)
        plot_grid(grid, cols, rows, start=start)
        units = get_units_till_flow(grid, start, cols, rows)
        print(f"{units=}")
        plot_grid(grid, cols, rows, start=None, title=f"{units=}")
