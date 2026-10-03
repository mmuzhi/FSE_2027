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
        for signedIn in self.users.values():
            if not signedIn:
                return False
        return True

    def allNotSignedIn(self):
        notSignedIn = []
        for username, signedIn in self.users.items():
            if not signedIn:
                notSignedIn.append(username)
        return notSignedIn