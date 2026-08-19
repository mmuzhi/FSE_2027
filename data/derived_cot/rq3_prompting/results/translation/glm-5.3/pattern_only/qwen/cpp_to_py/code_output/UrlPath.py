class UrlPath:
    def __init__(self):
        self.segments = []
        self._with_end_tag = False

    def add(self, segment):
        self.segments.append(UrlPath.fix_path(segment))

    def parse(self, path, charset):
        if path:
            if path[-1] == '/':
                self._with_end_tag = True

            fixed_path = UrlPath.fix_path(path)
            if fixed_path:
                # Emulate std::getline(ss, segment, '/'): a trailing '/'
                # does not yield an extra empty segment.
                parts = fixed_path.split('/')
                if parts and parts[-1] == '':
                    parts.pop()
                for segment in parts:
                    decoded_seg = ''.join(
                        chr(ord(ch) & 0xFF) for ch in segment if ch != '%'
                    )
                    self.segments.append(decoded_seg)

    @staticmethod
    def fix_path(path):
        if not path:
            return ""
        if path[0] == '/':
            path = path[1:]
        if path and path[-1] == '/':
            path = path[:-1]
        return path

    def get_segments(self):
        return self.segments

    def with_end_tag(self):
        return self._with_end_tag