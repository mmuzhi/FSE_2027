class SignInSystem:
    def __init__(self):
        self.users = {}  # Dictionary to store username and their sign-in state

    def add_user(self, username):
        if username in self.users:
            return False
        self.users[username] = False  # Initialize as not signed in
        return True

    def sign_in(self, username):
        if username not in self.users:
            return False
        self.users[username] = True  # Update sign-in state
        return True

    def check_sign_in(self, username):
        if username not in self.users:
            return False
        return self.users[username]

    def all_signed_in(self):
        for status in self.users.values():
            if not status:
                return False
        return True

    def all_not_signed_in(self):
        return [username for username, signed_in in self.users.items() if not signed_in]