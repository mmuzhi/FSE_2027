class SignInSystem:
    def __init__(self):
        self.users = {}

    def addUser(self, username):
        if username in self.users:
            return False
        else:
            self.users[username] = False
            return True

    def signIn(self, username):
        if username not in self.users:
            return False
        else:
            self.users[username] = True
            return True

    def checkSignIn(self, username):
        if username not in self.users:
            return False
        else:
            return self.users[username]

    def allSignedIn(self):
        for signedIn in self.users.values():
            if not signedIn:
                return False
        return True

    def allNotSignedIn(self):
        return [username for username, signedIn in self.users.items() if not signedIn]