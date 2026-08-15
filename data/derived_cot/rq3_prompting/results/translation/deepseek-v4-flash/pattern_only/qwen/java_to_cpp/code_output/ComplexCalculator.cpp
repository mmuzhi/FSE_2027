#include <cmath>
#include <charconv>
#include <string>
#include <system_error>

class ComplexCalculator {
public:
    class ComplexNumber {
    private:
        double real;
        double imaginary;

        static int doubleCompare(double d1, double d2) {
            if (std::isnan(d1) && std::isnan(d2)) return 0;
            if (d1 < d2) return -1;
            if (d1 > d2) return 1;
            if (d1 == d2) {
                if (d1 == 0.0) {
                    bool b1 = std::signbit(d1);
                    bool b2 = std::signbit(d2);
                    if (b1 != b2) return b1 ? -1 : 1;
                }
                return 0;
            }
            if (std::isnan(d1)) return 1;
            if (std::isnan(d2)) return -1;
            return 0;
        }

        static std::string doubleToString(double value) {
            if (std::isnan(value)) return "NaN";
            if (std::isinf(value)) return value > 0 ? "Infinity" : "-Infinity";
            if (value == 0.0) {
                return std::signbit(value) ? "-0.0" : "0.0";
            }

            char buffer[128];
            auto result = std::to_chars(buffer, buffer + sizeof(buffer), value, std::chars_format::scientific);
            if (result.ec != std::errc()) {
                return "NaN";
            }
            std::string sci(buffer, result.ptr);

            size_t pos = 0;
            std::string sign;
            if (sci[0] == '-') {
                sign = "-";
                pos = 1;
            } else if (sci[0] == '+') {
                pos = 1;
            }

            size_t ePos = sci.find('e', pos);
            std::string mantissa = sci.substr(pos, ePos - pos);
            int exp = std::stoi(sci.substr(ePos + 1));

            size_t dotPos = mantissa.find('.');
            std::string intPart = dotPos == std::string::npos ? mantissa : mantissa.substr(0, dotPos);
            std::string fracPart = dotPos == std::string::npos ? "" : mantissa.substr(dotPos + 1);

            while (!fracPart.empty() && fracPart.back() == '0') {
                fracPart.pop_back();
            }

            std::string digits = intPart + fracPart;

            if (exp >= -3 && exp < 7) {
                if (exp >= 0) {
                    int intLen = exp + 1;
                    if (digits.length() <= static_cast<size_t>(intLen)) {
                        std::string intPartStr = digits;
                        intPartStr.append(intLen - digits.length(), '0');
                        return sign + intPartStr + ".0";
                    } else {
                        std::string intPartStr = digits.substr(0, intLen);
                        std::string fracPartStr = digits.substr(intLen);
                        return sign + intPartStr + "." + fracPartStr;
                    }
                } else {
                    int zeros = -exp - 1;
                    std::string result = sign + "0.";
                    result.append(zeros, '0');
                    result += digits;
                    return result;
                }
            } else {
                std::string mantissaStr;
                if (digits.length() == 1) {
                    mantissaStr = digits + ".0";
                } else {
                    mantissaStr = digits.substr(0, 1) + "." + digits.substr(1);
                }
                return sign + mantissaStr + "E" + std::to_string(exp);
            }
        }

    public:
        ComplexNumber(double real, double imaginary) : real(real), imaginary(imaginary) {}

        double getReal() const { return real; }
        double getImaginary() const { return imaginary; }

        bool equals(const ComplexNumber& other) const {
            return doubleCompare(real, other.real) == 0 && doubleCompare(imaginary, other.imaginary) == 0;
        }

        bool operator==(const ComplexNumber& other) const {
            return equals(other);
        }

        std::string toString() const {
            return doubleToString(real) + (imaginary >= 0 ? "+" : "") + doubleToString(imaginary) + "j";
        }
    };

    ComplexNumber add(const ComplexNumber& c1, const ComplexNumber& c2) {
        double real = c1.getReal() + c2.getReal();
        double imaginary = c1.getImaginary() + c2.getImaginary();
        return ComplexNumber(real, imaginary);
    }

    ComplexNumber subtract(const ComplexNumber& c1, const ComplexNumber& c2) {
        double real = c1.getReal() - c2.getReal();
        double imaginary = c1.getImaginary() - c2.getImaginary();
        return ComplexNumber(real, imaginary);
    }

    ComplexNumber multiply(const ComplexNumber& c1, const ComplexNumber& c2) {
        double real = c1.getReal() * c2.getReal() - c1.getImaginary() * c2.getImaginary();
        double imaginary = c1.getReal() * c2.getImaginary() + c1.getImaginary() * c2.getReal();
        return ComplexNumber(real, imaginary);
    }

    ComplexNumber divide(const ComplexNumber& c1, const ComplexNumber& c2) {
        double denominator = c2.getReal() * c2.getReal() + c2.getImaginary() * c2.getImaginary();
        double real = (c1.getReal() * c2.getReal() + c1.getImaginary() * c2.getImaginary()) / denominator;
        double imaginary = (c1.getImaginary() * c2.getReal() - c1.getReal() * c2.getImaginary()) / denominator;
        return ComplexNumber(real, imaginary);
    }
};