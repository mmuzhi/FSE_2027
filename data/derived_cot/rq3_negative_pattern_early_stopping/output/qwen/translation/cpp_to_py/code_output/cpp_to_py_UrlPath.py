class UrlPath:
    def __init__(self):
        self.segments = []
        self._with_end_tag = False

    def add(self, segment):
        fixed_segment = self.fix_path(segment)
        self.segments.append(fixed_segment)

    def parse(self, path, charset):
        if path and path[-1] == '/':
            self._with_end_tag = True
        
        fixed_path = self.fix_path(path)
        if fixed_path:
            segments_list = fixed_path.split('/')
            for seg in segments_list:
                decoded_seg = ''.join([c for c in seg if c != '%'])
                self.segments.append(decoded_seg)

    @staticmethod
    def fix_path(path):
        if path.startswith('/'):
            path = path[1:]
        if path.endswith('/'):
            path = path[:-1]
        return path

    def get_segments(self):
        return self.segments

    def with_end_tag(self):
        return self._with_end_tag