from datetime import date, datetime, timedelta


class AccessGatewayFilter:

    def filter(self, request):
        request_uri = request.get("path")
        method = request.get("method")

        if self.is_start_with(request_uri):
            return True

        try:
            token = self.get_jwt_user(request)
            user = token.get("user")
            if user.get("level") > 2:
                self.set_current_user_info_and_log(user)
                return True
        except Exception:
            return False
        return False

    def is_start_with(self, request_uri):
        start_with = ("/api", "/login")
        for s in start_with:
            if request_uri.startswith(s):
                return True
        return False

    def get_jwt_user(self, request):
        token = request.get("headers").get("Authorization")
        user = token.get("user")
        jwt = token.get("jwt")

        if jwt.startswith(user.get("name")):
            jwt_str_date = jwt[len(user.get("name")):]
            jwt_date = datetime.strptime(jwt_str_date, "%Y-%m-%d").date()
            if date.today() - timedelta(days=3) > jwt_date:
                return None
        return token

    def set_current_user_info_and_log(self, user):
        host = user.get("address")
        message = str(user.get("name")) + str(host) + str(date.today())
        print(message)