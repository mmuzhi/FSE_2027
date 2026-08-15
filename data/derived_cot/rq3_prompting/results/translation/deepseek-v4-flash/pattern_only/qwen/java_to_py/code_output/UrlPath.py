import re
import traceback
import unicodedata

_HEX_BYTE_RE = re.compile(r'(?:[0-9a-fA-F]{2}|[+-][0-9a-fA-F])')


def _parse_hex_byte(hex_str):
    if not _HEX_BYTE_RE.fullmatch(hex_str):
        raise ValueError
    return int(hex_str, 16)


def _is_java_whitespace(ch):
    cp = ord(ch)
    if cp in (0x00A0, 0x2007, 0x202F):
        return False
    if cp in (0x0009, 0x000A, 0x000B, 0x000C, 0x000D) or 0x001C <= cp <= 0x001F:
        return True
    return unicodedata.category(ch) in ('Zs', 'Zl', 'Zp')


def _java_strip(s):
    start = 0
    end = len(s)
    while start < end and _is_java_whitespace(s[start]):
        start += 1
    while end > start and _is_java_whitespace(s[end - 1]):
        end -= 1
    return s[start:end]


def _utf16_code_units(s):
    units = []
    for ch in s:
        cp = ord(ch)
        if cp >= 0x10000:
            cp -= 0x10000
            units.append(0xD800 + (cp >> 10))
            units.append(0xDC00 + (cp & 0x3FF))
        else:
            units.append(cp)
    return units


def _url_decode(s, charset):
    units = _utf16_code_units(s)
    out = bytearray()
    i = 0
    n = len(units)
    while i < n:
        u = units[i]
        if u == 0x2B:  # '+'
            out.append(0x20)
            i += 1
        elif u == 0x25:  # '%'
            if i + 2 >= n:
                raise ValueError("URLDecoder: Incomplete trailing escape (%) pattern")
            hex_str = chr(units[i + 1]) + chr(units[i + 2])
            try:
                v = _parse_hex_byte(hex_str)
            except ValueError:
                raise ValueError("URLDecoder: Invalid hex digits in escape (%) pattern") from None
            out.append(v & 0xFF)
            i += 3
        else:
            out.append(u & 0xFF)
            i += 1
    return out.decode(charset, errors='replace')


class UrlPath:
    def __init__(self):
        self._segments = []
        self._withEndTag = False

    def add(self, segment):
        self._segments.append(self.fixPath(segment))

    def parse(self, path, charset):
        if path is not None and path != "":
            if path.endswith("/"):
                self._withEndTag = True

            path = self.fixPath(path)
            if path is not None and path != "":
                for seg in path.split("/"):
                    try:
                        decoded_seg = _url_decode(seg, charset)
                        self._segments.append(decoded_seg)
                    except Exception:
                        traceback.print_exc()

    @staticmethod
    def fixPath(path):
        if path is None or path == "":
            return ""
        segment_str = re.sub(r'^/+|/+$', '', _java_strip(path))
        return segment_str

    def getSegments(self):
        return self._segments

    def isWithEndTag(self):
        return self._withEndTag