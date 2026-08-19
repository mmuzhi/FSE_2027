import re
import traceback
from urllib.parse import unquote_plus

# Java's URLDecoder.decode throws on malformed '%' escapes (e.g. "%zz", trailing '%');
# Python's unquote_plus silently passes them through, so guard first to keep behavior identical.
_BAD_ESCAPE = re.compile(r'%(?![0-9A-Fa-f]{2})')


def _url_decode(s, charset):
    if _BAD_ESCAPE.search(s):
        raise ValueError("URLDecoder: Illegal hex characters in escape (%) pattern")
    # '+' -> space, then percent-decode; 'replace' matches Java's byte-to-String decoding
    return unquote_plus(s, encoding=charset, errors='replace')


class UrlPath:
    def __init__(self):
        self._segments = []
        self._with_end_tag = False

    def add(self, segment):
        self._segments.append(UrlPath.fix_path(segment))

    def parse(self, path, charset):
        if path is not None and path != "":
            if path.endswith("/"):
                self._with_end_tag = True

            path = UrlPath.fix_path(path)
            if path is not None and path != "":
                for seg in path.split("/"):
                    try:
                        decoded_seg = _url_decode(seg, charset)
                        self._segments.append(decoded_seg)
                    except Exception:
                        traceback.print_exc()

    @staticmethod
    def fix_path(path):
        if path is None or path == "":
            return ""
        return re.sub(r'^/+|/+$', '', path.strip())

    def get_segments(self):
        return self._segments

    def is_with_end_tag(self):
        return self._with_end_tag