import time

class User:
    def __init__(self):
        self.name = ""
        self.level = 0
        self.address = ""

class Authorization:
    def __init__(self):
        self.user = User()
        self.jwt = ""

class Request:
    def __init__(self):
        self.path = ""
        self.method = ""
        self.auth = Authorization()

class AccessGatewayFilter:
    def filter(self, request):
        request_uri = request.path
        method = request.method

        if self.is_start_with(request_uri):
            return True

        try:
            token = self.get_jwt_user(request)
            user = token.user
            if user.level > 2:
                self.set_current_user_info_and_log(user)
                return True
        except:
            return False
        return False

    def is_start_with(self, request_uri):
        start_with = ["/api", "/login"]
        for s in start_with:
            if request_uri.startswith(s):
                return True
        return False

    def get_jwt_user(self, request):
        token = request.auth
        user = token.user

        if token.jwt.startswith(user.name):
            jwt_str_date = token.jwt[len(user.name):]
            try:
                jwt_timestamp = float(jwt_str_date)
            except ValueError:
                return Authorization()

            now = time.time()
            if (now - jwt_timestamp) >= 3 * 24 * 60 * 60:
                return Authorization()
        return token

    def set_current_user_info_and_log(self, user):
        print(user.name, user.address, int(time.time()))