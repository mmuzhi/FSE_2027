class CSVProcessor:
    def __init__(self):
        pass

    @staticmethod
    def _split_csv_line(line):
        if line == '':
            return []
        parts = line.split(',')
        if line.endswith(','):
            parts.pop()
        return parts

    @staticmethod
    def _ascii_upper(s):
        return ''.join(chr(ord(c) - 32) if 'a' <= c <= 'z' else c for c in s)

    def read_csv(self, file_name):
        title = []
        data = []
        try:
            with open(file_name, 'rb') as f:
                content = f.read()
        except OSError:
            return (title, data)

        if content == b'':
            return (title, data)

        text = content.decode('latin-1')
        lines = text.split('\n')
        if lines and lines[-1] == '':
            lines.pop()

        if not lines:
            return (title, data)

        title = self._split_csv_line(lines[0])
        for line in lines[1:]:
            row = self._split_csv_line(line)
            data.append(row)
        return (title, data)

    def write_csv(self, data, file_name):
        try:
            f = open(file_name, 'wb')
        except OSError:
            return 0
        with f:
            for row in data:
                line = ','.join(row)
                f.write(line.encode('latin-1'))
                f.write(b'\n')
        return 1

    def process_csv_data(self, N, save_file_name):
        title, data = self.read_csv(save_file_name)
        if N < 0 or N >= len(data[0]):
            return 0

        column_data = []
        for row in data:
            if N < len(row):
                upper_str = self._ascii_upper(row[N])
                column_data.append(upper_str)

        new_data = [title, column_data]
        dot = save_file_name.rfind('.')
        if dot == -1:
            base = save_file_name
        else:
            base = save_file_name[:dot]
        output = base + "_process.csv"
        return self.write_csv(new_data, output)