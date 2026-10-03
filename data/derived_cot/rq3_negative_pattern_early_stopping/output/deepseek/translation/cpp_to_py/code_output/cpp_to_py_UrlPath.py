class UrlPath:
    def __init__(self):
        self._segments = []
        self._with_end_tag = False

    def add(self, segment: str):
        self._segments.append(UrlPath.fix_path(segment))

    def parse(self, path: str, charset: str):
        if path:
            if path.endswith('/'):
                self._with_end_tag = True

            fixed_path = UrlPath.fix_path(path)
            if fixed_path:
                for segment in fixed_path.split('/'):
                    decoded_seg_chars = []
                    for ch in segment:
                        if ch == '%':
                            continue
                        else:
                            byte_val = ord(ch) & 0xFF
                            decoded_seg_chars.append(chr(byte_val))
                    decoded_seg = ''.join(decoded_seg_chars)
                    self._segments.append(decoded_seg)

    @staticmethod
    def fix_path(path: str) -> str:
        if not path:
            return ""
        segment_str = path
        if segment_str.startswith('/'):
            segment_str = segment_str[1:]
        if segment_str.endswith('/'):
            segment_str = segment_str[:-1]
        return segment_str

    def get_segments(self):
        return self._segments

    def with_end_tag(self) -> bool:
        return self._with_end_tag