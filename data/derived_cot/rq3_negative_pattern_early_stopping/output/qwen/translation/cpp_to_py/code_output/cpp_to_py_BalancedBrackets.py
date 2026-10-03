class BalancedBrackets:
    def __init__(self, expr):
        self.expr = expr
        self.stack = []
        self.leftBrackets = "({["
        self.rightBrackets = ")}]"

    def clearExpr(self):
        allowed = set(self.leftBrackets + self.rightBrackets)
        self.expr = ''.join(c for c in self.expr if c in allowed)

    def check_balanced_brackets(self):
        self.clearExpr()
        for char in self.expr:
            if char in self.leftBrackets:
                self.stack.append(char)
            else:
                if not self.stack:
                    return False
                top = self.stack.pop()
                if (top == '(' and char != ')') or \
                   (top == '[' and char != ']') or \
                   (top == '{' and char != '}'):
                    return False
        return len(self.stack) == 0