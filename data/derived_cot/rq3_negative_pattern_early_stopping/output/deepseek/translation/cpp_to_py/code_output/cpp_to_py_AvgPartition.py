class AvgPartition:
    """
    Replicates the behavior of the C++ AvgPartition class.

    Attributes:
        _lst (list): The underlying list.
        _limit (int): The number of partitions.
    """

    def __init__(self, lst, limit):
        """
        Args:
            lst (list): List of elements to partition.
            limit (int): Number of partitions.
        """
        self._lst = lst
        self._limit = limit

    def set_num(self):
        """
        Returns a tuple (size, remainder) where:
            size = len(lst) // limit
            remainder = len(lst) % limit
        """
        size = len(self._lst) // self._limit
        remainder = len(self._lst) % self._limit
        return (size, remainder)

    def get(self, index):
        """
        Returns the index-th partition of the list.

        Partitions are computed so that the first `remainder` partitions have
        size+1 elements, and the rest have size elements.

        Args:
            index (int): 0-based index of the partition.

        Returns:
            list: The sublist corresponding to the partition.
        """
        size, remainder = self.set_num()
        start = index * size + min(index, remainder)
        end = start + size
        if index + 1 <= remainder:
            end += 1
        return self._lst[start:end]