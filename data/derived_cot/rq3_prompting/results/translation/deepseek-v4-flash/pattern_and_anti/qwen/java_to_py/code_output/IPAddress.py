class IPAddress:
    def __init__(self, ip_address):
        self.ip_address = ip_address

    def _split_octets(self):
        if self.ip_address == '':
            return ['']
        parts = self.ip_address.split('.')
        while parts and parts[-1] == '':
            parts.pop()
        return parts

    def isValid(self):
        octets = self._split_octets()
        if len(octets) != 4:
            return False
        for octet in octets:
            if octet != octet.strip():
                return False
            try:
                num = int(octet)
            except ValueError:
                return False
            if num < 0 or num > 255:
                return False
        return True

    def getOctets(self):
        if self.isValid():
            return self._split_octets()
        return []

    def getBinary(self):
        if self.isValid():
            octets = self._split_octets()
            binary_parts = []
            for octet in octets:
                num = int(octet)
                binary_parts.append(format(num, '08b'))
            return '.'.join(binary_parts)
        return ""