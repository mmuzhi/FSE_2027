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

        # The C++ code only performs reverse lookup for IPv4 addresses.
        # Invalid/non-IPv4 addresses cause getnameinfo to fail and return "".
        try:
            socket.inet_pton(socket.AF_INET, ip_address)
        except OSError:
            return ""

        try:
            host, _ = socket.getnameinfo((ip_address, 0), 0)
            return host
        except OSError:
            return ""