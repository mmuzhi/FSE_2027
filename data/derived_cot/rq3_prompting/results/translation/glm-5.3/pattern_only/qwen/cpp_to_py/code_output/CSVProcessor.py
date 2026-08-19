class CSVProcessor:

    def __init__(self):
        pass

    @staticmethod
    def _split_line(line):
        # Emulates repeated std::getline(stream, item, ','):
        # empty input yields no fields; a trailing delimiter drops the final empty field.
        if line == '':
            return []
        parts = line.split(',')
        if line.endswith(','):
            parts.pop()
        return parts

    def read_csv(self, file_name):
        title = []
        data = []

        try:
            f = open(file_name, 'r', newline='')
        except OSError:
            return title, data

        with f:
            content = f.read()

        # C++ getline splits only on '\n' and drops the final (failed) read at EOF.
        lines = content.split('\n')
        if lines and lines[-1] == '':
            lines.pop()

        if lines:
            title = self._split_line(lines[0])
            for line in lines[1:]:
                data.append(self._split_line(line))

        return title, data

    def write_csv(self, data, file_name):
        try:
            f = open(file_name, 'w', newline='')
        except OSError:
            return 0

        with f:
            for row in data:
                f.write(','.join(row))
                f.write('\n')

        return 1

    def process_csv_data(self, N, save_file_name):
        title, data = self.read_csv(save_file_name)
        if N >= len(data[0]):
            return 0

        column_data = []
        for row in data:
            if N < len(row):
                upper_str = row[N]
                # ::toupper in the C locale: only ASCII 'a'-'z' are transformed.
                upper_str = ''.join(
                    chr(ord(c) - 32) if 'a' <= c <= 'z' else c
                    for c in upper_str
                )
                column_data.append(upper_str)

        new_data = [title, column_data]
        idx = save_file_name.rfind('.')
        base = save_file_name if idx == -1 else save_file_name[:idx]
        return self.write_csv(new_data, base + '_process.csv')