from typing import Dict, List

class SignInSystem:
    def __init__(self) -> None:
        self.users: Dict[str, bool] = {}

    def add_user(self, username: str) -> bool:
        if username in self.users:
            return False
        else:
            self.users[username] = False
            return True

    def sign_in(self, username: str) -> bool:
        if username not in self.users:
            return False
        else:
            self.users[username] = True
            return True

    def check_sign_in(self, username: str) -> bool:
        if username not in self.users:
            return False
        else:
            return self.users[username]

    def all_signed_in(self) -> bool:
        return all(self.users.values())

    def all_not_signed_in(self) -> List[str]:
        return [username for username, signed_in in self.users.items() if not signed_in]