#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>

// Mimics Java's Double.toString(double) closely for the values printed here:
// shortest decimal string that round-trips to the same double, with a
// fractional digit, and Java-style exponent formatting.
static std::string javaDoubleToString(double v) {
    if (std::isnan(v)) return "NaN";
    if (std::isinf(v)) return v > 0 ? "Infinity" : "-Infinity";

    char buf[64];
    for (int prec = 1; prec <= 17; ++prec) {
        std::snprintf(buf, sizeof(buf), "%.*g", prec, v);
        if (std::strtod(buf, nullptr) == v) break;
    }

    std::string s(buf);
    size_t epos = s.find('e');
    if (epos == std::string::npos) {
        if (s.find('.') == std::string::npos) s += ".0";
        return s;
    }
    std::string mant = s.substr(0, epos);
    std::string exp = s.substr(epos + 1);
    if (mant.find('.') == std::string::npos) mant += ".0";
    bool negExp = !exp.empty() && exp[0] == '-';
    if (!exp.empty() && (exp[0] == '+' || exp[0] == '-')) exp.erase(0, 1);
    while (exp.size() > 1 && exp[0] == '0') exp.erase(0, 1);
    return mant + "E" + (negExp ? "-" : "") + exp;
}

double kappa(const std::vector<std::vector<int>>& testData, int k) {
    const auto& dataMat = testData;
    double P0 = 0.0;
    for (int i = 0; i < k; i++) {
        P0 += dataMat[i][i] * 1.0;
    }
    std::vector<int> xsum(k, 0);
    std::vector<int> ysum(k, 0);
    int sum = 0;
    for (int i = 0; i < k; i++) {
        for (int j = 0; j < k; j++) {
            xsum[i] += dataMat[i][j];
            ysum[j] += dataMat[i][j];
            sum += dataMat[i][j];
        }
    }
    double Pe = 0.0;
    for (int i = 0; i < k; i++) {
        // int * int (Java overflow semantics), then widened to double
        Pe += static_cast<double>(ysum[i] * xsum[i]);
    }
    Pe = Pe / (sum * sum);
    P0 = P0 / sum;
    return (P0 - Pe) / (1 - Pe);
}

double fleissKappa(const std::vector<std::vector<int>>& testData, int N, int k, int n) {
    const auto& dataMat = testData;
    std::vector<double> P(N, 0.0);
    double sum = 0.0;
    for (int i = 0; i < N; i++) {
        double temp = 0.0;
        for (int j = 0; j < k; j++) {
            sum += dataMat[i][j];
            temp += dataMat[i][j] * dataMat[i][j];
        }
        temp -= n;
        temp /= static_cast<double>((n - 1) * n);
        P[i] = temp;
    }
    double P0 = 0.0;
    for (double p : P) P0 += p;   // Arrays.stream(P).sum(), same order
    P0 /= N;
    std::vector<double> pj(k, 0.0);
    for (int j = 0; j < k; j++) {
        for (int i = 0; i < N; i++) {
            pj[j] += dataMat[i][j];
        }
        pj[j] /= sum;
    }
    double Pe = 0.0;
    for (double p : pj) Pe += p * p;   // Arrays.stream(pj).map(p -> p * p).sum()
    return (P0 - Pe) / (1 - Pe);
}

int main() {
    std::cout << javaDoubleToString(kappa({{2, 1, 1}, {1, 2, 1}, {1, 1, 2}}, 3)) << "\n";
    std::cout << javaDoubleToString(fleissKappa({{0, 0, 0, 0, 14},
                                                 {0, 2, 6, 4, 2},
                                                 {0, 0, 3, 5, 6},
                                                 {0, 3, 9, 2, 0},
                                                 {2, 2, 8, 1, 1},
                                                 {7, 7, 0, 0, 0},
                                                 {3, 2, 6, 3, 0},
                                                 {2, 5, 3, 2, 2},
                                                 {6, 5, 2, 1, 0},
                                                 {0, 2, 2, 3, 7}},
                                       10, 5, 14)) << "\n";
    return 0;
}