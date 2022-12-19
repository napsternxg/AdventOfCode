from pathlib import Path


class DayInfo(object):
    """Call as day_info = DayInfo(__file__)

    Args:
        object (_type_): _description_
    """

    def __init__(self, file_handle) -> None:
        # file_handle should be "__file__"
        self.base_dir = Path(file_handle).parent
        self.py_file = Path(file_handle).name

        print(self.py_file)
        input_pattern = self.py_file.replace(".py", "*.txt")
        print(input_pattern)

        # print(list(base_dir.glob("day12*.txt")))
        self.input_files = list(self.base_dir.glob(input_pattern))
        print(self.input_files)


def grid_neighbors(i, j, rows, cols):
    for dir in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        ni, nj = (i + dir[0], j + dir[1])
        if ni < 0 or ni >= rows or nj < 0 or nj >= cols:
            # Discard invalid moves
            continue
        yield (ni, nj)
