class UrlPath:
    def __init__(self):
        self.segments = []
        self._with_end_tag = False

    def add(self, segment):
        self.segments.append(self.fix_path(segment))

    def parse(self, path, charset):
        if not path:
            return

        if path[-1] == '/':
            self._with_end_tag = True

        fixed_path = self.fix_path(path)
        if fixed_path:
            for segment in self._split_getline(fixed_path):
                decoded_seg = []
                for ch in segment:
                    if ch == '%':
                        continue
                    decoded_seg.append(chr(ord(ch) & 0xFF))
                self.segments.append(''.join(decoded_seg))

    @staticmethod
    def fix_path(path):
        if not path:
            return ""
        if path[0] == '/':
            path = path[1:]
        if path and path[-1] == '/':
            path = path[:-1]
        return path

    @staticmethod
    def _split_getline(s):
        tokens = []
        current = []
        for ch in s:
            if ch == '/':
                tokens.append(''.join(current))
                current = []
            else:
                current.append(ch)
        if s and s[-1] != '/':
            tokens.append(''.join(current))
        return tokens

    def get_segments(self):
        return self.segments

    def with_end_tag(self):
        return self._with_end_tag