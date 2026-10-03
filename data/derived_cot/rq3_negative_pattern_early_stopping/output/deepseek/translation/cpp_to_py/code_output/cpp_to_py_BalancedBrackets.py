class BalancedBrackets:
    def __init__(self, expr: str):
        self.expr = expr
        self.stack = []
        self.leftBrackets = "({["
        self.rightBrackets = ")}]"

    def clearExpr(self):
        self.expr = ''.join(c for c in self.expr if c in self.leftBrackets or c in self.rightBrackets)

    def check_balanced_brackets(self):
        self.clearExpr()
        for brkt in self.expr:
            if brkt in self.leftBrackets:
                self.stack.append(brkt)
            else:
                if not self.stack:
                    return False
                current_brkt = self.stack.pop()
                if current_brkt == '(' and brkt != ')':
                    return False
                if current_brkt == '{' and brkt != '}':
                    return False
                if current_brkt == '[' and brkt != ']':
                    return False
        return not self.stack