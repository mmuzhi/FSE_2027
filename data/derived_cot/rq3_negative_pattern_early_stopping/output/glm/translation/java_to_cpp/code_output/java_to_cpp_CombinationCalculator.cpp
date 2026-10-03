#include <vector>
#include <string>
#include <limits>
#include <stdexcept>

class CombinationCalculator {
private:
    std::vector<std::string> datas;

    static int factorial(int x) {
        unsigned int result = 1;
        for (int i = 1; i <= x; i++) {
            result *= static_cast<unsigned int>(i);
        }
        return static_cast<int>(result);
    }

protected:
    void _select(int dataIndex, std::vector<std::string>& resultList, int resultIndex, std::vector<std::vector<std::string>>& result, int m) {
        if (resultIndex == m) {
            result.push_back(resultList);
            return;
        }

        for (int i = dataIndex; i <= static_cast<int>(datas.size()) - (m - resultIndex); i++) {
            resultList.insert(resultList.begin() + resultIndex, datas.at(i));
            _select(i + 1, resultList, resultIndex + 1, result, m);
            resultList.erase(resultList.begin() + resultIndex);
        }
    }

public:
    CombinationCalculator(std::vector<std::string> datas) : datas(std::move(datas)) {}

    static int count(int n, int m) {
        if (m == 0 || n == m) {
            return 1;
        }
        int fn = factorial(n);
        int fnm = factorial(n - m);
        int fm = factorial(m);
        unsigned int u_fnm = static_cast<unsigned int>(fnm);
        unsigned int u_fm = static_cast<unsigned int>(fm);
        unsigned int u_prod = u_fnm * u_fm;
        int prod = static_cast<int>(u_prod);
        return fn / prod;
    }

    static double countAll(int n) {
        if (n < 0 || n > 63) {
            return std::numeric_limits<double>::quiet_NaN();
        }
        if (n == 63) {
            return std::numeric_limits<double>::infinity();
        }
        int shift = n & 31;
        unsigned int uval = 1U << shift;
        unsigned int ures = uval - 1;
        int res = static_cast<int>(ures);
        return static_cast<double>(res);
    }

    std::vector<std::vector<std::string>> select(int m) {
        std::vector<std::vector<std::string>> result;
        std::vector<std::string> resultList;
        _select(0, resultList, 0, result, m);
        return result;
    }

    std::vector<std::vector<std::string>> selectAll() {
        std::vector<std::vector<std::string>> result;
        for (int i = 1; i <= static_cast<int>(datas.size()); i++) {
            std::vector<std::vector<std::string>> partial = select(i);
            result.insert(result.end(), partial.begin(), partial.end());
        }
        return result;
    }
};