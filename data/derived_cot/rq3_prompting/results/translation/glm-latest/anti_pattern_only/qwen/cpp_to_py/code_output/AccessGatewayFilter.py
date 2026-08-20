import re
import time


class User:
    def __init__(self, name="", level=0, address=""):
        self.name = name
        self.level = level
        self.address = address


class Authorization:
    def __init__(self, user=None, jwt=""):
        self.user = User() if user is None else user
        self.jwt = jwt


class Request:
    def __init__(self, path="", method="", auth=None):
        self.path = path
        self.method = method
        self.auth = Authorization() if auth is None else auth


class AccessGatewayFilter:
    # Mirrors `std::istringstream >> time_t` under the classic "C" locale:
    # optional leading whitespace, an optional sign, then decimal digits.
    # Trailing characters after the number are ignored (not a failure).
    _TIMESTAMP_RE = re.compile(r'[ \t\n\r\f\v]*([+-]?[0-9]+)')

    def filter(self, request):
        request_uri = request.path
        method = request.method  # kept for parity with the C++ code

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
        start_with = ("/api", "/login")
        for s in start_with:
            if request_uri.startswith(s):  # equivalent to find(s) == 0
                return True
        return False

    def get_jwt_user(self, request):
        token = request.auth
        user = token.user

        if token.jwt.startswith(user.name):
            jwt_str_date = token.jwt[len(user.name):]

            match = self._TIMESTAMP_RE.match(jwt_str_date)
            if match is None:
                # Extraction failed (ss.fail()).
                return Authorization()

            jwt_timestamp = int(match.group(1))
            # C++ sets failbit when the parsed value overflows time_t
            # (64-bit on the usual platforms).
            if not (-(2 ** 63) <= jwt_timestamp <= 2 ** 63 - 1):
                return Authorization()

            now = int(time.time())
            if now - jwt_timestamp >= 3 * 24 * 60 * 60:
                return Authorization()

        return token

    def set_current_user_info_and_log(self, user):
        # std::endl == "\n" + flush
        print(user.name, user.address, int(time.time()), flush=True)