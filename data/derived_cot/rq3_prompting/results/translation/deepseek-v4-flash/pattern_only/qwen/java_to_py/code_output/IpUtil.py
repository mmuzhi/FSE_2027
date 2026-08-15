import socket


class IpUtil:

    @staticmethod
    def isValidIpv4(ip_address):
        try:
            socket.getaddrinfo(ip_address, 0)
            return "." in ip_address and ":" not in ip_address
        except (socket.gaierror, UnicodeError):
            return False

    @staticmethod
    def isValidIpv6(ip_address):
        try:
            socket.getaddrinfo(ip_address, 0)
            return ":" in ip_address
        except (socket.gaierror, UnicodeError):
            return False

    @staticmethod
    def getHostname(ip_address):
        if ip_address is None:
            hostname = socket.getfqdn("127.0.0.1")
            if hostname == ip_address:
                return None
            return hostname

        if ip_address == "":
            return None

        try:
            socket.getaddrinfo(ip_address, 0)
        except (socket.gaierror, UnicodeError):
            return None

        if ip_address == "0.0.0.0":
            try:
                hostname = socket.gethostname()
                socket.getaddrinfo(hostname, 0)
                return hostname
            except (UnicodeError, OSError):
                return None

        hostname = socket.getfqdn(ip_address)
        if hostname == ip_address:
            return None
        return hostname