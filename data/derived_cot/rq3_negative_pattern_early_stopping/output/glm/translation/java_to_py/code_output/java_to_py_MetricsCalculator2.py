class MetricsCalculator2:

    @staticmethod
    def mrr(data):
        if not isinstance(data, (list, MetricsCalculator2.Tuple)):
            raise ValueError("the input must be a tuple([0,...,1,...],int) or a iteration of list of tuple")

        if isinstance(data, MetricsCalculator2.Tuple):
            tuple_ = data
            sub_list = tuple_.get_list()
            total_num = tuple_.get_total_num()

            if total_num == 0:
                return 0.0

            mr = 0.0
            for i in range(len(sub_list)):
                if sub_list[i] == 1:
                    mr = 1.0 / (i + 1)
                    break
            return mr
        else:
            tuple_list = data
            separate_result = []

            for tuple_ in tuple_list:
                sub_list = tuple_.get_list()
                total_num = tuple_.get_total_num()

                if total_num == 0:
                    separate_result.append(0.0)
                else:
                    mr = 0.0
                    for i in range(len(sub_list)):
                        if sub_list[i] == 1:
                            mr = 1.0 / (i + 1)
                            break
                    separate_result.append(mr)

            if not separate_result:
                return 0.0
            return sum(separate_result) / len(separate_result)

    @staticmethod
    def map(data):
        if not isinstance(data, (list, MetricsCalculator2.Tuple)):
            raise ValueError("the input must be a tuple([0,...,1,...],int) or a iteration of list of tuple")

        if isinstance(data, MetricsCalculator2.Tuple):
            tuple_ = data
            sub_list = tuple_.get_list()
            total_num = tuple_.get_total_num()

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
            tuple_list = data
            separate_result = []

            for tuple_ in tuple_list:
                sub_list = tuple_.get_list()
                total_num = tuple_.get_total_num()

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

            if not separate_result:
                return 0.0
            return sum(separate_result) / len(separate_result)

    class Tuple:
        def __init__(self, list_, total_num):
            self._list = list_
            self._total_num = total_num

        def get_list(self):
            return self._list

        def get_total_num(self):
            return self._total_num