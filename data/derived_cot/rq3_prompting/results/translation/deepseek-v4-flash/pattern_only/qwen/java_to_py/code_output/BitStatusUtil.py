class BitStatusUtil:

    @staticmethod
    def add(states: int, stat: int) -> int:
        BitStatusUtil.check(states, stat)
        return states | stat

    @staticmethod
    def has(states: int, stat: int) -> bool:
        BitStatusUtil.check(states, stat)
        return (states & stat) == stat

    @staticmethod
    def remove(states: int, stat: int) -> int:
        BitStatusUtil.check(states, stat)
        if BitStatusUtil.has(states, stat):
            return states ^ stat
        return states

    @staticmethod
    def check(*args: int) -> None:
        for arg in args:
            if arg < 0:
                raise ValueError(f"{arg} must be greater than or equal to 0")
            if arg % 2 != 0:
                raise ValueError(f"{arg} not even")

    @staticmethod
    def main() -> None:
        print(BitStatusUtil.add(2, 4))
        print(str(BitStatusUtil.has(6, 2)).lower())
        print(BitStatusUtil.remove(6, 2))
        try:
            BitStatusUtil.check(2, 3, 4)
        except ValueError as e:
            print(e)


if __name__ == "__main__":
    BitStatusUtil.main()