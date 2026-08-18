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
                # Replicate std::getline(ss, segment, '/'): segments are the
                # pieces between delimiters, and a trailing delimiter does NOT
                # produce a final empty segment.
                parts = fixed_path.split('/')
                if fixed_path.endswith('/'):
                    parts.pop()
                for segment in parts:
                    # C++ decodes UTF-8 to wide chars, drops '%', and casts
                    # each char back to char (truncation for codepoints > 255).
                    decoded_seg = ''.join(
                        chr(ord(ch) & 0xFF) for ch in segment if ch != '%'
                    )
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
        return list(self._segments)

    def with_end_tag(self):
        return self._with_end_tag