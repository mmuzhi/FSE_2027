class IPAddress:
    def __init__(self, ip_address):
        self.ip_address = ip_address

    def is_valid(self):
        octets = self.ip_address.split('.')
        if len(octets) != 4:
            return False
        for octet in octets:
            if not self._is_valid_octet(octet):
                return False
        return True

    def get_octets(self):
        if self.is_valid():
            return self.ip_address.split('.')
        return []

    def get_binary(self):
        if self.is_valid():
            return '.'.join(f'{int(octet):08b}' for octet in self.get_octets())
        return ''

    def _is_valid_octet(self, octet):
        if not octet or len(octet) > 3:
            return False
        for c in octet:
            if not ('0' <= c <= '9'):
                return False
        value = int(octet)
        return 0 <= value <= 255