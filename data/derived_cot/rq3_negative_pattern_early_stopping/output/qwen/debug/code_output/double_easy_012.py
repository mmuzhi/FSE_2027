from typing import List

class Solution:
    def helperMethod(self, n: int, arr: List[str]) -> None:
        for i in range(1, n+1):
            if i % 15 == 0:
                arr.append("FizzBuzz")
            elif i % 3 == 0:
                arr.append("Fizz")
            elif i % 5 == 0:
                arr.append("Buzz")
            else:
                arr.append(str(i))
    
    def fizzBuzz(self, n: int) -> List[str]:
        arr = []
        self.helperMethod(n, arr)
        return arr