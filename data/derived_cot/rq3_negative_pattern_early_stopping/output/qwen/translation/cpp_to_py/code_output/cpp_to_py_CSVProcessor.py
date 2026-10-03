import csv
import os

class CSVProcessor:
    def __init__(self):
        pass

    def read_csv(self, file_name):
        try:
            with open(file_name, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                title = []
                data = []
                first_row = next(reader, None)
                if first_row is not None:
                    title = first_row
                for row in reader:
                    data.append(row)
                return title, data
        except FileNotFoundError:
            return [], []
        except Exception as e:
            # In C++, if file not open, return empty vectors. We return empty lists on any exception.
            return [], []

    def write_csv(self, data, file_name):
        try:
            with open(file_name, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                for row in data:
                    writer.writerow(row)
            return 1
        except Exception:
            return 0

    def process_csv_data(self, N, save_file_name):
        # Extract the base name and extension for the output file
        base_name = save_file_name
        if '.' in base_name:
            base_name = base_name.rsplit('.', 1)[0]
        else:
            base_name = save_file_name
        output_file = base_name + "_process.csv"

        title, data = self.read_csv(save_file_name)
        if not data or N >= len(title):
            return 0

        # Process the Nth column (0-indexed) from each row
        column_data = []
        for row in data:
            if N < len(row):
                # Convert the string to uppercase
                column_data.append(row[N].upper())
            else:
                # If the row doesn't have the Nth column, skip it? But the C++ code doesn't skip, it just doesn't push.
                # Actually, the C++ code checks N < row.size() for each row. So we do the same.
                # But note: the C++ code only processes rows that have at least N+1 columns. We do the same.
                # We'll skip this row for the column_data? But the C++ code doesn't include rows without the column.
                # However, the C++ code does: if (N < row.size()) then process, else skip.
                # So we skip rows without the column.
                continue

        # Create new data: [title, column_data]
        new_data = [title, column_data]
        self.write_csv(new_data, output_file)
        return 1