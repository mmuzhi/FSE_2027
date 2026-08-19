def _java_split(s, sep):
    # Emulates Java's String.split(sep): zero matches -> [s]; trailing empty strings dropped.
    if sep not in s:
        return [s]
    parts = s.split(sep)
    while parts and parts[-1] == "":
        parts.pop()
    return parts


class CSVProcessor:

    def readCSV(self, fileName, title, data):
        with open(fileName) as reader:
            content = reader.read()
        # Emulate BufferedReader.readLine(): universal-newline translation turns
        # '\r' and '\r\n' into '\n'; drop the final empty piece after the last '\n'.
        lines = content.split("\n")
        if lines and lines[-1] == "":
            lines.pop()
        if lines:
            title.extend(_java_split(lines[0], ","))
            for line_data in lines[1:]:
                data.append(_java_split(line_data, ","))

    def writeCSV(self, *args):
        # Overload: writeCSV(title, data, fileName) or writeCSV(data, fileName)
        if len(args) == 3:
            title, data, fileName = args
        elif len(args) == 2:
            title, data, fileName = None, args[0], args[1]
        else:
            raise TypeError("writeCSV expected 2 or 3 arguments")
        try:
            with open(fileName, "w") as writer:
                if title is not None:
                    writer.write(",".join(title))
                    writer.write("\n")
                for row in data:
                    writer.write(",".join(row))
                    writer.write("\n")
            return 1
        except OSError:
            return 0

    def processCSVData(self, N, saveFileName):
        title = []
        data = []
        self.readCSV(saveFileName, title, data)

        column_data = []
        for row in data:
            if N < len(row):
                if N < 0:
                    # Java List.get(negative) throws; avoid Python's negative indexing
                    raise IndexError(f"Index: {N}, Size: {len(row)}")
                column_data.append(row[N].upper())

        new_data = [column_data]

        return self.writeCSV(title, new_data, _java_split(saveFileName, ".")[0] + "_process.csv")