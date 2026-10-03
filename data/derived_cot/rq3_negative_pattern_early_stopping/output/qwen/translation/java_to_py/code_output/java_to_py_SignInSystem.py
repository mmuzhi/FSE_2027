class SignInSystem:
    def __init__(self):
        self.users = {}

    def addUser(self, username):
        if username in self.users:
            return False
        self.users[username] = False
        return True

    def signIn(self, username):
        if username not in self.users:
            return False
        self.users[username] = True
        return True

    def checkSignIn(self, username):
        if username not in self.users:
            return False
        return self.users[username]

    def allSignedIn(self):
        return all(status is True for status in self.users.values())

    def allNotSignedIn(self):
        return [username for username, signed_in in self.users.items() if not signed_in]