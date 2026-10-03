const std::vector<int>& get(int index) const {
    auto nums = setNum();
    int size = nums[0];
    int remainder = nums[1];
    int start = index * size + std::min(index, remainder);
    int end = start + size;
    if (index + 1 <= remainder) {
        end += 1;
    }
    // We want to return a reference to the segment [start, end) of the internal vector.
    // But we cannot return a reference to a part of a vector without the entire vector being managed by the caller.
    // We can return a reference to the entire vector? No, because the segment is not the entire vector.
    // We can return a reference to a temporary vector that is a copy? No, because then it's a copy.

    // Alternatively, we can use a std::vector_view if we are allowed to use C++20 and the standard library supports it.
    // But std::vector_view is not standard until C++23.

    // Given the constraints, I think we must return a copy.

    // Let's return a copy.
    return std::vector<int>(lst.begin() + start, lst.begin() + end);
}