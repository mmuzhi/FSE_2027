class BalancedBrackets:
    def __init__(self, expr):
        self.stack = []
        self.leftBrackets = "({["
        self.rightBrackets = ")}]"
        self.expr = expr

    def clearExpr(self):
        cleaned_expr = []
        for c in self.expr:
            if c in self.leftBrackets or c in self.rightBrackets:
                cleaned_expr.append(c)
        self.expr = ''.join(cleaned_expr)

    def checkBalancedBrackets(self):
        self.clearExpr()
        for Brkt in self.expr:
            if Brkt in self.leftBrackets:
                self.stack.append(Brkt)
            else:
                if not self.stack:
                    return False
                currentBrkt = self.stack.pop()
                if currentBrkt == '(' and Brkt != ')':
                    return False
                if currentBrkt == '{' and Brkt != '}':
                    return False
                if currentBrkt == '[' and Brkt != ']':
                    return False
        return len(self.stack) == 0

    def getExpr(self):
        return self.expr


if __name__ == "__main__":
    b = BalancedBrackets("a(b)c")
    print(b.checkBalancedBrackets())