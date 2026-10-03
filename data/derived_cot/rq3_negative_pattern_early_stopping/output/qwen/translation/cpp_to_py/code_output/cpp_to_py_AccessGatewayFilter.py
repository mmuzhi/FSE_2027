import time
from datetime import timedelta

class User:
    def __init__(self, name, level, address):
        self.name = name
        self.level = level
        self.address = address

class Authorization:
    def __init__(self, user, jwt):
        self.user = user
        self.jwt = jwt

class Request:
    def __init__(self, path, method, auth):
        self.path = path
        self.method = method
        self.auth = auth

class AccessGatewayFilter:
    def __init__(self):
        pass

    def filter(self, request):
        request_uri = request.path
        method = request.method

        if self.is_start_with(request_uri):
            return True

        token = self.get_jwt_user(request)
        user = token.user
        if user.level > 2:
            self.set_current_user_info_and_log(user)
            return True

        return False

    def is_start_with(self, request_uri):
        prefixes = ["/api", "/login"]
        for prefix in prefixes:
            if request_uri.startswith(prefix):
                return True
        return False

    def get_jwt_user(self, request):
        token = request.auth
        user = token.user

        if token.jwt.startswith(user.name):
            jwt_str_date = token.jwt[len(user.name):]
            try:
                timestamp = int(jwt_str_date)
                current_time = time.time()
                if current_time - timestamp >= 3 * 24 * 60 * 60:
                    return Authorization(User("", 0, ""), "")
            except ValueError:
                return Authorization(User("", 0, ""), "")
        return token

    def set_current_user_info_and_log(self, user):
        current_time = time.time()
        print(f"{user.name} {user.address} {current_time}")

# Example usage:
if __name__ == "__main__":
    # Create a user
    user = User("john_doe", 3, "123 Main St")
    # Create an authorization token
    auth = Authorization(user, "john_doe 1710000000")
    # Create a request
    request = Request("/protected", "GET", auth)
    # Initialize the filter
    filter = AccessGatewayFilter()
    # Check if the request is allowed
    print(filter.filter(request))  # Output: True