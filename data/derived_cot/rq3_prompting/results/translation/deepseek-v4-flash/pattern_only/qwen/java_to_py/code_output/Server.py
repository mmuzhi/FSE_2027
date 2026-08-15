class Server:
    def __init__(self):
        self.whiteList = []
        self.sendStruct = {}
        self.receiveStruct = {}

    def addWhiteList(self, addr):
        if addr in self.whiteList:
            return None
        else:
            self.whiteList.append(addr)
            return self.whiteList

    def delWhiteList(self, addr):
        if addr not in self.whiteList:
            return None
        else:
            self.whiteList.remove(addr)
            return self.whiteList

    def recv(self, info):
        if info is None or "addr" not in info or "content" not in info:
            return -1
        addr = info["addr"]
        content = info["content"]
        if type(addr) is not int:
            raise TypeError("addr must be int")
        if content is not None and type(content) is not str:
            raise TypeError("content must be str")
        if addr not in self.whiteList:
            return False
        else:
            self.receiveStruct["addr"] = addr
            self.receiveStruct["content"] = content
            return self.receiveStruct["content"]

    def send(self, info):
        if info is None or "addr" not in info or "content" not in info:
            return "info structure is not correct"
        self.sendStruct["addr"] = info["addr"]
        self.sendStruct["content"] = info["content"]
        return None

    def show(self, type):
        if type == "send":
            return self.sendStruct
        elif type == "receive":
            return self.receiveStruct
        else:
            return None