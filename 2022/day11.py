class Monkey(object):
    @classmethod
    def from_data(cls, data):
        """
        Monkey 0:
            Starting items: 79, 98
            Operation: new = old * 19
            Test: divisible by 23
                If true: throw to monkey 2
                If false: throw to monkey 3

        Args:
            data (_type_): _description_
        """

        data = [line.strip() for line in data.splitlines()]
        print(f"{data=}")
        mid = int(data[0][:-1].split(" ")[-1])
        items = [int(worry_level) for worry_level in data[1].split(": ")[1].split(", ")]

        op = data[2].split(": ")[1].replace("=", ":").replace("new", "old")
        op = eval(f"lambda {op}")

        test_divisor = int(data[3].split("Test: divisible by ")[1])
        true_cond = int(data[4].split("If true: throw to monkey ")[1])
        false_cond = int(data[5].split("If false: throw to monkey ")[1])

        test = (
            lambda worry_level: true_cond
            if worry_level % test_divisor == 0
            else false_cond
        )
        return cls(mid, items, op, test, divisor=test_divisor)

    def __init__(self, mid, items, op, test, divisor) -> None:
        self.mid = mid
        self.items = items
        self.op = op
        self.test = test
        self.divisor = divisor

    def __repr__(self) -> str:
        return f"Monkey(mid={self.mid}, items={self.items})"

    def throw(self, agent_worry_fn=lambda x: x // 3):
        worry_level = self.items.pop(0)
        worry_level = self.op(worry_level)
        worry_level = agent_worry_fn(worry_level)
        next_monkey_idx = self.test(worry_level)
        return worry_level, next_monkey_idx

    def throws(self, agent_worry_fn=lambda x: x // 3):
        while self.items:
            yield self.throw(agent_worry_fn=agent_worry_fn)

    def catch(self, item):
        self.items.append(item)


from collections import defaultdict


class Agent(object):
    def __init__(self, data, worry_fn=lambda x: x // 3) -> None:
        self.inspections = defaultdict(int)
        self.worry_fn = worry_fn
        self.setup_monkeys(data)

    def setup_monkeys(self, data):
        self.monkeys = []
        for monkey_data in data:
            self.monkeys.append(Monkey.from_data(monkey_data))

    def observe(self, monkey):
        self.inspections[monkey.mid] += 1

    def observe_round(self, round):
        for monkey in self.monkeys:
            for worry_level, next_monkey_idx in monkey.throws(
                agent_worry_fn=self.worry_fn
            ):
                self.observe(monkey)
                self.monkeys[next_monkey_idx].catch(worry_level)
        # print(f"---- {round=} ----")
        # for monkey in self.monkeys:
        #     print(f"{round=}, {monkey=}, {self.inspections[monkey.mid]=}")

    def observe_rounds(self, rounds=20):
        for round in range(rounds):
            self.observe_round(round)
        print(f"{self.inspections=}")
        top_monkeys = sorted(
            self.inspections.items(), key=lambda x: x[1], reverse=True
        )[:2]
        print(f"{top_monkeys=}")
        ans = top_monkeys[0][1] * top_monkeys[1][1]
        return ans


from utils import DayInfo

day_info = DayInfo(__file__)

for input_file in day_info.input_files:
    print(f"==== {input_file.name=} ====")
    with open(input_file) as fp:
        data = fp.read().split("\n\n")
    print(">>> Less worried agent")
    agent = Agent(data=data, worry_fn=lambda x: x // 3)
    print(f"{agent.monkeys=}")
    ans = agent.observe_rounds(rounds=20)
    print(f"{ans=}")

    print(">>> More worried agent")
    """
    Key Trick for part 2 is as follows
    The worry_level gets very large the % op takes a lot of time.
    Since all we care about is the divisibility test we can instead store a smaller number.
    This number can be worry_level % product of all divisors

    The key learning here is that modulo operation is not an O(1) op.

    Source: https://www.reddit.com/r/adventofcode/comments/zifqmh/comment/j0qzik6/?utm_source=reddit&utm_medium=web2x&context=3
    """
    prod_divisors = 1
    for monkey in agent.monkeys:
        prod_divisors *= monkey.divisor

    print(f"{prod_divisors=}")

    agent = Agent(data=data, worry_fn=lambda x: x % prod_divisors)
    print(f"{agent.monkeys=}")
    ans = agent.observe_rounds(rounds=10_000)
    print(f"{ans=}")
