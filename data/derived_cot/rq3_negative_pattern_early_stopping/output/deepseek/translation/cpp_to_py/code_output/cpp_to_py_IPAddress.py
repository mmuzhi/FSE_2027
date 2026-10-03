class IPAddress:
    def __init__(self, ip_address: str):
        self._ip_address = ip_address

    def is_valid(self) -> bool:
        octets = self._ip_address.split('.')
        if len(octets) != 4:
            return False
        for octet in octets:
            if not self._is_valid_octet(octet):
                return False
        return True

    def get_octets(self) -> list:
        if not self.is_valid():
            return []
        return self._ip_address.split('.')

    def get_binary(self) -> str:
        if not self.is_valid():
            return ""
        octets = self.get_octets()
        binary_parts = []
        for octet in octets:
            num = int(octet)
            binary_parts.append(format(num, '08b'))
        return '.'.join(binary_parts)

    def _is_valid_octet(self, octet: str) -> bool:
        if not octet or len(octet) > 3:
            return False
        for c in octet:
            if not ('0' <= c <= '9'):
                return False
        value = int(octet)
        return 0 <= value <= 255