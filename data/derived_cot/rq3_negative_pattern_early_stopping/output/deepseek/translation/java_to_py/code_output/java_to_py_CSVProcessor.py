import os

class CSVProcessor:
    def read_csv(self, filename, title, data):
        with open(filename, 'r') as f:
            line = f.readline()
            if line:
                parts = line.rstrip('\n').split(',')
                while parts and parts[-1] == '':
                    parts.pop()
                title.extend(parts)

                for line_data in f:
                    line_data = line_data.rstrip('\n')
                    parts = line_data.split(',')
                    while parts and parts[-1] == '':
                        parts.pop()
                    data.append(parts)

    def write_csv(self, title, data, filename):
        try:
            with open(filename, 'w') as f:
                f.write(','.join(title) + '\n')
                for row in data:
                    f.write(','.join(row) + '\n')
            return 1
        except (IOError, OSError):
            return 0

    def write_csv_no_title(self, data, filename):
        try:
            with open(filename, 'w') as f:
                for row in data:
                    f.write(','.join(row) + '\n')
            return 1
        except (IOError, OSError):
            return 0

    def process_csv_data(self, n, save_filename):
        title = []
        data = []
        self.read_csv(save_filename, title, data)

        column_data = []
        for row in data:
            if n < len(row):
                column_data.append(row[n].upper())

        new_data = [column_data]
        base = save_filename.split('.')[0] + '_process.csv'
        return self.write_csv(title, new_data, base)