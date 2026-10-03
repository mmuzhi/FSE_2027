class IPAddress:
    def __init__(self, ipAddress):
        self.ipAddress = ipAddress

    def isValid(self):
        octets = self.ipAddress.split(".")
        if len(octets) != 4:
            return False
        for octet in octets:
            try:
                num = int(octet)
                if num < 0 or num > 255:
                    return False
            except ValueError:
                return False
        return True

    def getOctets(self):
        octets_list = []
        if self.isValid():
            octets = self.ipAddress.split(".")
            for octet in octets:
                octets_list.append(octet)
        return octets_list

    def getBinary(self):
        if self.isValid():
            octets = self.ipAddress.split(".")
            binary_parts = []
            for octet in octets:
                num = int(octet)
                binary_parts.append(format(num, '08b'))
            return ".".join(binary_parts)
        return ""