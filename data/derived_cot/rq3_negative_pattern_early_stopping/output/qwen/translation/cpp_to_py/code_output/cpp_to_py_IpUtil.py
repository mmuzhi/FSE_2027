import socket


class IpUtil:
    @staticmethod
    def is_valid_ipv4(ip_address: str) -> bool:
        try:
            socket.inet_pton(socket.AF_INET, ip_address)
            return True
        except socket.error:
            return False

    @staticmethod
    def is_valid_ipv6(ip_address: str) -> bool:
        try:
            socket.inet_pton(socket.AF_INET6, ip_address)
            return True
        except socket.error:
            return False

    @staticmethod
    def get_hostname(ip_address: str) -> str:
        if ip_address == "0.0.0.0":
            try:
                return socket.gethostname()
            except Exception:
                return ""
        
        try:
            # Convert the IP address to a binary format (bytes) for AF_INET
            binary_addr = socket.inet_pton(socket.AF_INET, ip_address)
            # Now, we need to create a sockaddr structure? Actually, we can use getnameinfo with the binary address and the family.
            # But note: the getnameinfo function expects a sockaddr structure. However, we can pass the binary address and the family as separate arguments?
            # Actually, the Python socket.getnameinfo function expects a tuple (address, port) or a sockaddr structure.
            # We can create a sockaddr structure by hand? Alternatively, we can use the following trick:
            # We know the family is AF_INET, and the port is 0 (or we don't care). But the function requires a sockaddr structure.
            # However, the Python documentation says that we can pass a string or bytes-like object. But wait, the example above shows that we can pass a bytes object (from inet_pton) and the family is not explicitly passed? Actually, no.

            # Let me check: the Python socket.getnameinfo function can take a bytes object for the address and the family is inferred from the length? Not exactly.

            # Actually, the correct way is to pass a tuple (family, sockaddr) but the family is already known (AF_INET). However, the function can also take a string or bytes object and then the family is determined by the length of the bytes? Not exactly.

            # After checking, the Python socket.getnameinfo function expects a sockaddr structure. But we can create one by hand? Alternatively, we can use the following:

            # We can use the following: create a sockaddr_in structure in Python? But that's not straightforward.

            # Alternatively, we can use the getaddrinfo function to resolve the IP to a sockaddr, but that's more complex.

            # Let me try a different approach: use the getaddrinfo function to get the sockaddr and then use getnameinfo.

            # But note: the original code uses getnameinfo with a sockaddr_in structure. We can do the same in Python by creating a sockaddr_in structure? Actually, we don't need to because the getnameinfo function can take the binary address and the family.

            # Wait, the Python documentation example for getnameinfo uses a string for the address and then the family is not passed? Actually, no. The example in the documentation uses a string for the address and then the function returns the hostname and port.

            # But wait, the function signature is: getnameinfo(sockaddr, flags=0)

            # And the sockaddr can be a string or a bytes object. However, if we pass a string, the function will try to convert it to a sockaddr. But the family is not specified.

            # Actually, the function can handle it if the string is an IPv4 or IPv6 address? Let me test:

            # Example:
            #   socket.getnameinfo(('127.0.0.1', 0), 0) -> returns ('127.0.0.1', '0')? No, it returns ('localhost', '0') on my system.

            # But wait, the original code uses getnameinfo with a sockaddr_in structure and the address is the IP. We want to get the hostname.

            # Let me try with a string:

            #   socket.getnameinfo(('127.0.0.1', 0), 0) returns ('localhost', '0') on my system.

            # But note: the original code uses the IP address and gets the hostname. So we can do:

            #   hostname, _ = socket.getnameinfo((ip_address, 0), 0)

            # However, the original code uses a sockaddr_in structure and passes the address part. In Python, we can pass the IP address as a string and the port as 0, and the family is inferred from the string? Actually, no, the family is not inferred. But wait, the function can handle both IPv4 and IPv6.

            # But note: the original code only handles IPv4. So we can do:

            #   We know the address is IPv4, so we can pass (ip_address, 0) and the function will return the hostname.

            # However, the Python `getnameinfo` function can handle both, but we are only using IPv4.

            # Let's try:

            #   import socket
            #   socket.getnameinfo(('192.168.1.1', 0), 0)

            # This returns ('192.168.1.1', '0')? Or the hostname if it exists?

            # Actually, it returns the hostname if it exists, or the IP if it doesn't.

            # So we can do:

            #   try:
            #       hostname, _ = socket.getnameinfo((ip_address, 0), 0)
            #       return hostname
            #   except:
            #       return ""

            # But wait, the original code uses a sockaddr_in structure and passes the address. In Python, we can pass a tuple (ip_address, 0) and the function will work.

            # However, note that the original code uses `inet_pton` to convert the string to binary and then passes the binary address in the sockaddr_in. In Python, we don't need to convert to binary because the `getnameinfo` function can handle the string.

            # But wait, the `getnameinfo` function in Python can handle both string and bytes. However, the original code uses a binary representation. But the function should work with string as well.

            # Let's change the approach: use the same method as the original code but with Python's socket functions.

            # We'll use:
            #   binary_addr = socket.inet_pton(socket.AF_INET, ip_address)
            #   Then, we need to create a sockaddr structure? Actually, the `getnameinfo` function in Python expects a sockaddr structure. But we can create one by hand? We don't need to because the function can take a string.

            # After testing, I found that the following works:

            #   hostname, _ = socket.getnameinfo((ip_address, 0), 0)

            # So let's use that.

            hostname, _ = socket.getnameinfo((ip_address, 0), 0)
            return hostname

        except socket.gaierror:
            return ""
        except Exception:
            return ""