#include <string>
#include <optional>
#include <algorithm>
#include <array>
#include <cstddef>

class PersonRequest {
public:
    // Fields are None in Python when invalid -> std::optional<std::string>.
    std::optional<std::string> name;
    std::optional<std::string> sex;
    std::optional<std::string> phoneNumber;

    PersonRequest(const std::string& name,
                  const std::string& sex,
                  const std::string& phoneNumber)
        : name(validateName(name)),
          sex(validateSex(sex)),
          phoneNumber(validatePhoneNumber(phoneNumber)) {}

private:
    static std::optional<std::string> validateName(const std::string& name) {
        if (name.empty()) {
            return std::nullopt;
        }
        if (name.size() > 33) {
            return std::nullopt;
        }
        return name;
    }

    static std::optional<std::string> validateSex(const std::string& sex) {
        static const std::array<std::string, 3> validSexes = {"Man", "Woman", "UGM"};
        if (std::find(validSexes.begin(), validSexes.end(), sex) == validSexes.end()) {
            return std::nullopt;
        }
        return sex;
    }

    static bool isAsciiDigit(char c) {
        return c >= '0' && c <= '9';
    }

    static std::optional<std::string> validatePhoneNumber(const std::string& phoneNumber) {
        if (phoneNumber.empty()) {
            return std::nullopt;
        }
        if (phoneNumber.size() != 11 ||
            !std::all_of(phoneNumber.begin(), phoneNumber.end(), isAsciiDigit)) {
            return std::nullopt;
        }
        return phoneNumber;
    }
};