class CSVProcessor:

    def readCSV(self, fileName, title, data):
        with open(fileName, 'r') as reader:
            line = reader.readline()
            if line:
                line = line.rstrip('\r\n')
                title.extend(line.split(","))
                lineData = reader.readline()
                while lineData:
                    lineData = lineData.rstrip('\r\n')
                    data.append(lineData.split(","))
                    lineData = reader.readline()

    def writeCSV(self, *args):
        if len(args) == 3:
            title, data, fileName = args
        elif len(args) == 2:
            data, fileName = args
            title = None
        else:
            raise TypeError("writeCSV requires 2 or 3 arguments")
        try:
            with open(fileName, 'w') as writer:
                if title is not None:
                    writer.write(",".join(title))
                    writer.write("\n")
                for row in data:
                    writer.write(",".join(row))
                    writer.write("\n")
            return 1
        except IOError:
            return 0

    def processCSVData(self, N, saveFileName):
        title = []
        data = []
        self.readCSV(saveFileName, title, data)
        columnData = []
        for row in data:
            if 0 <= N < len(row):
                columnData.append(row[N].upper())
        newData = []
        newData.append(columnData)
        return self.writeCSV(title, newData, saveFileName.split(".")[0] + "_process.csv")