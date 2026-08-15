#include <iostream>
#include <vector>
#include <iomanip>

static int javaIntMul(int a, int b) {
    return static_cast<int>(static_cast<unsigned int>(a) * static_cast<unsigned int>(b));
}

static double kahanSum(const std::vector<double>& values) {
    double sum = 0.0;
    double c = 0.0;
    for (double value : values) {
        double y = value - c;
        double t = sum + y;
        c = (t - sum) - y;
        sum = t;
    }
    return sum;
}

double kappa(const std::vector<std::vector<int>>& testData, int k) {
    double P0 = 0.0;
    for (int i = 0; i < k; ++i) {
        P0 += testData.at(i).at(i) * 1.0;
    }

    std::vector<int> xsum(k, 0);
    std::vector<int> ysum(k, 0);
    int sum = 0;

    for (int i = 0; i < k; ++i) {
        for (int j = 0; j < k; ++j) {
            int val = testData.at(i).at(j);
            xsum[i] += val;
            ysum[j] += val;
            sum += val;
        }
    }

    double Pe = 0.0;
    for (int i = 0; i < k; ++i) {
        Pe += javaIntMul(ysum[i], xsum[i]);
    }

    Pe = Pe / javaIntMul(sum, sum);
    P0 = P0 / sum;

    return (P0 - Pe) / (1.0 - Pe);
}

double fleissKappa(const std::vector<std::vector<int>>& testData, int N, int k, int n) {
    std::vector<double> P(N, 0.0);
    double sum = 0.0;

    for (int i = 0; i < N; ++i) {
        double temp = 0.0;
        for (int j = 0; j < k; ++j) {
            int val = testData.at(i).at(j);
            sum += val;
            temp += javaIntMul(val, val);
        }
        temp -= n;
        temp /= javaIntMul(n - 1, n);
        P[i] = temp;
    }

    double P0 = kahanSum(P) / N;

    std::vector<double> pj(k, 0.0);
    for (int j = 0; j < k; ++j) {
        for (int i = 0; i < N; ++i) {
            pj[j] += testData.at(i).at(j);
        }
        pj[j] /= sum;
    }

    std::vector<double> squares(k);
    for (int j = 0; j < k; ++j) {
        squares[j] = pj[j] * pj[j];
    }

    double Pe = kahanSum(squares);

    return (P0 - Pe) / (1.0 - Pe);
}

int main() {
    std::cout << std::setprecision(17);
    std::cout << kappa({{2,1,1},{1,2,1},{1,1,2}}, 3) << '\n';
    std::cout << fleissKappa({{0,0,0,0,14},
                              {0,2,6,4,2},
                              {0,0,3,5,6},
                              {0,3,9,2,0},
                              {2,2,8,1,1},
                              {7,7,0,0,0},
                              {3,2,6,3,0},
                              {2,5,3,2,2},
                              {6,5,2,1,0},
                              {0,2,2,3,7}}, 10, 5, 14) << '\n';
    return 0;
}