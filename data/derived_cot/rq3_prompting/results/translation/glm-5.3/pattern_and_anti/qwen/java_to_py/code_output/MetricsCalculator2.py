class Tuple:
    def __init__(self, list_, total_num):
        self.list = list_
        self.total_num = total_num

    def get_list(self):
        return self.list

    def get_total_num(self):
        return self.total_num


class MetricsCalculator2:

    @staticmethod
    def mrr(data):
        if not isinstance(data, (list, Tuple)):
            raise ValueError(
                "the input must be a tuple([0,...,1,...],int) or a iteration of list of tuple"
            )

        if isinstance(data, Tuple):
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

            return sum(separate_result) / len(separate_result) if separate_result else 0.0

    @staticmethod
    def map(data):
        if not isinstance(data, (list, Tuple)):
            raise ValueError(
                "the input must be a tuple([0,...,1,...],int) or a iteration of list of tuple"
            )

        if isinstance(data, Tuple):
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

            return sum(separate_result) / len(separate_result) if separate_result else 0.0