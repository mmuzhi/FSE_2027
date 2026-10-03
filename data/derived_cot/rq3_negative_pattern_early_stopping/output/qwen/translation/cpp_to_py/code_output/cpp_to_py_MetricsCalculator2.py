class MetricsCalculator2:
    @staticmethod
    def mrr(data):
        if not data:
            return (0.0, [0.0])
        
        individual_mrr = []
        total_sum = 0.0
        
        for vec, k in data:
            if k <= 0 or not vec:
                individual_mrr.append(0.0)
            else:
                try:
                    idx = vec.index(1)
                except ValueError:
                    idx = -1
                if idx == -1:
                    mrr_val = 0.0
                else:
                    mrr_val = 1.0 / (idx + 1)
                individual_mrr.append(mrr_val)
                total_sum += mrr_val
                
        average_mrr = total_sum / len(data) if data else 0.0
        return (average_mrr, individual_mrr)
    
    @staticmethod
    def map(data):
        if not data:
            return (0.0, [0.0])
        
        separate_result = []
        
        for sub_list, total_num in data:
            if total_num == 0:
                separate_result.append(0.0)
                continue
                
            n = len(sub_list)
            ranking_array = [1.0 / (i + 1) for i in range(n)]
            count = 1
            right_ranking_list = []
            for elem in sub_list:
                if elem != 0:
                    right_ranking_list.append(count)
                    count += 1
                else:
                    right_ranking_list.append(0)
                    
            ap = 0.0
            for i in range(n):
                ap += right_ranking_list[i] * ranking_array[i]
                
            ap /= total_num
            separate_result.append(ap)
            
        mean_ap = sum(separate_result) / len(separate_result) if separate_result else 0.0
        return (mean_ap, separate_result)