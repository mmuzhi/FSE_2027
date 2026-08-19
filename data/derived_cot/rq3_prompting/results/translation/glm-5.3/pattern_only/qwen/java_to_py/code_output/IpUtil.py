import socket


class IpUtil:

    @staticmethod
    def is_valid_ipv4(ip_address):
        try:
            socket.getaddrinfo(ip_address, None)
            return "." in ip_address and ":" not in ip_address
        except OSError:  # socket.gaierror / herror are OSError subclasses (≈ UnknownHostException)
            return False

    @staticmethod
    def is_valid_ipv6(ip_address):
        try:
            socket.getaddrinfo(ip_address, None)
            return ":" in ip_address
        except OSError:
            return False

    @staticmethod
    def get_hostname(ip_address):
        try:
            # Resolve first (mirrors InetAddress.getByName), keeping the resolved
            # address string so the reverse-lookup fallback behaves like Java.
            ip = socket.getaddrinfo(ip_address, None)[0][4][0]

            if ip_address == "0.0.0.0":
                return socket.gethostname()

            try:
                hostname = socket.gethostbyaddr(ip)[0]
            except OSError:
                # getCanonicalHostName falls back to the address string on failure
                hostname = ip

            if hostname == ip_address:
                return None
            return hostname
        except OSError:
            return None