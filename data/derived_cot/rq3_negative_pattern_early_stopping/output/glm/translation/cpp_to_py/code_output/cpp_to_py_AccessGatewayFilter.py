import time
import re


class User:
    def __init__(self, name="", level=0, address=""):
        self.name = name
        self.level = level
        self.address = address


class Authorization:
    def __init__(self, user=None, jwt=""):
        self.user = user if user is not None else User()
        self.jwt = jwt


class Request:
    def __init__(self, path="", method="", auth=None):
        self.path = path
        self.method = method
        self.auth = auth if auth is not None else Authorization()


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
        except Exception:
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

            match = re.match(r'\s*([-+]?\d+)', jwt_str_date)
            if not match:
                return Authorization()
            jwt_timestamp = int(match.group(1))

            now = int(time.time())
            if now - jwt_timestamp >= 3 * 24 * 60 * 60:
                return Authorization()

        return token

    def set_current_user_info_and_log(self, user):
        print(f"{user.name} {user.address} {int(time.time())}")