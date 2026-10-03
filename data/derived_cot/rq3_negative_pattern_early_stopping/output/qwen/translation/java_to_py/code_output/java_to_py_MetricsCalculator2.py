class Tuple:
    def __init__(self, lst, total_num):
        self.list = lst
        self.totalNum = total_num

    def get_list(self):
        return self.list

    def get_total_num(self):
        return self.totalNum

def mrr(data):
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
    elif isinstance(data, list):
        if not all(isinstance(item, Tuple) for item in data):
            raise ValueError("the input must be a tuple([0,...,1,...],int) or a iteration of list of tuple")
        separate_results = []
        for item in data:
            sub_list = item.get_list()
            total_num = item.get_total_num()
            if total_num == 0:
                separate_results.append(0.0)
            else:
                mr = 0.0
                for i in range(len(sub_list)):
                    if sub_list[i] == 1:
                        mr = 1.0 / (i + 1)
                        break
                separate_results.append(mr)
        if separate_results:
            return sum(separate_results) / len(separate_results)
        else:
            return 0.0
    else:
        raise ValueError("the input must be a tuple([0,...,1,...],int) or a iteration of list of tuple")

def map_score(data):
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
    elif isinstance(data, list):
        if not all(isinstance(item, Tuple) for item in data):
            raise ValueError("the input must be a tuple([0,...,1,...],int) or a iteration of list of tuple")
        separate_results = []
        for item in data:
            sub_list = item.get_list()
            total_num = item.get_total_num()
            if total_num == 0:
                separate_results.append(0.0)
            else:
                ap = 0.0
                count = 0
                for i in range(len(sub_list)):
                    if sub_list[i] == 1:
                        count += 1
                        ap += count / (i + 1.0)
                separate_results.append(ap / total_num)
        if separate_results:
            return sum(separate_results) / len(separate_results)
        else:
            return 0.0
    else:
        raise ValueError("the input must be a tuple([0,...,1,...],int) or a iteration of list of tuple")