from dataclasses import dataclass


@dataclass
class TreeNode:
    path: str
    children: dict[str, "TreeNode"] = None
    size: int = 0

    @property
    def is_dir(self):
        return self.children is not None

    @property
    def file_type(self):
        return "dir" if self.is_dir else "file"


def show_tree(root, depth=0):
    """_summary_

    - / (dir)
      - a (dir)
        - e (dir)
          - i (file, size=584)
        - f (file, size=29116)
        - g (file, size=2557)
        - h.lst (file, size=62596)
      - b.txt (file, size=14848514)
      - c.dat (file, size=8504156)
      - d (dir)
        - j (file, size=4060174)
        - d.log (file, size=8033020)
        - d.ext (file, size=5626152)
        - k (file, size=7214296)
        Args:
            root (_type_): _description_
            depth (int, optional): _description_. Defaults to 0.

        Returns:
            _type_: _description_
    """
    paths = [f"{' '*depth}- {root.path} ({root.file_type}, size={root.size})"]
    if not root.children:
        # return [f"{' '*depth}- {root.path} ({root.file_type}, size={root.size})"]
        return paths
    for path, child in root.children.items():
        paths += show_tree(child, depth=depth + 1)
    return paths


def parse_cmd(line):
    cmd, *args = line.strip().split(" ")
    # print(f"{cmd=}, {args=}")
    return cmd, args


class Terminal(object):
    def __init__(self, fp) -> None:
        self.fp = fp
        self.root = TreeNode("/", children=dict())
        self.stack = []
        self.curr = self.root

    def cd(self, args, output):
        path = args[0]
        if path == "/":
            self.curr = self.root
            self.stack = []
        elif path == "..":
            self.curr = self.stack.pop()
        else:
            self.stack.append(self.curr)
            self.curr = self.curr.children[path]
        # print(f"cd > {self.curr.path=}, {len(self.stack)=}")

    def ls(self, args, output):
        for line in output:
            prop, name = line.strip().split(" ")
            if name not in self.curr.children:
                self.curr.children[name] = TreeNode(f"{self.curr.path}/{name}")
            if prop != "dir":
                prop = int(prop)
                self.curr.children[name].size = prop
            else:
                self.curr.children[name].children = dict()

    def process_output(self, cmd, args, output):
        # print(f"> {cmd=}, {args=}, {output=}, {self.curr.path=}")
        if cmd == "cd":
            self.cd(args, output)
        elif cmd == "ls":
            self.ls(args, output)
        pass

    def parse_lines(self):
        cmd, args, output = None, None, None
        num_cmd = 0
        for line in self.fp:
            line = line.strip()
            if line.startswith("$ "):
                if output:
                    self.process_output(cmd, args, output)
                    # break
                cmd, args = parse_cmd(line[2:])
                if cmd == "cd":
                    self.cd(args, output)
                output = []
                # num_cmd += 1
                # if num_cmd > 10:
                #     break
            else:
                output.append(line)
        if output:
            self.process_output(cmd, args, output)

    def du(self):
        def dfs(node):
            # print(f"du > {node.path=}, {node.size=}, {node.is_dir=}")
            if node.children is None:
                return node.size
            node.size = 0
            for path, child in node.children.items():
                node.size += dfs(child)
            return node.size

        return dfs(self.root)


def find_dirs(root, min_size=100_000):
    total_size = [0]

    def dfs(node):
        # print(f"find_dirs > {node.path=}, {node.size=}, {node.is_dir=}")
        if node.size <= min_size:
            total_size[0] += node.size
        for path, child in node.children.items():
            if child.is_dir:
                dfs(child)

    dfs(root)
    return total_size[0]


def find_dirs_to_delete(root, min_size=100_000):
    smallest_size = [float("inf")]
    smallest_node = [None]

    def dfs(node):
        # print(f"find_dirs > {node.path=}, {node.size=}, {node.is_dir=}")
        if not node.is_dir or node.size <= min_size:
            # Skip if non dir, size is less than requirement
            return False
        if node.size < smallest_size[0]:
            smallest_size[0] = node.size
            smallest_node[0] = node
        for path, child in node.children.items():
            dfs(child)

    dfs(root)
    print(f"{smallest_node[0].path=}, {smallest_node[0].size=}")
    return smallest_size[0]


with open("day07-test.txt") as fp:
    terminal = Terminal(fp)
    terminal.parse_lines()
    # print(f"{terminal.root=}")
    # print("\n".join(show_tree(terminal.root)))

    total_size = terminal.du()
    print(f"{total_size=}")
    # print(f"{terminal.root=}")

    # print("\n".join(show_tree(terminal.root)))

    total_size_of_dirs = find_dirs(terminal.root, min_size=100_000)
    print(f"{total_size_of_dirs=}")

    unused_space = 70_000_000 - terminal.root.size
    additional_space_needed = 30_000_000 - unused_space

    dir_to_delete = find_dirs_to_delete(terminal.root, min_size=additional_space_needed)
    print(f"{unused_space=:,}, {additional_space_needed=:,}, {dir_to_delete=:,}")
