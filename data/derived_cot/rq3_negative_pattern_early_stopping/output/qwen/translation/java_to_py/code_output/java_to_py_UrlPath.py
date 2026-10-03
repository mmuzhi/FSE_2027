import urllib.parse
from typing import List

class UrlPath:
    def __init__(self):
        self.segments: List[str] = []
        self.withEndTag: bool = False

    def add(self, segment: str) -> None:
        self.segments.append(self._fix_path(segment))

    def parse(self, path: str, charset: str) -> None:
        if path is not None and path != "":
            if path.endswith("/"):
                self.withEndTag = True

            fixed_path = self._fix_path(path)
            if fixed_path is not None and fixed_path != "":
                segments = fixed_path.split("/")
                for seg in segments:
                    try:
                        decoded_seg = urllib.parse.unquote(seg, encoding=charset)
                        self.segments.append(decoded_seg)
                    except Exception as e:
                        print(f"Error decoding segment: {seg}")
                        print(e)

    def _fix_path(self, path: str) -> str:
        if path is None or path == "":
            return ""
        # Strip leading/trailing whitespace and remove leading/trailing slashes
        path = path.strip().strip('/')
        return path

    def get_segments(self) -> List[str]:
        return self.segments

    def is_with_end_tag(self) -> bool:
        return self.withEndTag