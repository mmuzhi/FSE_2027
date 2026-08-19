class IPAddress:
    def __init__(self, ip_address):
        self._ip_address = ip_address

    @staticmethod
    def _split_java_style(s):
        # Java's String.split("\\.") discards trailing empty strings.
        parts = s.split(".")
        while parts and parts[-1] == "":
            parts.pop()
        return parts

    @staticmethod
    def _parse_java_int(s):
        # Mirror Integer.parseInt: optional sign followed by decimal digits only
        # (rejects whitespace and underscores, which Python's int() would accept).
        body = s[1:] if s[:1] in ("+", "-") else s
        if not body or not body.isdecimal():
            raise ValueError(f'For input string: "{s}"')
        return int(s)

    def is_valid(self):
        octets = self._split_java_style(self._ip_address)
        if len(octets) != 4:
            return False
        for octet in octets:
            try:
                num = self._parse_java_int(octet)
                if num < 0 or num > 255:
                    return False
            except ValueError:
                return False
        return True

    def get_octets(self):
        octets_list = []
        if self.is_valid():
            octets_list.extend(self._split_java_style(self._ip_address))
        return octets_list

    def get_binary(self):
        if self.is_valid():
            parts = [
                format(self._parse_java_int(octet), "08b")
                for octet in self._split_java_style(self._ip_address)
            ]
            return ".".join(parts)
        return ""