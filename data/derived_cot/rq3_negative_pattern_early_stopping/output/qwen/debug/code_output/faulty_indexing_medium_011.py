class Solution:
    def invalidTransactions(self, transactions: List[str]) -> List[str]:
        invalid = []
        txn_dict = {}
        n = len(transactions)
        for idx, trn in enumerate(transactions):
            parts = trn.split(",")
            name = parts[0]
            time = parts[1]
            amount = parts[2]
            city = parts[3]
            if name not in txn_dict:
                txn_dict[name] = []
            txn_dict[name].append([time, amount, city, idx])
        
        for idx in range(n):
            parts = transactions[idx].split(",")
            name = parts[0]
            time = parts[1]
            amount_val = int(parts[2])
            city = parts[3]
            if amount_val > 1000:
                invalid.append(transactions[idx])
            else:
                for trn in txn_dict[name]:
                    stored_time, stored_amount, stored_city, stored_idx = trn
                    if stored_idx == idx:
                        continue
                    if stored_city != city and abs(int(time) - int(stored_time)) <= 60:
                        invalid.append(transactions[idx])
                        break
        return invalid