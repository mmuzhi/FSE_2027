#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

string padLeft(const string& s, int length) {
    string padded;
    if ((int)s.size() >= length) {
        padded = s;
    } else {
        padded = string(length - (int)s.size(), ' ') + s;
    }
    for (char& c : padded) {
        if (c == ' ') c = '0';
    }
    return padded;
}

string add(const string& num1, const string& num2) {
    int maxLength = max((int)num1.size(), (int)num2.size());
    string a = padLeft(num1, maxLength);
    string b = padLeft(num2, maxLength);

    int carry = 0;
    string result;
    result.reserve(maxLength + 1);

    for (int i = maxLength - 1; i >= 0; --i) {
        int digitSum = (a[i] - '0') + (b[i] - '0') + carry;
        carry = digitSum / 10;
        int digit = digitSum % 10;
        result.push_back('0' + digit);
    }

    if (carry > 0) {
        result.push_back('0' + carry);
    }

    reverse(result.begin(), result.end());
    return result;
}

string subtract(string num1, string num2) {
    bool negative = false;

    if (num1.size() < num2.size() ||
        (num1.size() == num2.size() && num1.compare(num2) < 0)) {
        swap(num1, num2);
        negative = true;
    }

    int maxLength = max((int)num1.size(), (int)num2.size());
    num1 = padLeft(num1, maxLength);
    num2 = padLeft(num2, maxLength);

    int borrow = 0;
    string result;
    result.reserve(maxLength);

    for (int i = maxLength - 1; i >= 0; --i) {
        int digitDiff = (num1[i] - '0') - (num2[i] - '0') - borrow;

        if (digitDiff < 0) {
            digitDiff += 10;
            borrow = 1;
        } else {
            borrow = 0;
        }

        result.push_back('0' + digitDiff);
    }

    reverse(result.begin(), result.end());

    while (result.size() > 1 && result[0] == '0') {
        result.erase(result.begin());
    }

    if (negative) {
        result.insert(result.begin(), '-');
    }

    return result;
}

string multiply(const string& num1, const string& num2) {
    int len1 = (int)num1.size();
    int len2 = (int)num2.size();
    vector<int> result(len1 + len2, 0);

    for (int i = len1 - 1; i >= 0; --i) {
        for (int j = len2 - 1; j >= 0; --j) {
            int mul = (num1[i] - '0') * (num2[j] - '0');
            int p1 = i + j;
            int p2 = i + j + 1;
            int total = mul + result[p2];

            result[p1] += total / 10;
            result[p2] = total % 10;
        }
    }

    string sb;
    int n = (int)result.size();
    int start = 0;

    while (start < n - 1 && result[start] == 0) {
        start++;
    }

    for (int i = start; i < n; ++i) {
        sb.push_back('0' + result[i]);
    }

    return sb;
}

int main() {
    cout << add("12345678901234567890", "98765432109876543210") << "\n";
    cout << subtract("12345678901234567890", "98765432109876543210") << "\n";
    cout << multiply("12345678901234567890", "98765432109876543210") << "\n";
    return 0;
}