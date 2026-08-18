class CSVProcessor:

    def read_csv(self, file_name, title, data):
        with open(file_name, "r") as reader:
            line = reader.readline()
            if line:  # Java readLine() != null (EOF in Python is "")
                title.extend(_java_split(line.rstrip("\n")))
                for line_data in reader:
                    data.append(_java_split(line_data.rstrip("\n")))

    def write_csv(self, *args):
        # Emulates the two Java overloads: writeCSV(title, data, fileName)
        # and writeCSV(data, fileName).
        if len(args) == 2:
            rows = args[0]
            file_name = args[1]
        elif len(args) == 3:
            rows = [args[0]] + list(args[1])
            file_name = args[2]
        else:
            raise TypeError("write_csv() expects (title, data, file_name) or (data, file_name)")
        try:
            with open(file_name, "w") as writer:
                for row in rows:
                    writer.write(",".join(row) + "\n")
            return 1
        except OSError:
            return 0

    def process_csv_data(self, N, save_file_name):
        title = []
        data = []
        self.read_csv(save_file_name, title, data)

        column_data = []
        for row in data:
            if N < len(row):
                if N < 0:
                    # Java's List.get(N) throws IndexOutOfBoundsException for negative N
                    raise IndexError("Index: %d, Size: %d" % (N, len(row)))
                column_data.append(row[N].upper())

        new_data = [column_data]

        return self.write_csv(title, new_data,
                              save_file_name.split(".")[0] + "_process.csv")


def _java_split(line):
    # Java's String.split(",") removes trailing empty fields,
    # but returns [line] when the separator never occurs (even for "").
    parts = line.split(",")
    if "," in line:
        while parts and parts[-1] == "":
            parts.pop()
    return parts