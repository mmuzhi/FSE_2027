class CSVProcessor:
    def __init__(self):
        pass

    def read_csv(self, file_name):
        title = []
        data = []

        try:
            with open(file_name, 'r') as file:
                line = file.readline()
                if line:
                    line = line.rstrip('\n').rstrip('\r')
                    title = line.split(',')
                
                for line in file:
                    line = line.rstrip('\n').rstrip('\r')
                    row = line.split(',')
                    data.append(row)
        except (IOError, OSError):
            pass

        return (title, data)

    def write_csv(self, data, file_name):
        try:
            with open(file_name, 'w') as file:
                for row in data:
                    file.write(','.join(row) + '\n')
        except (IOError, OSError):
            return 0

        return 1

    def process_csv_data(self, N, save_file_name):
        title, data = self.read_csv(save_file_name)
        if N >= len(data[0]):
            return 0

        column_data = []
        for row in data:
            if N < len(row):
                upper_str = row[N].upper()
                column_data.append(upper_str)

        new_data = [title, column_data]

        dot_pos = save_file_name.rfind('.')
        if dot_pos == -1:
            base_name = save_file_name
        else:
            base_name = save_file_name[:dot_pos]

        return self.write_csv(new_data, base_name + "_process.csv")