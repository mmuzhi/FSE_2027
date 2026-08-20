class MetricsCalculator2:

    class Tuple:
        def __init__(self, list, total_num):
            self.list = list
            self.total_num = total_num

        def get_list(self):
            return self.list

        def get_total_num(self):
            return self.total_num

    @staticmethod
    def mrr(data):
        if not isinstance(data, list) and not isinstance(data, MetricsCalculator2.Tuple):
            raise ValueError(
                "the input must be a tuple([0,...,1,...],int) or a iteration of list of tuple"
            )

        if isinstance(data, MetricsCalculator2.Tuple):
            sub_list = data.get_list()
            total_num = data.get_total_num()

            if total_num == 0:
                return 0.0

            mr = 0.0
            for i in range(len(sub_list)):
                if sub_list[i] == 1:
                    mr = 1.0 / (i + 1)
                    break
            return mr
        else:
            separate_result = []

            for tup in data:
                sub_list = tup.get_list()
                total_num = tup.get_total_num()

                if total_num == 0:
                    separate_result.append(0.0)
                else:
                    mr = 0.0
                    for i in range(len(sub_list)):
                        if sub_list[i] == 1:
                            mr = 1.0 / (i + 1)
                            break
                    separate_result.append(mr)

            if separate_result:
                return sum(separate_result) / len(separate_result)
            return 0.0

    @staticmethod
    def map(data):
        if not isinstance(data, list) and not isinstance(data, MetricsCalculator2.Tuple):
            raise ValueError(
                "the input must be a tuple([0,...,1,...],int) or a iteration of list of tuple"
            )

        if isinstance(data, MetricsCalculator2.Tuple):
            sub_list = data.get_list()
            total_num = data.get_total_num()

            if total_num == 0:
                return 0.0

            ap = 0.0
            count = 0
            for i in range(len(sub_list)):
                if sub_list[i] == 1:
                    count += 1
                    ap += count / (i + 1.0)
            return ap / total_num
        else:
            separate_result = []

            for tup in data:
                sub_list = tup.get_list()
                total_num = tup.get_total_num()

                if total_num == 0:
                    separate_result.append(0.0)
                else:
                    ap = 0.0
                    count = 0
                    for i in range(len(sub_list)):
                        if sub_list[i] == 1:
                            count += 1
                            ap += count / (i + 1.0)
                    separate_result.append(ap / total_num)

            if separate_result:
                return sum(separate_result) / len(separate_result)
            return 0.0