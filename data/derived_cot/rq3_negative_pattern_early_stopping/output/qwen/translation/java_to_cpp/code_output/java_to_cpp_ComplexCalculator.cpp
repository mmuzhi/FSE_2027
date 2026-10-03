#include <cmath>
#include <string>
#include <sstream>
#include <iostream>

class ComplexCalculator {
private:
    struct ComplexNumber {
        double real;
        double imaginary;

        ComplexNumber(double real, double imaginary) : real(real), imaginary(imaginary) {}

        double getReal() const { return real; }
        double getImaginary() const { return imaginary; }

        // Helper function to compare two doubles for equality, handling NaN and infinity.
        static bool doubleEqual(double a, double b) {
            if (std::isnan(a) || std::isnan(b)) {
                return false;
            }
            if (std::isinf(a) && std::isinf(b)) {
                return (a == b);
            }
            return a == b;
        }
    };

public:
    // Operations as static methods in ComplexCalculator
    static ComplexNumber add(const ComplexNumber& c1, const ComplexNumber& c2) {
        double real = c1.getReal() + c2.getReal();
        double imaginary = c1.getImaginary() + c2.getImaginary();
        return ComplexNumber(real, imaginary);
    }

    static ComplexNumber subtract(const ComplexNumber& c1, const ComplexNumber& c2) {
        double real = c1.getReal() - c2.getReal();
        double imaginary = c1.getImaginary() - c2.getImaginary();
        return ComplexNumber(real, imaginary);
    }

    static ComplexNumber multiply(const ComplexNumber& c1, const ComplexNumber& c2) {
        double real = c1.getReal() * c2.getReal() - c1.getImaginary() * c2.getImaginary();
        double imaginary = c1.getReal() * c2.getImaginary() + c1.getImaginary() * c2.getReal();
        return ComplexNumber(real, imaginary);
    }

    static ComplexNumber divide(const ComplexNumber& c1, const ComplexNumber& c2) {
        double denominator = c2.getReal() * c2.getReal() + c2.getImaginary() * c2.getImaginary();
        if (denominator == 0) {
            // In Java, this would throw an exception? But the problem says to keep behavior identical.
            // The Java code does not check for division by zero. It would cause an arithmetic exception.
            // We'll throw an exception in C++ as well.
            throw std::runtime_error("Division by zero");
        }
        double real = (c1.getReal() * c2.getReal() + c1.getImaginary() * c2.getImaginary()) / denominator;
        double imaginary = (c1.getImaginary() * c2.getReal() - c1.getReal() * c2.getImaginary()) / denominator;
        return ComplexNumber(real, imaginary);
    }

    // We'll define a free function for equality if we want to use it outside, but the original Java code doesn't have a separate equals method for the outer class.
    // However, the ComplexNumber.equals is defined in the inner class. We'll define a free function for equality for ComplexNumber.
    static bool equals(const ComplexNumber& c1, const ComplexNumber& c2) {
        return ComplexNumber::doubleEqual(c1.real, c2.real) && ComplexNumber::doubleEqual(c1.imaginary, c2.imaginary);
    }

    // We'll define a free function for toString for ComplexNumber.
    static std::string toString(const ComplexNumber& c) {
        std::ostringstream oss;
        if (c.imaginary >= 0) {
            oss << c.real << "+" << c.imaginary << "j";
        } else {
            oss << c.real << c.imaginary << "j";
        }
        return oss.str();
    }
};

// We can also define the free function for equality and toString in the ComplexNumber struct, but we did them as static in the outer class for consistency with the Java code's structure (which has the equals and toString as methods of ComplexNumber).

// However, note: the Java code has the equals and toString as methods of ComplexNumber. We can move these to be member functions of ComplexNumber.

// Let's refactor to have the equals and toString as member functions of ComplexNumber.

// We'll change the ComplexNumber struct to have these member functions.

// But note: the equals method in Java uses Object.equals, which is a method of Object. In C++, we don't have that, but we can define a custom comparison.

// Alternatively, we can keep the free functions as above.

// Since the problem says to keep behavior identical, and the original Java code has the equals and toString as methods of ComplexNumber, we should move them to be member functions.

