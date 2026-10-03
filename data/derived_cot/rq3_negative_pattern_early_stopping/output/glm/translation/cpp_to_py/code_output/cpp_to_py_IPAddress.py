class IPAddress:
    def __init__(self, ip_address: str):
        self.ip_address = ip_address

    def _split_by_dot(self) -> list[str]:
        if not self.ip_address:
            return []
        
        parts = self.ip_address.split('.')
        if self.ip_address.endswith('.'):
            parts.pop()
        return parts

    def is_valid(self) -> bool:
        octets = self._split_by_dot()
        if len(octets) != 4:
            return False
        
        return all(self.is_valid_octet(octet) for octet in octets)

    def get_octets(self) -> list[str]:
        if self.is_valid():
            return self._split_by_dot()
        else:
            return []

    def get_binary(self) -> str:
        if self.is_valid():
            octets = self.get_octets()
            binary_octets = [format(int(octet), '08b') for octet in octets]
            return '.'.join(binary_octets)
        else:
            return ""

    def is_valid_octet(self, octet: str) -> bool:
        if not octet or len(octet) > 3:
            return False
        
        if not all('0' <= c <= '9' for c in octet):
            return False
            
        value = int(octet)
        return 0 <= value <= 255