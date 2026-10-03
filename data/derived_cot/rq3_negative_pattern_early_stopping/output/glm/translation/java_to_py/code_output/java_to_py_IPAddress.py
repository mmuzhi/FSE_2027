class IPAddress:
    def __init__(self, ip_address):
        self.ip_address = ip_address

    def is_valid(self):
        octets = self.ip_address.rstrip(".").split(".")
        if len(octets) != 4:
            return False
        for octet in octets:
            try:
                if octet.strip() != octet or '_' in octet:
                    return False
                num = int(octet)
                if num < 0 or num > 255:
                    return False
            except ValueError:
                return False
        return True

    def get_octets(self):
        if self.is_valid():
            return self.ip_address.rstrip(".").split(".")
        return []

    def get_binary(self):
        if self.is_valid():
            binary_octets = []
            octets = self.ip_address.rstrip(".").split(".")
            for octet in octets:
                num = int(octet)
                binary_octet = format(num, '08b')
                binary_octets.append(binary_octet)
            return ".".join(binary_octets)
        return ""