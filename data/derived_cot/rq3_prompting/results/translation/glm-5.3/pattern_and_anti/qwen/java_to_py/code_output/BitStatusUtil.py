def add(states: int, stat: int) -> int:
    check(states, stat)
    return states | stat


def has(states: int, stat: int) -> bool:
    check(states, stat)
    return (states & stat) == stat


def remove(states: int, stat: int) -> int:
    check(states, stat)
    if has(states, stat):
        return states ^ stat
    return states


def check(*args: int) -> None:
    for arg in args:
        if arg < 0:
            raise ValueError(f"{arg} must be greater than or equal to 0")
        if arg % 2 != 0:
            raise ValueError(f"{arg} not even")


if __name__ == "__main__":
    print(add(2, 4))
    print("true" if has(6, 2) else "false")
    print(remove(6, 2))
    try:
        check(2, 3, 4)
    except ValueError as e:
        print(e)