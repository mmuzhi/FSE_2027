class IPAddress:
    def __init__(self, ip_address):
        self.ip_address = ip_address

    def _split_octets(self):
        # Emulates C++ std::getline(ss, octet, '.') semantics:
        # empty input yields no tokens, and a trailing delimiter
        # does not produce a final empty token.
        if self.ip_address == '':
            return []
        octets = self.ip_address.split('.')
        if self.ip_address.endswith('.'):
            octets.pop()
        return octets

    def is_valid(self):
        octets = self._split_octets()
        if len(octets) != 4:
            return False
        for octet in octets:
            if not self._is_valid_octet(octet):
                return False
        return True

    def get_octets(self):
        if self.is_valid():
            return self._split_octets()
        else:
            return []

    def get_binary(self):
        if self.is_valid():
            result = []
            octets = self.get_octets()
            for i, octet in enumerate(octets):
                num = int(octet)
                if i > 0:
                    result.append('.')
                result.append(format(num, '08b'))
            return ''.join(result)
        else:
            return ""

    def _is_valid_octet(self, octet):
        if len(octet) == 0 or len(octet) > 3:
            return False

        for c in octet:
            if c not in '0123456789':
                return False

        value = int(octet)
        return 0 <= value <= 255