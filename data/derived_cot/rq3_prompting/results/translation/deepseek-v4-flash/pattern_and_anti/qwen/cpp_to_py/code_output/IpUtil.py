import socket


class IpUtil:
    @staticmethod
    def is_valid_ipv4(ip_address):
        try:
            socket.inet_pton(socket.AF_INET, ip_address)
            return True
        except OSError:
            return False

    @staticmethod
    def is_valid_ipv6(ip_address):
        try:
            socket.inet_pton(socket.AF_INET6, ip_address)
            return True
        except OSError:
            return False

    @staticmethod
    def get_hostname(ip_address):
        if ip_address == "0.0.0.0":
            try:
                return socket.gethostname()
            except OSError:
                return ""

        if not IpUtil.is_valid_ipv4(ip_address):
            return ""

        try:
            host, _ = socket.getnameinfo((ip_address, 0), 0)
            return host
        except OSError:
            return ""