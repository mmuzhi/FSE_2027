from collections import deque

class TextEditor:
    def __init__(self):
        self.stack = []
        self.q = deque()
        
    def addText(self, text: str) -> None:
        for c in text:
            self.stack.append(c)

    def deleteText(self, k: int) -> int:
        i = 0
        while self.stack and i < k:
            self.stack.pop()
            i += 1
        return i
        
    def cursorLeft(self, k: int) -> str:
        i = 0
        while self.stack and i < k:
            self.q.appendleft(self.stack.pop())
            i += 1
        return "".join(self.stack[-10:]) if len(self.stack) >= 10 else "".join(self.stack)

    def cursorRight(self, k: int) -> str:
        i = 0
        while self.q and i < k:
            self.stack.append(self.q.popleft())
            i += 1
        return "".join(self.stack[-10:]) if len(self.stack) >= 10 else "".join(self.stack)