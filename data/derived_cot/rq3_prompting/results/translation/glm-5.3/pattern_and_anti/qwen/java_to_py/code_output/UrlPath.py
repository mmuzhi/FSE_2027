import re
import traceback
from urllib.parse import unquote_plus


class UrlPath:
    def __init__(self):
        self.segments = []
        self.with_end_tag = False

    def add(self, segment):
        self.segments.append(UrlPath.fix_path(segment))

    def parse(self, path, charset):
        if path is not None and path != "":
            if path.endswith("/"):
                self.with_end_tag = True

            path = UrlPath.fix_path(path)
            if path is not None and path != "":
                split = path.split("/")
                for seg in split:
                    try:
                        # Java's URLDecoder.decode treats '+' as space and
                        # throws on malformed escapes -> unquote_plus + strict
                        decoded_seg = unquote_plus(seg, encoding=charset, errors='strict')
                        self.segments.append(decoded_seg)
                    except Exception:
                        traceback.print_exc()

    @staticmethod
    def fix_path(path):
        if path is None or path == "":
            return ""
        return re.sub(r'^/+|/+$', '', path.strip())

    def get_segments(self):
        return self.segments

    def is_with_end_tag(self):
        return self.with_end_tag