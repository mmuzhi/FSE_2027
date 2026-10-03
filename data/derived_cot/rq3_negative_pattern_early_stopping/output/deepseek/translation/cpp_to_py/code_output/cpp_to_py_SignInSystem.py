from typing import List

class SignInSystem:
    def __init__(self) -> None:
        self._users: dict = {}  # maps username (str) -> bool (signed in or not)

    def add_user(self, username: str) -> bool:
        if username in self._users:
            return False
        self._users[username] = False
        return True

    def sign_in(self, username: str) -> bool:
        if username not in self._users:
            return False
        self._users[username] = True
        return True

    def check_sign_in(self, username: str) -> bool:
        if username not in self._users:
            return False
        return self._users[username]

    def all_signed_in(self) -> bool:
        return all(flag for flag in self._users.values())

    def all_not_signed_in(self) -> List[str]:
        return [user for user, flag in self._users.items() if not flag]