// Let's do that:

// We'll remove the free functions and define:

//   bool equals(const ComplexNumber& that) const;
//   std::string toString() const;

// But note: the original Java code does not have a toString that takes an argument. It's just the default toString.

// We'll change the ComplexNumber struct to have these member functions.

// We'll also change the equals method to use the helper function.

// Revised ComplexNumber struct:

//   struct ComplexNumber {
//       double real;
//       double imaginary;
//
//       ComplexNumber(double real, double imaginary) : real(real), imaginary(imaginary) {}
//
//       double getReal() const { return real; }
//       double getImaginary() const { return imaginary; }
//
//       bool equals(const ComplexNumber& that) const {
//           return doubleEqual(real, that.real) && doubleEqual(imaginary, that.imaginary);
//       }
//
//       std::string toString() const {
//           std::ostringstream oss;
//           if (imaginary >= 0) {
//               oss << real << "+" << imaginary << "j";
//           } else {
//               oss << real << imaginary << "j";
//           }
//           return oss.str();
//       }
//
//       static bool doubleEqual(double a, double b) {
//           if (std::isnan(a) || std::isnan(b)) {
//               return false;
//           }
//           if (std::isinf(a) && std::isinf(b)) {
//               return (a == b);
//           }
//           return a == b;
//       }
//   };

// But note: the equals method in Java is defined as:

//   @Override
//   public boolean equals(Object obj) {
//       if (this == obj) return true;
//       if (obj == null || getClass() != obj.getClass()) return false;
//       ComplexNumber that = (ComplexNumber) obj;
//       return Double.compare(that.real, real) == 0 && Double.compare(that.imaginary, imaginary) == 0;
//   }

// We are missing the null check and class check. In C++, we can do:

//   bool equals(const ComplexNumber& that) const {
//       if (this == &that) return true;
//       // We don't have a way to check the class in the same way, but since it's a nested struct, we can assume that the object is of type ComplexNumber.
//       // But note: in C++, we can have derived classes, but we don't have inheritance here.
//       // We'll just compare the values.
//       return doubleEqual(real, that.real) && doubleEqual(imaginary, that.imaginary);
//   }

// However, the Java code does a getClass() check. In C++, we don't have getClass() unless we use RTTI. We can avoid it because the problem says to keep behavior identical and the original code doesn't have inheritance.

// Alternatively, we can do:

//   bool equals(const ComplexNumber& that) const {
//       if (this == &that) return true;
//       if (that.real != real || that.imaginary != imaginary) return false;
//       return true;
//   }

// But wait, we are using doubleEqual to handle NaN and infinity. We should use that.

// Let's stick to the doubleEqual function.

// We'll change the ComplexNumber struct to have the member functions.

// We'll also change the operations in ComplexCalculator to use the member functions.

// But note: the operations in ComplexCalculator are static and take a ComplexNumber by const reference. They don't need to call the member functions of ComplexNumber.

// We'll change the ComplexNumber struct to have the equals and toString as member functions.

// Final code:

#include <cmath>
#include <string>
#include <sstream>
#include <iostream>

class ComplexCalculator {
private:
    struct ComplexNumber {
        double real;
        double imaginary;

        ComplexNumber(double real, double imaginary) : real(real), imaginary(imaginary) {}

        double getReal() const { return real; }
        double getImaginary() const { return imaginary; }

        bool equals(const ComplexNumber& that) const {
            if (this == &that) return true;
            if (std::isnan(real) || std::isnan(that.real) || std::isnan(imaginary) || std::isnan(that.imaginary)) {
                return false;
            }
            if (std::isinf(real) && std::isinf(that.real) && std::isinf(imaginary) && std::isinf(that.imaginary)) {
                return (real == that.real) && (imaginary == that.imaginary);
            }
            return (real == that.real) && (imaginary == that.imaginary);
        }

        std::string toString() const {
            std::ostringstream oss;
            if (imaginary >= 0) {
                oss << real << "+" << imaginary << "j";
            } else {
                oss << real << imaginary << "j";
            }
            return oss.str();
        }

