class IPAddress:
    def __init__(self, ip_address):
        self.ip_address = ip_address

    def is_valid(self):
        parts = self.ip_address.split('.')
        if len(parts) != 4:
            return False
        for part in parts:
            if not self.is_valid_octet(part):
                return False
        return True

    def get_octets(self):
        if self.is_valid():
            return self.ip_address.split('.')
        return []

    def get_binary(self):
        if self.is_valid():
            octets = self.get_octets()
            binary_parts = []
            for octet_str in octets:
                num = int(octet_str)
                bin_rep = bin(num)[2:].zfill(8)
                binary_parts.append(bin_rep)
            return '.'.join(binary_parts)
        return ''

    def is_valid_octet(self, octet):
        if len(octet) == 0 or len(octet) > 3:
            return False
        if not octet.isdigit():
            return False
        num = int(octet)
        return 0 <= num <= 255