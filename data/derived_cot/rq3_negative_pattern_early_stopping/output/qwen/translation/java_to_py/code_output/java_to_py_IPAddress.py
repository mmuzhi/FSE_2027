class IPAddress:
    def __init__(self, ipAddress):
        self.ipAddress = ipAddress

    def isValid(self):
        octets = self.ipAddress.split('.')
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
        if not self.isValid():
            return []
        octets_list = []
        octets = self.ipAddress.split('.')
        for octet in octets:
            octets_list.append(octet)
        return octets_list

    def getBinary(self):
        if not self.isValid():
            return ""
        binary_parts = []
        octets = self.ipAddress.split('.')
        for octet in octets:
            num = int(octet)
            # Convert to binary and remove the '0b' prefix
            bin_str = bin(num)[2:]
            # Pad with zeros to make sure it's 8 bits
            bin_str = bin_str.zfill(8)
            binary_parts.append(bin_str)
        # Join with dots and remove the last dot if any (but we are appending each and then joining, so no trailing dot)
        return ".".join(binary_parts)