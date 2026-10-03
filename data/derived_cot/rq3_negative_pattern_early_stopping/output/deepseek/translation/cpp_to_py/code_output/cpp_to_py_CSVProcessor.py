import csv
from typing import List, Tuple

class CSVProcessor:
    def __init__(self):
        pass

    def read_csv(self, file_name: str) -> Tuple[List[str], List[List[str]]]:
        title: List[str] = []
        data: List[List[str]] = []
        try:
            with open(file_name, 'r') as f:
                first_line = f.readline()
                if first_line:
                    if first_line.endswith('\n'):
                        first_line = first_line[:-1]
                    title = first_line.split(',')
                for line in f:
                    if line.endswith('\n'):
                        line = line[:-1]
                    row = line.split(',')
                    data.append(row)
        except FileNotFoundError:
            pass
        return title, data

    def write_csv(self, data: List[List[str]], file_name: str) -> int:
        try:
            with open(file_name, 'w') as f:
                for row in data:
                    f.write(','.join(row) + '\n')
            return 1
        except:
            return 0

    def process_csv_data(self, N: int, save_file_name: str) -> int:
        title, data = self.read_csv(save_file_name)
        if not data or N >= len(data[0]):
            return 0

        column_data: List[str] = []
        for row in data:
            if N < len(row):
                column_data.append(row[N].upper())

        new_data = [title, column_data]
        dot_index = save_file_name.rfind('.')
        if dot_index == -1:
            out_name = save_file_name + '_process.csv'
        else:
            out_name = save_file_name[:dot_index] + '_process.csv'
        return self.write_csv(new_data, out_name)