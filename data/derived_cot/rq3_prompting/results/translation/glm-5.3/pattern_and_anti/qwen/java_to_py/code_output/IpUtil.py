import socket


class IpUtil:

    @staticmethod
    def is_valid_ipv4(ip_address: str) -> bool:
        try:
            socket.getaddrinfo(ip_address, None)
            return "." in ip_address and ":" not in ip_address
        except socket.gaierror:
            return False

    @staticmethod
    def is_valid_ipv6(ip_address: str) -> bool:
        try:
            socket.getaddrinfo(ip_address, None)
            return ":" in ip_address
        except socket.gaierror:
            return False

    @staticmethod
    def get_hostname(ip_address: str) -> str | None:
        try:
            socket.getaddrinfo(ip_address, None)
            if ip_address == "0.0.0.0":
                return socket.gethostname()
            try:
                hostname = socket.gethostbyaddr(ip_address)[0]
            except (socket.gaierror, socket.herror):
                return None
            if hostname == ip_address:
                return None
            return hostname
        except socket.gaierror:
            return None