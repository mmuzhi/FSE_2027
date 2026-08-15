class IllegalArgumentException(Exception):
    pass

class ClassCastException(Exception):
    pass

class MetricsCalculator2:
    class Tuple:
        def __init__(self, list, totalNum):
            self._list = list
            self._totalNum = totalNum

        def getList(self):
            return self._list

        def getTotalNum(self):
            return self._totalNum

    @staticmethod
    def mrr(data):
        if not isinstance(data, (list, MetricsCalculator2.Tuple)):
            raise IllegalArgumentException("the input must be a tuple([0,...,1,...],int) or a iteration of list of tuple")

        if isinstance(data, MetricsCalculator2.Tuple):
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
                if tuple is not None and not isinstance(tuple, MetricsCalculator2.Tuple):
                    raise ClassCastException(f"{type(tuple).__name__} cannot be cast to MetricsCalculator2.Tuple")
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

            if separateResult:
                return sum(separateResult) / len(separateResult)
            else:
                return 0.0

    @staticmethod
    def map(data):
        if not isinstance(data, (list, MetricsCalculator2.Tuple)):
            raise IllegalArgumentException("the input must be a tuple([0,...,1,...],int) or a iteration of list of tuple")

        if isinstance(data, MetricsCalculator2.Tuple):
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
                if tuple is not None and not isinstance(tuple, MetricsCalculator2.Tuple):
                    raise ClassCastException(f"{type(tuple).__name__} cannot be cast to MetricsCalculator2.Tuple")
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

            if separateResult:
                return sum(separateResult) / len(separateResult)
            else:
                return 0.0