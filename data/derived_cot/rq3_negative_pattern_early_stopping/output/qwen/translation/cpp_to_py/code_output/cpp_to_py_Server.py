class Server:
    def __init__(self):
        self.white_list = []
        self.send_struct = {}
        self.receive_struct = {}

    def add_white_list(self, addr):
        if addr in self.white_list:
            return []
        self.white_list.append(addr)
        return self.white_list

    def del_white_list(self, addr):
        if addr not in self.white_list:
            return []
        self.white_list.remove(addr)
        return self.white_list

    def recv(self, info):
        required_keys = {"addr", "content"}
        if not required_keys.issubset(info.keys()):
            return -1
        
        try:
            addr = int(info["addr"])
        except ValueError:
            return 0
        
        if addr not in self.white_list:
            return 0
        
        self.receive_struct = {"addr": str(addr), "content": info["content"]}
        return 1

    def send(self, info):
        required_keys = {"addr", "content"}
        if not required_keys.issubset(info.keys()):
            return "info structure is not correct"
        
        self.send_struct = {"addr": info["addr"], "content": info["content"]}
        return ""

    def show(self, type_str):
        if type_str == "send":
            return self.send_struct
        elif type_str == "receive":
            return self.receive_struct
        else:
            return {}