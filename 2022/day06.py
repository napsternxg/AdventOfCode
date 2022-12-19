def find_start(message, n=4, start=0):
    end = start + n - 1
    chars = set(message[start:end])
    print(chars)
    for end in range(n, len(message) + 1):
        chars = set(message[start:end])
        # print(f"{start=}, {end=}, {message[start:end]=}, {chars=}")
        if len(chars) == n:
            print(f"{start=}, {end=}, {message[start:end]=}, {chars=}")
            return start, end
        # chars.remove(message[start])
        # chars.add(message[end])

        start += 1
    return


with open("day06.txt") as fp:
    message = fp.read().strip()
    start, end = find_start(message, start=0, n=4)
    print(f"{start=}, {(start+1)=}, {end=}, {message[start:end]=}")
    start, end = find_start(message, start=0, n=14)
    print(f"{start=}, {(start+1)=}, {end=}, {message[start:end]=}")
