class CSVProcessor:
    def __init__(self):
        pass

    @staticmethod
    def _split_csv_line(line):
        if line == "":
            return []
        row = []
        start = 0
        while True:
            idx = line.find(",", start)
            if idx == -1:
                row.append(line[start:])
                break
            row.append(line[start:idx])
            start = idx + 1
            if start == len(line):
                break
        return row

    @staticmethod
    def _ascii_upper(s):
        return "".join(chr(ord(c) - 32) if "a" <= c <= "z" else c for c in s)

    def read_csv(self, file_name):
        try:
            file = open(file_name, "r", encoding="latin-1")
        except OSError:
            return [], []
        with file:
            first_line = file.readline()
            if first_line == "":
                return [], []
            title = self._split_csv_line(first_line.rstrip("\n"))
            data = []
            for line in file:
                row = self._split_csv_line(line.rstrip("\n"))
                data.append(row)
        return title, data

    def write_csv(self, data, file_name):
        try:
            file = open(file_name, "w", encoding="latin-1")
        except OSError:
            return 0
        with file:
            for row in data:
                file.write(",".join(row) + "\n")
        return 1

    def process_csv_data(self, N, save_file_name):
        title, data = self.read_csv(save_file_name)
        if not data or N < 0 or N >= len(data[0]):
            return 0

        column_data = []
        for row in data:
            if N < len(row):
                column_data.append(self._ascii_upper(row[N]))

        new_data = [title, column_data]
        idx = save_file_name.rfind(".")
        if idx == -1:
            base = save_file_name
        else:
            base = save_file_name[:idx]
        return self.write_csv(new_data, base + "_process.csv")