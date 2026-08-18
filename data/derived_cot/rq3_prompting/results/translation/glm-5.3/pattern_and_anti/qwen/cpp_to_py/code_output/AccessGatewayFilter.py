import time
from dataclasses import dataclass, field


@dataclass
class User:
    name: str = ""
    level: int = 0
    address: str = ""


@dataclass
class Authorization:
    user: User = field(default_factory=User)
    jwt: str = ""


@dataclass
class Request:
    path: str = ""
    method: str = ""
    auth: Authorization = field(default_factory=Authorization)


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
        except BaseException:
            return False
        return False

    def is_start_with(self, request_uri):
        start_with = ("/api", "/login")
        for s in start_with:
            if request_uri.startswith(s):
                return True
        return False

    @staticmethod
    def _parse_time_t(text):
        # Emulates `std::istringstream >> std::time_t`:
        # skip leading whitespace, optional sign, then ASCII digits.
        # Partial prefixes (e.g. "123abc") succeed; no digits -> failure.
        i, n = 0, len(text)
        while i < n and text[i] in " \t\n\v\f\r":
            i += 1
        start = i
        if i < n and text[i] in "+-":
            i += 1
        digits_start = i
        while i < n and "0" <= text[i] <= "9":
            i += 1
        if i == digits_start:
            return None  # stream failure (ss.fail())
        val = int(text[start:i])
        if not (-(2 ** 63) <= val <= 2 ** 63 - 1):
            return None  # overflow sets failbit on signed extraction
        return val

    def get_jwt_user(self, request):
        token = request.auth
        user = token.user

        # Note: jwt.startswith("") is True, matching jwt.find("") == 0
        if token.jwt.startswith(user.name):
            jwt_str_date = token.jwt[len(user.name):]

            jwt_timestamp = self._parse_time_t(jwt_str_date)
            if jwt_timestamp is None:
                return Authorization()

            now = int(time.time())
            if now - jwt_timestamp >= 3 * 24 * 60 * 60:
                return Authorization()
        return token

    def set_current_user_info_and_log(self, user):
        print(f"{user.name} {user.address} {int(time.time())}")