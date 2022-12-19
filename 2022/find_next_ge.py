def num_recent_le_idx(arr):
    """For each item find number of recent <= elements

    arr=[2, 5, 5, 1, 2]
    out=[0, 1, 1, 1, 2]

    arr=[1, 5, 4, 2, 5]
    out=[0, 1, 1, 1, 3]

    Args:
        arr (_type_): _description_
    """
    print(f"num_recent_le_idx({arr=})")
    out = [0]
    for i in range(1, len(arr)):
        for j in range(i - 1, -1, -1):
            if arr[j] >= arr[i]:
                print(f"{i=}, {arr[i]=}, {j=}, {arr[j]=}")
                break
        out.append(j)
    print(f"{arr=}")
    print(f"{out=}")
    print(f"max={[arr[i] for i in out]}")
    print(f"num={[(i-j) for i, j in enumerate(out)]}")


def next_ge_idx(arr):
    """For each item find number of recent <= elements
    https://painted-brush-a63.notion.site/day-8-O-n-with-next-greater-element-algorithm-ce3fb66663be44aea022ba1731fbe33b
    Using next greater element
    arr=[2, 5, 5, 1, 2]
    out=[0, 1, 1, 1, 2]

    arr=[1, 5, 4, 2, 5]
    out=[0, 1, 1, 1, 3]

    Args:
        arr (_type_): _description_
    """
    print(f"next_ge_idx({arr=})")
    out = [-1] * len(arr)
    stack = []
    for i in range(len(arr)):
        print(f"{i=}, {arr[i]=}, {stack=}, {out=}")
        while stack and arr[stack[-1]] < arr[i]:
            print(f"> {i=}, {arr[i]=}, {arr[stack[-1]]=}, {stack=}, {out=}")
            j = stack.pop()
            out[j] = i
        stack.append(i)
    print(f"{arr=}")
    print(f"{out=}")
    print(f"max={[arr[i] for i in out]}")
    print(f"num={[(i-j) for i, j in enumerate(out)]}")


class Container(object):
    def __init__(self, data) -> None:
        self.data = data

    def __repr__(self):
        return repr(self.data)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, key):
        return self.data[key]

    def __contains__(self, key):
        return key >= 0 and key < len(self)

    def traverse(self, key, dir):
        return key + dir


def next_ge_idx_generic(container, dir):
    out = dict()
    stack = []
    print(f"next_ge_idx_generic({container=!r}, {dir=})")
    key, dir = 0, 1
    while key in container:
        # print(f"{key=}, {(key in container)=}, {container[key]=}, {stack=}, {out=}")
        while stack and container[stack[-1]] <= container[key]:
            lower_elem_idx = stack.pop()
            out[lower_elem_idx] = key
        stack.append(key)
        key = container.traverse(key, dir)
    # print(f"{stack=}")
    print(f"{container=}")
    print(f"{out=}")
    print(
        f"max={[None if i not in out else container[out[i]] for i in range(len(container))]}"
    )
    print(f"num={[0 if i not in out else (out[i]-i) for i in range(len(container))]}")
    # print(f"num={[None if j is None else (i-j) for i, j in enumerate(out)]}")


for arr in [[2, 5, 5, 1, 2], [1, 5, 4, 2, 5], [1, 5, 5, 4, 2, 5]]:
    num_recent_le_idx(arr)
    next_ge_idx(arr)
    next_ge_idx_generic(Container(arr), dir=1)
