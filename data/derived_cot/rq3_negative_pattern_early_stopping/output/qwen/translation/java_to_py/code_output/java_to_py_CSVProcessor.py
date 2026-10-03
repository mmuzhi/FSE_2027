import os

class CSVProcessor:

    def read_csv(self, file_name, title, data):
        try:
            with open(file_name, 'r') as file:
                line = file.readline().strip()
                if line:
                    title.extend(line.split(','))
                    for line_data in file:
                        line_data = line_data.strip()
                        if line_data:
                            data.append(line_data.split(','))
        except IOError as e:
            raise e

    def write_csv(self, title, data, file_name):
        try:
            with open(file_name, 'w') as writer:
                writer.write(','.join(title))
                writer.write('\n')
                for row in data:
                    writer.write(','.join(row))
                    writer.write('\n')
            return 1
        except IOError:
            return 0

    def write_csv_no_title(self, data, file_name):
        try:
            with open(file_name, 'w') as writer:
                for row in data:
                    writer.write(','.join(row))
                    writer.write('\n')
            return 1
        except IOError:
            return 0

    def process_csv_data(self, N, save_file_name):
        title = []
        data = []
        self.read_csv(save_file_name, title, data)
        if not data:
            return 0
        column_data = []
        for row in data:
            if N < len(row):
                column_data.append(row[N].upper())
        new_data = [column_data]
        output_file = os.path.splitext(save_file_name)[0] + "_process.csv"
        return self.write_csv(title, new_data, output_file)