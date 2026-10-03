import socket


def is_valid_ipv4(ip_address: str) -> bool:
    """
    Mimics Java IpUtil.isValidIpv4:
    - Uses socket.getaddrinfo to check if the string can be resolved (address or hostname).
    - Returns True if it can be resolved AND the original string contains '.' and not ':'.
    - Returns False otherwise (including resolution failure).
    """
    try:
        socket.getaddrinfo(ip_address, 0, socket.AF_UNSPEC, socket.SOCK_STREAM)
        return '.' in ip_address and ':' not in ip_address
    except (socket.gaierror, socket.herror, OSError):
        return False


def is_valid_ipv6(ip_address: str) -> bool:
    """
    Mimics Java IpUtil.isValidIpv6:
    - Uses socket.getaddrinfo to check if the string can be resolved.
    - Returns True if it can be resolved AND the original string contains ':'.
    - Returns False otherwise.
    """
    try:
        socket.getaddrinfo(ip_address, 0, socket.AF_UNSPEC, socket.SOCK_STREAM)
        return ':' in ip_address
    except (socket.gaierror, socket.herror, OSError):
        return False


def get_hostname(ip_address: str):
    """
    Mimics Java IpUtil.getHostname:
    - Resolves the input to an IP address (using socket.getaddrinfo).
    - Special case: "0.0.0.0" returns the local hostname.
    - Performs a reverse DNS lookup on the resolved IP.
    - Returns:
        - `None` if the input cannot be resolved (any exception).
        - `None` if the canonical hostname equals the original input string.
        - Otherwise, the canonical hostname string.
    """
    try:
        addrinfo = socket.getaddrinfo(ip_address, 0, socket.AF_UNSPEC, socket.SOCK_STREAM)
        sockaddr = addrinfo[0][4]
        resolved_ip = sockaddr[0]  # for both IPv4 and IPv6, the IP is the first element

        if ip_address == "0.0.0.0":
            return socket.gethostname()

        try:
            canonical = socket.gethostbyaddr(resolved_ip)[0]
        except (socket.herror, OSError):
            canonical = resolved_ip

        if canonical == ip_address:
            return None
        return canonical

    except (socket.gaierror, socket.herror, OSError):
        return None