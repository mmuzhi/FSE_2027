class Solution:
    def calPoints(self, operations: List[str]) -> int:
        stack = []
        for op in operations:
            if op == 'D':
                if stack:
                    stack.append(2 * stack[-1])
                else:
                    stack.append(0)
            elif op == 'C':
                if stack:
                    stack.pop()
            elif op == '+':
                if len(stack) >= 2:
                    stack.append(stack[-1] + stack[-2])
                else:
                    stack.append(stack[-1] if stack else 0)
            else:
                stack.append(int(op))
        return sum(stack)