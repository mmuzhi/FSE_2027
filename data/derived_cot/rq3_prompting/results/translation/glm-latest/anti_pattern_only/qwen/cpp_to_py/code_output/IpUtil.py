import socket


class IpUtil:
    @staticmethod
    def is_valid_ipv4(ip_address: str) -> bool:
        try:
            socket.inet_pton(socket.AF_INET, ip_address)
            return True
        except OSError:
            return False

    @staticmethod
    def is_valid_ipv6(ip_address: str) -> bool:
        try:
            socket.inet_pton(socket.AF_INET6, ip_address)
            return True
        except OSError:
            return False

    @staticmethod
    def get_hostname(ip_address: str) -> str:
        if ip_address == "0.0.0.0":
            try:
                return socket.gethostname()
            except OSError:
                return ""

        try:
            # Mirrors getnameinfo() with flags = 0: performs a reverse lookup
            # and falls back to the numeric address if the name cannot be
            # resolved (NI_NAMEREQD is not set in the original code).
            host, _service = socket.getnameinfo((ip_address, 0), 0)
            return host
        except OSError:
            return ""