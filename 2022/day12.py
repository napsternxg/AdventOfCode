def process_grid(grid):
    start = None
    end = None
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == "S":
                start = (i, j)
                grid[i][j] = "a"
            elif cell == "E":
                end = (i, j)
                grid[i][j] = "z"
            grid[i][j] = ord(grid[i][j]) - ord("a")
    return start, end


# from functools import lru_cache

from heapq import heappop, heappush, heapify

import matplotlib.pyplot as plt
from utils import grid_neighbors


def find_path(grid, start, end):
    rows, cols = len(grid), len(grid[0])

    def plot_path(best_path):
        plot_grid = [[0] * cols for i in range(rows)]
        for i, j in best_path:
            plot_grid[i][j] = 1

        plt.imshow(plot_grid)
        plt.show()

    visited = set()

    def dfs(end):
        # print(f"> {end=}, {visited=}")
        if end == start:
            # print(f"> Found. {visited=}")
            return 0
        min_dist = float("inf")
        visited.add(end)
        for nn in grid_neighbors(end[0], end[1], rows, cols):
            if nn in visited:
                continue
            # if abs(ord(grid[end[0]][end[1]]) - ord(grid[nn[0]][nn[1]])) > 1:
            if grid[end[0]][end[1]] - grid[nn[0]][nn[1]] > 1:
                continue
            min_dist = min(dfs(nn) + 1, min_dist)
        visited.remove(end)
        return min_dist

    def djikstra_path(parents, end):
        path = []
        while end is not None:
            path.append(end)
            end = parents[end[0]][end[1]]
        path = list(reversed(path))
        return path

    def djikstra(start, dir_cond=lambda c, n: grid[n[0]][n[1]] - grid[c[0]][c[1]] <= 1):
        pqueue = []

        dist = []
        parents = []
        for i in range(rows):
            dist.append([])
            parents.append([])
            for j in range(cols):
                # dist[i].append(0 if (i, j) == start else float("inf"))
                dist[i].append(float("inf"))
                parents[i].append(None)
        dist[start[0]][start[1]] = 0
        pqueue.append((0, start[0], start[1]))
        # heapify(pqueue)
        visited = set([start])
        while pqueue:
            d, i, j = heappop(pqueue)
            # if (i, j) == end:
            #     break
            for ni, nj in grid_neighbors(i, j, rows, cols):
                if (ni, nj) in visited or (not dir_cond((i, j), (ni, nj))):
                    # or grid[ni][nj] - grid[i][j] > 1:
                    continue
                visited.add((ni, nj))
                if (d + 1) < dist[ni][nj]:
                    dist[ni][nj] = d + 1
                    parents[ni][nj] = (i, j)
                    heappush(pqueue, (dist[ni][nj], ni, nj))
        return dist, parents

    dist, parents = djikstra(start)
    print(f"Final dist")
    for row in dist:
        print(row)
    print(f"Final parents")
    for row in parents:
        print(row)
    best_path = djikstra_path(parents, end)
    print(f"{best_path=}")
    plot_path(best_path)
    ans1 = dist[end[0]][end[1]]

    dist, parents = djikstra(
        end, dir_cond=lambda c, n: grid[c[0]][c[1]] - grid[n[0]][n[1]] <= 1
    )  # Dir cond with reverse args

    # return dfs(end)
    best_start = start
    min_end = float("inf")
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == 0:
                d_end = dist[i][j]
                if d_end < min_end:
                    best_start = (i, j)
                    min_end = d_end
    print(f"{best_start=}, {min_end=}")

    best_path = djikstra_path(parents, start)
    plot_path(best_path)
    return ans1


from utils import DayInfo

day_info = DayInfo(__file__)

for input_file in day_info.input_files:
    print(f"==== {input_file.name=} ====")
    with open(input_file) as fp:
        grid = [list(line.strip()) for line in fp.read().splitlines()]
    start, end = process_grid(grid)
    for row in grid:
        print(row)
    print(f"{start=}, {end=}")
    ans = find_path(grid, start, end)

    print(f"{ans=}")
