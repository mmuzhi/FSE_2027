import socket


class IpUtil:
    @staticmethod
    def is_valid_ipv4(ip_address):
        try:
            socket.inet_pton(socket.AF_INET, ip_address)
            return True
        except (OSError, ValueError):
            return False

    @staticmethod
    def is_valid_ipv6(ip_address):
        try:
            socket.inet_pton(socket.AF_INET6, ip_address)
            return True
        except (OSError, ValueError):
            return False

    @staticmethod
    def get_hostname(ip_address):
        if ip_address == "0.0.0.0":
            try:
                return socket.gethostname()
            except OSError:
                return ""

        # Mirror inet_pton failure: address unusable -> lookup yields ""
        try:
            socket.inet_pton(socket.AF_INET, ip_address)
        except (OSError, ValueError):
            return ""

        try:
            # flags = 0, same as the C++ getnameinfo(..., 0):
            # reverse lookup without NI_NAMEREQD, falls back to numeric on Windows
            host, _ = socket.getnameinfo((ip_address, 0), 0)
            return host
        except (socket.gaierror, OSError):
            return ""