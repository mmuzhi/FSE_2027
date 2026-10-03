#include <vector>
#include <algorithm>
#include <cmath>
#include <map>
#include <iostream>
#include <cstddef> // for size_t

class DataStatistics {
public:
    double mean(std::vector<int> data) {
        double sum = 0.0;
        for (int num : data) {
            sum += num;
        }
        double average = sum / static_cast<double>(data.size());
        return std::round(average * 100.0) / 100.0;
    }

    double median(std::vector<int> data) {
        std::vector<int> sortedData = data;
        std::sort(sortedData.begin(), sortedData.end());
        size_t n = sortedData.size();

        if (n % 2 == 0) {
            size_t middle = n / 2;
            double average = (sortedData[middle - 1] + sortedData[middle]) / 2.0;
            return std::round(average * 100.0) / 100.0;
        } else {
            size_t middle = n / 2;
            return sortedData[middle];
        }
    }

    std::vector<int> mode(std::vector<int> data) {
        std::map<int, long> frequencyMap;
        for (int num : data) {
            frequencyMap[num]++;
        }

        long maxCount = 0;
        for (const auto& pair : frequencyMap) {
            if (pair.second > maxCount) {
                maxCount = pair.second;
            }
        }

        std::vector<int> modes;
        for (const auto& pair : frequencyMap) {
            if (pair.second == maxCount) {
                modes.push_back(pair.first);
            }
        }

        std::sort(modes.begin(), modes.end());
        return modes;
    }
};