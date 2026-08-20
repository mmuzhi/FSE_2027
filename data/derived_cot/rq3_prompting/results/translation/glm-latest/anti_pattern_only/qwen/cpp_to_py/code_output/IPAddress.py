class IPAddress:
    def __init__(self, ip_address):
        self.ip_address = ip_address

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
        return []

    def get_binary(self):
        if self.is_valid():
            octets = self.get_octets()
            return '.'.join(format(int(octet), '08b') for octet in octets)
        return ""

    def _split_octets(self):
        # Mimics `while (std::getline(ss, octet, '.'))`:
        # - an empty string yields no tokens at all
        # - a trailing '.' does not produce an extra empty token
        #   (e.g. "1.2.3.4." splits into exactly 4 tokens)
        if self.ip_address == "":
            return []
        octets = self.ip_address.split('.')
        if self.ip_address.endswith('.'):
            octets.pop()
        return octets

    def _is_valid_octet(self, octet):
        if not octet or len(octet) > 3:
            return False
        for c in octet:
            # explicit ASCII-digit check, matching C's isdigit() in the
            # "C" locale (str.isdigit() would also accept Unicode digits)
            if not ('0' <= c <= '9'):
                return False
        value = int(octet)
        return 0 <= value <= 255