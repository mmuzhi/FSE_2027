class Server:
    def __init__(self):
        self.white_list = []
        self.send_struct = {}
        self.receive_struct = {}

    def add_white_list(self, addr):
        if addr in self.white_list:
            return []
        else:
            self.white_list.append(addr)
            # C++ returns the vector by value -> return a copy
            return list(self.white_list)

    def del_white_list(self, addr):
        if addr not in self.white_list:
            return []
        else:
            # removes the first occurrence, like erase(it) on the found iterator
            self.white_list.remove(addr)
            return list(self.white_list)

    def recv(self, info):
        if "addr" not in info or "content" not in info:
            return -1
        addr = int(info["addr"])  # std::stoi equivalent; raises ValueError on bad input
        content = info["content"]

        if addr not in self.white_list:
            return 0
        else:
            self.receive_struct = {"addr": str(addr), "content": content}
            return 1

    def send(self, info):
        if "addr" not in info or "content" not in info:
            return "info structure is not correct"
        self.send_struct = {"addr": info["addr"], "content": info["content"]}
        return ""

    def show(self, type):
        if type == "send":
            return dict(self.send_struct)
        elif type == "receive":
            return dict(self.receive_struct)
        else:
            return {}