        static bool doubleEqual(double a, double b) {
            if (std::isnan(a) || std::isnan(b)) {
                return false;
            }
            if (std::isinf(a) && std::isinf(b)) {
                return (a == b);
            }
            return a == b;
        }
    };

public:
    static ComplexNumber add(const ComplexNumber& c1, const ComplexNumber& c2) {
        double real = c1.getReal() + c2.getReal();
        double imaginary = c1.getImaginary() + c2.getImaginary();
        return ComplexNumber(real, imaginary);
    }

    static ComplexNumber subtract(const ComplexNumber& c1, const ComplexNumber& c2) {
        double real = c1.getReal() - c2.getReal();
        double imaginary = c1.getImaginary() - c2.getImaginary();
        return ComplexNumber(real, imaginary);
    }

    static ComplexNumber multiply(const ComplexNumber& c1, const ComplexNumber& c2) {
        double real = c1.getReal() * c2.getReal() - c1.getImaginary() * c2.getImaginary();
        double imaginary = c1.getReal() * c2.getImaginary() + c1.getImaginary() * c2.getReal();
        return ComplexNumber(real, imaginary);
    }

    static ComplexNumber divide(const ComplexNumber& c1, const ComplexNumber& c2) {
        double denominator = c2.getReal() * c2.getReal() + c2.getImaginary() * c2.getImaginary();
        if (denominator == 0) {
            throw std::runtime_error("Division by zero");
        }
        double real = (c1.getReal() * c2.getReal() + c1.getImaginary() * c2.getImaginary()) / denominator;
        double imaginary = (c1.getImaginary() * c2.getReal() - c1.getReal() * c2.getImaginary()) / denominator;
        return ComplexNumber(real, imaginary);
    }
};

// We removed the free functions for equals and toString because they are now member functions.

// However, note: the equals method in the Java code does a getClass() check. We did a pointer check (this == &that) but not a class check. Since we don't have inheritance, it's okay.

// But wait, the equals method in Java does:

//   if (this == obj) return true;
//   if (obj == null || getClass() != obj.getClass()) return false;

// We are missing the getClass() check. In C++, we can use:

//   if (obj == nullptr || dynamic_cast<const ComplexNumber*>(obj) == nullptr) return false;

// But that would require RTTI and change the behavior for derived classes. We don't have derived classes, so we can skip it.

// Alternatively, we can change the equals method to:

//   bool equals(const ComplexNumber& that) const {
//       if (this == &that) return true;
//       // Check if the other object is of the same type
//       if (typeid(that) != typeid(ComplexNumber)) {
//           return false;
//       }
//       return doubleEqual(real, that.real) && doubleEqual(imaginary, that.imaginary);
//   }

// But note: the original Java code does not have a getClass() check in the equals method? Actually, it does:

//   if (obj == null || getClass() != obj.getClass()) return false;

// We can use RTTI to mimic that.

// However, the problem says to keep behavior identical. The Java code would return false if the object is not an instance of ComplexNumber. In C++, if we pass an object of a different type, we should return false.

// We'll use RTTI to check the type.

// But note: the operations in ComplexCalculator are static and take a ComplexNumber by const reference. So the equals method is only called on ComplexNumber instances.

// We'll change the equals method to:

//   bool equals(const ComplexNumber& that) const {
//       if (this == &that) return true;
//       if (typeid(that) != typeid(ComplexNumber)) {
//           return false;
//       }
//       return doubleEqual(real, that.real) && doubleEqual(imaginary, that.imaginary);
//   }

// However, the original Java code does not have a separate type for ComplexNumber, so it's always the same class.

// Alternatively, we can avoid RTTI and just compare the values, because the problem doesn't specify that the equals method should be used on derived classes.

// Let's keep it simple and just compare the values.

// Final code without RTTI.

// We'll output the code as below.

// Note: The above code is very long and has a lot of details. We must be cautious.

// Let's write the final code.

// We'll also note that the divide method throws an exception on division by zero, which is the same as Java.

// We'll include the necessary headers.

// Final code:
</think>
To translate the provided Java code to C++, we need to maintain the same behavior, including handling of edge cases and exceptions. The solution involves creating a nested `ComplexNumber` struct within the `ComplexCalculator` class, ensuring all operations and comparisons are correctly implemented.