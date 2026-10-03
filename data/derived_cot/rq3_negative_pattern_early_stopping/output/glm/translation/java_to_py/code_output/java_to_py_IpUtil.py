import socket
import ipaddress

class IpUtil:

    @staticmethod
    def is_valid_ipv4(ip_address: str) -> bool:
        try:
            socket.getaddrinfo(ip_address, None)
            return '.' in ip_address and ':' not in ip_address
        except OSError:
            return False

    @staticmethod
    def is_valid_ipv6(ip_address: str) -> bool:
        try:
            socket.getaddrinfo(ip_address, None)
            return ':' in ip_address
        except OSError:
            return False

    @staticmethod
    def get_hostname(ip_address: str) -> str | None:
        try:
            socket.getaddrinfo(ip_address, None)
        except OSError:
            return None

        if ip_address == "0.0.0.0":
            return socket.gethostname()

        hostname = socket.getfqdn(ip_address)

        try:
            addr = ipaddress.ip_address(ip_address)
            if hostname == ip_address:
                if addr.version == 4:
                    return None
                expanded_ip = addr.exploded
                parts = expanded_ip.split(':')
                java_expanded_ip = ':'.join(part.lstrip('0') or '0' for part in parts)
                if java_expanded_ip == ip_address:
                    return None
                return java_expanded_ip
        except ValueError:
            if hostname == ip_address:
                return None

        return hostname