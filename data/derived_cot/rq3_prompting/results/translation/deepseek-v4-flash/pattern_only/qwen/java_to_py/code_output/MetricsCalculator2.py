class Tuple:
    def __init__(self, list, totalNum):
        self.list = list
        self.totalNum = totalNum

    def getList(self):
        return self.list

    def getTotalNum(self):
        return self.totalNum


class MetricsCalculator2:
    @staticmethod
    def mrr(data):
        if not isinstance(data, (list, Tuple)):
            raise ValueError("the input must be a tuple([0,...,1,...],int) or a iteration of list of tuple")

        if isinstance(data, Tuple):
            tuple = data
            subList = tuple.getList()
            totalNum = tuple.getTotalNum()

            if totalNum == 0:
                return 0.0

            mr = 0.0
            for i, val in enumerate(subList):
                if val == 1:
                    mr = 1.0 / (i + 1)
                    break
            return mr
        else:
            tupleList = data
            separateResult = []

            for tuple in tupleList:
                if not isinstance(tuple, Tuple):
                    raise TypeError("element is not a Tuple")
                subList = tuple.getList()
                totalNum = tuple.getTotalNum()

                if totalNum == 0:
                    separateResult.append(0.0)
                else:
                    mr = 0.0
                    for i, val in enumerate(subList):
                        if val == 1:
                            mr = 1.0 / (i + 1)
                            break
                    separateResult.append(mr)

            if not separateResult:
                return 0.0
            return sum(separateResult) / len(separateResult)

    @staticmethod
    def map(data):
        if not isinstance(data, (list, Tuple)):
            raise ValueError("the input must be a tuple([0,...,1,...],int) or a iteration of list of tuple")

        if isinstance(data, Tuple):
            tuple = data
            subList = tuple.getList()
            totalNum = tuple.getTotalNum()

            if totalNum == 0:
                return 0.0

            ap = 0.0
            count = 0
            for i, val in enumerate(subList):
                if val == 1:
                    count += 1
                    ap += count / (i + 1.0)
            return ap / totalNum
        else:
            tupleList = data
            separateResult = []

            for tuple in tupleList:
                if not isinstance(tuple, Tuple):
                    raise TypeError("element is not a Tuple")
                subList = tuple.getList()
                totalNum = tuple.getTotalNum()

                if totalNum == 0:
                    separateResult.append(0.0)
                else:
                    ap = 0.0
                    count = 0
                    for i, val in enumerate(subList):
                        if val == 1:
                            count += 1
                            ap += count / (i + 1.0)
                    separateResult.append(ap / totalNum)

            if not separateResult:
                return 0.0
            return sum(separateResult) / len(separateResult)


MetricsCalculator2.Tuple = Tuple