class IPAddress:
    def __init__(self, ip_address: str):
        self.ip_address = ip_address

    def is_valid(self) -> bool:
        octets = self._split_octets()
        if len(octets) != 4:
            return False
        for octet in octets:
            if not self._is_valid_octet(octet):
                return False
        return True

    def get_octets(self) -> list:
        if self.is_valid():
            return self._split_octets()
        else:
            return []

    def get_binary(self) -> str:
        if self.is_valid():
            octets = self.get_octets()
            parts = []
            for i, octet in enumerate(octets):
                num = int(octet)
                if i > 0:
                    parts.append('.')
                # bitset<8> + setw(8)/setfill('0') -> always exactly 8 binary digits
                parts.append(format(num, '08b'))
            return ''.join(parts)
        else:
            return ""

    def _split_octets(self) -> list:
        # Emulates `while (std::getline(ss, octet, '.'))`:
        # - empty string yields no fields
        # - a trailing '.' does not produce an extra empty field
        s = self.ip_address
        if s == '':
            return []
        octets = s.split('.')
        if s.endswith('.'):
            octets.pop()
        return octets

    def _is_valid_octet(self, octet: str) -> bool:
        if len(octet) == 0 or len(octet) > 3:
            return False

        for c in octet:
            # C isdigit(): only ASCII '0'-'9' (str.isdigit() would accept e.g. superscripts)
            if not ('0' <= c <= '9'):
                return False

        value = int(octet)
        return value >= 0 and value <= 255