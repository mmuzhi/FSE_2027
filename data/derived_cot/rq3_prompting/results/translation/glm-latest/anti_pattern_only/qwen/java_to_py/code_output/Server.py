from typing import Any, Dict, List, Optional


class Server:

    def __init__(self) -> None:
        self.white_list: List[int] = []
        self.send_struct: Dict[str, Any] = {}
        self.receive_struct: Dict[str, Any] = {}

    def add_white_list(self, addr: int) -> Optional[List[int]]:
        if addr in self.white_list:
            return None
        else:
            self.white_list.append(addr)
            return self.white_list

    def del_white_list(self, addr: int) -> Optional[List[int]]:
        if addr not in self.white_list:
            return None
        else:
            self.white_list.remove(addr)
            return self.white_list

    def recv(self, info: Optional[Dict[str, Any]]) -> Any:
        if info is None or "addr" not in info or "content" not in info:
            return -1
        addr = info["addr"]
        content = info["content"]
        if addr not in self.white_list:
            return False
        else:
            self.receive_struct["addr"] = addr
            self.receive_struct["content"] = content
            return self.receive_struct["content"]

    def send(self, info: Optional[Dict[str, Any]]) -> Optional[str]:
        if info is None or "addr" not in info or "content" not in info:
            return "info structure is not correct"
        self.send_struct["addr"] = info["addr"]
        self.send_struct["content"] = info["content"]
        return None

    def show(self, type: Optional[str]) -> Optional[Dict[str, Any]]:
        if type == "send":
            return self.send_struct
        elif type == "receive":
            return self.receive_struct
        else:
            return None