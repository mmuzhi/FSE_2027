import re
from urllib.parse import unquote
import traceback


class UrlPath:
    def __init__(self):
        self.segments = []
        self.with_end_tag = False

    def add(self, segment: str) -> None:
        self.segments.append(self.fix_path(segment))

    def parse(self, path: str, charset: str) -> None:
        if path is not None and path != "":
            if path.endswith("/"):
                self.with_end_tag = True

            path = self.fix_path(path)
            if path is not None and path != "":
                for seg in path.split("/"):
                    try:
                        decoded_seg = unquote(seg, encoding=charset, errors='strict')
                        self.segments.append(decoded_seg)
                    except Exception:
                        traceback.print_exc()

    @staticmethod
    def fix_path(path: str) -> str:
        if path is None or path == "":
            return ""
        segment_str = path.strip()
        segment_str = re.sub(r'^/+|/+$', '', segment_str)
        return segment_str

    def get_segments(self):
        return self.segments

    def is_with_end_tag(self):
        return self.with_end_tag