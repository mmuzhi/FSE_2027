def _java_split(s, delim):
    if delim not in s:
        return [s]
    parts = s.split(delim)
    while parts and parts[-1] == "":
        parts.pop()
    return parts

class CSVProcessor:
    def readCSV(self, fileName, title, data):
        with open(fileName, 'r', errors='replace') as reader:
            line = reader.readline()
            if line != '':
                title.extend(_java_split(line.rstrip('\n'), ','))
                for lineData in reader:
                    data.append(_java_split(lineData.rstrip('\n'), ','))

    def writeCSV(self, *args):
        if len(args) == 2:
            data, fileName = args
            title = None
        else:
            title, data, fileName = args
        try:
            with open(fileName, 'w', errors='replace') as writer:
                if title is not None:
                    writer.write(','.join(title) + '\n')
                for row in data:
                    writer.write(','.join(row) + '\n')
            return 1
        except OSError:
            return 0

    def processCSVData(self, N, saveFileName):
        title = []
        data = []
        self.readCSV(saveFileName, title, data)
        columnData = []
        for row in data:
            if N < len(row):
                if N < 0:
                    raise IndexError("Index out of range")
                columnData.append(row[N].upper())
        newData = [columnData]
        return self.writeCSV(title, newData, _java_split(saveFileName, ".")[0] + "_process.csv")