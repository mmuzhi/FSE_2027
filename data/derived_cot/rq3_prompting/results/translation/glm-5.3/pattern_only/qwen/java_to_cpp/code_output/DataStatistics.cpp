#include <algorithm>
#include <cmath>
#include <map>
#include <stdexcept>
#include <vector>

namespace org::example {

class DataStatistics {
public:
    double mean(const std::vector<int>& data) const {
        int sum = 0; // int accumulation, matching Arrays.stream(data).sum() overflow semantics
        for (int value : data) sum += value;
        double dsum = static_cast<double>(sum);
        return javaRound((dsum / static_cast<double>(data.size())) * 100.0) / 100.0;
    }

    double median(const std::vector<int>& data) const {
        std::vector<int> sortedData(data);
        std::sort(sortedData.begin(), sortedData.end());
        const int n = static_cast<int>(sortedData.size());

        if (n % 2 == 0) {
            int middle = n / 2;
            return javaRound(((sortedData[middle - 1] + sortedData[middle]) / 2.0) * 100.0) / 100.0;
        } else {
            int middle = n / 2;
            return static_cast<double>(sortedData[middle]);
        }
    }

    std::vector<int> mode(const std::vector<int>& data) const {
        std::map<int, long long> frequencyMap;
        for (int e : data) ++frequencyMap[e];

        if (frequencyMap.empty()) {
            // Collections.max on an empty collection throws NoSuchElementException
            throw std::runtime_error("NoSuchElementException");
        }

        long long maxCount = frequencyMap.begin()->second;
        for (const auto& entry : frequencyMap)
            maxCount = std::max(maxCount, entry.second);

        std::vector<int> result;
        for (const auto& entry : frequencyMap)
            if (entry.second == maxCount) result.push_back(entry.first);
        std::sort(result.begin(), result.end());
        return result;
    }

private:
    // Java Math.round(double): nearest long, ties toward positive infinity; NaN -> 0
    static double javaRound(double value) {
        if (std::isnan(value)) return 0.0;
        return std::floor(value + 0.5);
    }
};

} // namespace org::example