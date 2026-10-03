import sys
from datetime import datetime, date, timedelta

class AccessGatewayFilter:
    def __init__(self):
        pass

    def filter(self, request):
        request_uri = request.get("path")
        method = request.get("method")

        if self.is_start_with(request_uri):
            return True

        try:
            token = self.get_jwt_user(request)
            if token is None:
                return False
            user = token.get("user")
            if user is None:
                return False
            if user.get("level", 0) > 2:
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
        headers = request.get("headers")
        if headers is None:
            raise KeyError("headers")
        token = headers.get("Authorization")
        if token is None:
            raise KeyError("Authorization")
        user = token.get("user")
        if user is None:
            raise KeyError("user")
        jwt = token.get("jwt")
        if jwt is None:
            raise KeyError("jwt")

        if jwt.startswith(user["name"]):
            jwt_str_date = jwt[len(user["name"]):]
            try:
                jwt_date = datetime.strptime(jwt_str_date, "%Y-%m-%d").date()
            except ValueError:
                return None
            if (date.today() - timedelta(days=3)) > jwt_date:
                return None
        return token

    def set_current_user_info_and_log(self, user):
        host = user.get("address", "")
        message = str(user.get("name", "")) + host + str(date.today())
        sys.stdout.write(message + "\n")