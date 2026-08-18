class IPAddress:
    def __init__(self, ip_address):
        self.ip_address = ip_address

    @staticmethod
    def _split_octets(s):
        # Java's split("\\.") drops trailing empty strings; Python's split does not.
        parts = s.split(".")
        while parts and parts[-1] == "":
            parts.pop()
        return parts

    def is_valid(self):
        octets = self._split_octets(self.ip_address)
        if len(octets) != 4:
            return False
        for octet in octets:
            try:
                # Java's Integer.parseInt rejects surrounding whitespace and
                # underscores, which Python's int() would otherwise accept.
                if octet.strip() != octet or "_" in octet:
                    return False
                num = int(octet)
            except ValueError:
                return False
            if num < 0 or num > 255:
                return False
        return True

    def get_octets(self):
        octets_list = []
        if self.is_valid():
            for octet in self._split_octets(self.ip_address):
                octets_list.append(octet)
        return octets_list

    def get_binary(self):
        if self.is_valid():
            binary_octets = [f"{int(octet):08b}" for octet in self._split_octets(self.ip_address)]
            return ".".join(binary_octets)
        return ""