class CSVProcessor:
    def __init__(self):
        pass

    @staticmethod
    def _split_fields(line):
        # Mimics repeated std::getline(stream, item, ','):
        # a trailing delimiter produces no final empty field; empty line -> [].
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
            # newline='' keeps '\r' like C++ on Unix (no newline translation)
            file = open(file_name, 'r', newline='')
        except OSError:
            return title, data

        with file:
            content = file.read()

        lines = content.split('\n')
        # Emulate std::getline loop: trailing '\n' (or empty file) yields no extra line
        if lines and lines[-1] == '' and (content.endswith('\n') or content == ''):
            lines.pop()

        if lines:
            title = self._split_fields(lines[0])

        data = [self._split_fields(line) for line in lines[1:]]
        return title, data

    def write_csv(self, data, file_name):
        try:
            file = open(file_name, 'w', newline='')
        except OSError:
            return 0

        with file:
            for row in data:
                file.write(','.join(row) + '\n')
        return 1

    def process_csv_data(self, N, save_file_name):
        title, data = self.read_csv(save_file_name)
        if N >= len(data[0]):  # IndexError mirrors C++ UB on empty data
            return 0

        column_data = []
        for row in data:
            if N < len(row):
                column_data.append(row[N].upper())

        new_data = [title, column_data]
        idx = save_file_name.rfind('.')
        base = save_file_name if idx == -1 else save_file_name[:idx]
        return self.write_csv(new_data, base + '_process.csv')