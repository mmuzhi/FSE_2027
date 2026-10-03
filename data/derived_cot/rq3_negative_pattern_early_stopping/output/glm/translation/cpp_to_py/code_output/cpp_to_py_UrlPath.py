class UrlPath:
    def __init__(self):
        self._segments = []
        self._with_end_tag = False

    def add(self, segment):
        self._segments.append(UrlPath.fix_path(segment))

    def parse(self, path, charset):
        if path:
            if path[-1] == '/':
                self._with_end_tag = True

            fixed_path = UrlPath.fix_path(path)
            if fixed_path:
                for segment in fixed_path.split('/'):
                    decoded_seg = ''
                    for ch in segment:
                        if ch == '%':
                            pass
                        else:
                            decoded_seg += chr(ord(ch) & 0xFF)
                    self._segments.append(decoded_seg)

    @staticmethod
    def fix_path(path):
        if not path:
            return ""
        segment_str = path
        if segment_str[0] == '/':
            segment_str = segment_str[1:]
        if segment_str and segment_str[-1] == '/':
            segment_str = segment_str[:-1]
        return segment_str

    def get_segments(self):
        return self._segments

    def with_end_tag(self):
        return self._with_end_tag