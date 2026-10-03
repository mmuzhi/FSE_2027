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
        if info is None or 'addr' not in info or 'content' not in info:
            return -1

        addr = info['addr']
        content = info['content']

        if addr is None:
            raise TypeError("Cannot convert null to int")  # matches NullPointerException
        if not isinstance(addr, int) or isinstance(addr, bool):
            raise TypeError("Cannot cast to int")
        if content is not None and not isinstance(content, str):
            raise TypeError("Cannot cast to String")

        if addr not in self.whiteList:
            return False
        else:
            self.receiveStruct['addr'] = addr
            self.receiveStruct['content'] = content
            return self.receiveStruct['content']

    def send(self, info):
        if info is None or 'addr' not in info or 'content' not in info:
            return "info structure is not correct"
        self.sendStruct['addr'] = info['addr']
        self.sendStruct['content'] = info['content']
        return None

    def show(self, type_):
        if type_ == "send":
            return self.sendStruct
        elif type_ == "receive":
            return self.receiveStruct
        else:
            return None