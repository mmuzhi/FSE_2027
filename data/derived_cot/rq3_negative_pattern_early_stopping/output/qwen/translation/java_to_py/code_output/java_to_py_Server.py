class Server:
    def __init__(self):
        self.white_list = []
        self.send_struct = {}
        self.receive_struct = {}

    def add_white_list(self, addr):
        if addr in self.white_list:
            return None
        self.white_list.append(addr)
        return self.white_list

    def del_white_list(self, addr):
        if addr not in self.white_list:
            return None
        self.white_list.remove(addr)
        return self.white_list

    def recv(self, info):
        if info is None or 'addr' not in info or 'content' not in info:
            return -1
        try:
            addr = int(info['addr'])
            content = str(info['content'])
        except (TypeError, ValueError):
            return -1
        if addr not in self.white_list:
            return False
        self.receive_struct = {'addr': addr, 'content': content}
        return content

    def send(self, info):
        if info is None or 'addr' not in info or 'content' not in info:
            return "info structure is not correct"
        try:
            addr = info['addr']
            content = info['content']
        except (TypeError, ValueError):
            return "info structure is not correct"
        self.send_struct = {'addr': addr, 'content': content}
        return None

    def show(self, type_str):
        if type_str == "send":
            return self.send_struct
        elif type_str == "receive":
            return self.receive_struct
        return None